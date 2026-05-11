import streamlit as st
import plotly.graph_objects as go
from analyzer import analyze_gap

st.set_page_config(page_title="Job Skills Gap Analyzer", page_icon="", layout="wide")

st.title("Job Skills Gap Analyzer")
st.write("By Migs Manganti")
st.write("Paste a job description and your resume below to see how well you match.")

left, right = st.columns([1, 1])

with left:
    st.subheader("Input")
    job_text = st.text_area(
        "Job Description",
        placeholder="Paste the job description here...",
        height=300
    )
    candidate_text = st.text_area(
        "Your Resume / Skills",
        placeholder="Paste your resume or skills list here...",
        height=300
    )
    analyze = st.button("Analyze Gap", use_container_width=True)

with right:
    st.subheader("Results")
    if analyze:
        if not job_text.strip() or not candidate_text.strip():
            st.warning("Please fill in both fields before analyzing.")
        else:
            results = analyze_gap(job_text, candidate_text)
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
            st.plotly_chart(fig, use_container_width=True)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### Matched Skills")
                if results["matched"]:
                    for skill in results["matched"]:
                        st.success(skill)
                else:
                    st.write("No matched skills found.")

                st.markdown("### Bonus Skills")
                if results["bonus"]:
                    for skill in results["bonus"]:
                        st.info(skill)
                else:
                    st.write("No bonus skills.")

            with col2:
                st.markdown("### Missing Skills")
                if results["missing"]:
                    for skill in results["missing"]:
                        st.error(skill)
                else:
                    st.write("No missing skills — great match!")

                st.markdown("### Recommendations")
                if results["recommendations"]:
                    for rec in results["recommendations"]:
                        st.markdown(f"- {rec}")
                else:
                    st.write("You are a strong match")
    else:
        st.markdown("#### How to use")
        st.markdown("1. Paste a job description in the top left box")
        st.markdown("2. Paste your resume or skills list in the bottom left box")
        st.markdown("3. Click Analyze Gap")
        st.markdown("4. See your match score, skill breakdown, and what to learn next")
        st.divider()
        st.markdown("#### What you will get")
        st.markdown("- A match score from 0 to 100 percent")
        st.markdown("- Matched skills in green")
        st.markdown("- Missing skills in red")
        st.markdown("- Bonus skills you have that the job did not ask for")
        st.markdown("- 3 personalized learning recommendations")