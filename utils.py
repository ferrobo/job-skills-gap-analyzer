import re
import spacy

nlp = spacy.load("en_core_web_sm")

STOPWORDS = {
    "experience", "ability", "knowledge", "understanding", "strong",
    "good", "excellent", "work", "working", "team", "years", "year",
    "minimum", "required", "preferred", "plus", "bonus", "candidate",
    "looking", "skills", "skill", "role", "position", "job", "company",
    "opportunity", "responsibilities", "requirements", "qualifications",
    "we", "you", "our", "us", "fine", "tuning", "rest", "models",
    "platforms", "machine", "cloud", "python machine"
}

KNOWN_SKILLS = [
    "machine learning", "deep learning", "natural language processing",
    "computer vision", "data analysis", "data science", "sql", "python",
    "pytorch", "tensorflow", "huggingface", "streamlit", "git", "apis",
    "cloud platforms", "communication", "transformer models"
]

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s\+\#]', ' ', text)
    text = re.sub(r'\b(skills|skill|we are|looking for|a plus|a candidate)\b', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_skills(text):
    text = clean_text(text)
    
    skills = set()
    
    for skill in KNOWN_SKILLS:
        if skill in text:
            skills.add(skill)
    
    doc = nlp(text)
    
    for chunk in doc.noun_chunks:
        skill = chunk.text.strip()
        if (skill not in STOPWORDS
            and len(skill) > 2
            and len(skill.split()) <= 3
            and skill.split()[0] not in STOPWORDS
            and not any(skill in s for s in skills)):
            skills.add(skill)
    
    for token in doc:
        if token.pos_ in ("NOUN", "PROPN") and token.text not in STOPWORDS:
            if len(token.text) > 2:
                if not any(token.text in s for s in skills):
                    skills.add(token.text)
    
    return list(skills)