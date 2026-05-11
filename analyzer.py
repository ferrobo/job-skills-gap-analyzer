from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils import extract_skills

def analyze_gap(job_text, candidate_text):
    """Compare job description and candidate resume, return gap analysis."""
    
    # Extract skills from both texts
    job_skills = extract_skills(job_text)
    candidate_skills = extract_skills(candidate_text)
    
    # Convert skill lists to strings for TF-IDF
    job_str = " ".join(job_skills)
    candidate_str = " ".join(candidate_skills)
    
    # TF-IDF vectorization
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([job_str, candidate_str])
    
    # Cosine similarity score
    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    match_percent = round(score * 100, 2)
    
    # Find matched and missing skills
    job_set = set(job_skills)
    candidate_set = set(candidate_skills)
    
    matched = list(job_set & candidate_set)
    missing = list(job_set - candidate_set)
    bonus = list(candidate_set - job_set)
    
    # Generate recommendations
    recommendations = []
    for skill in missing[:3]:
        recommendations.append(f"Learn {skill} — search for free courses on Coursera or freeCodeCamp")
    
    return {
        "score": match_percent,
        "matched": matched,
        "missing": missing,
        "bonus": bonus,
        "recommendations": recommendations
    }