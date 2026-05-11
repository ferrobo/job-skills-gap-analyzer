import streamlit as st
import plotly.graph_objects as go
from analyzer import analyze_gap

st.set_page_config(page_title="Job Skills Gap Analyzer", page_icon="")

st.title("Job Skills Gap Analyzer")
st.write("Paste a job description and your resume below to see how well you match.")

col1, col2 = st.columns(2)

with col1:
    job_text = st.text_area(
        "Job Description",
        placeholder="Paste the job description here...",
        height=300
    )

with col2:
    candidate_text = st.text_area(
        "Your Resume / Skills",
        placeholder="Paste your resume or skills list here...",
        height=300
    )

if st.button("Analyze Gap"):
    
    if not job_text.strip() or not candidate_text.strip():
        st.warning("Please fill in both fields before analyzing.")
    
    else:
        results = analyze_gap(job_text, candidate_text)
        
        st.divider()
        
        score = results["score"]
        
        if score >= 75:
            color = "green"
        elif score >= 50:
            color = "orange"
        else:
            color = "red"
        
        st.markdown(f"### Match Score: :{color}[{score}%]")
        
        fig = go.Figure(go.Bar(
            x=["Matched", "Missing", "Bonus"],
            y=[len(results["matched"]), len(results["missing"]), len(results["bonus"])],
            marker_color=["green", "red", "blue"]
        ))
        fig.update_layout(title="Skills Breakdown", yaxis_title="Number of Skills")
        st.plotly_chart(fig)
        
        st.markdown("### Matched Skills")
        if results["matched"]:
            for skill in results["matched"]:
                st.success(skill)
        else:
            st.write("No matched skills found.")
        
        st.markdown("### Missing Skills")
        if results["missing"]:
            for skill in results["missing"]:
                st.error(skill)
        else:
            st.write("No missing skills — great match!")
        
        st.markdown("### Bonus Skills (You have these, job does not require them)")
        if results["bonus"]:
            for skill in results["bonus"]:
                st.info(skill)
        else:
            st.write("No bonus skills.")
        
        st.markdown("### Recommendations")
        if results["recommendations"]:
            for rec in results["recommendations"]:
                st.markdown(f"- {rec}")
        else:
            st.write("You are a strong match")