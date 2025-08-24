import streamlit as st
import os
import pandas as pd
from utils import (
    extract_text_from_pdf,
    clean_text,
    calculate_similarity,
    extract_email,
    extract_name   # ✅ replaced wrong "extrse" with "extract_name"
)

# 🛠️ Page Config
st.set_page_config(page_title="Resume Screener", layout="wide")

# 📌 Sidebar Options
with st.sidebar:
    st.title("🔧 Options")
    st.markdown("Built with ❤️ using NLP & Streamlit")
    
    # ✏️ Change Job Description
    st.subheader("✏️ Edit Job Description")
    try:
        with open("job_description.txt", "r", encoding='utf-8') as f:
            current_jd = f.read()
    except FileNotFoundError:
        current_jd = ""

    new_jd = st.text_area("Job Description", value=current_jd, height=200)

    if st.button("💾 Save Job Description"):
        with open("job_description.txt", "w", encoding='utf-8') as f:
            f.write(new_jd)
        st.success("✅ Job description updated successfully!")
        st.rerun()  # Updated for latest Streamlit

# 🧠 Title and Header Image
st.title("📄 AI Resume Screener using NLP")

# Load header image if available
if os.path.exists("assets/header.png"):
    st.image("assets/header.png", use_container_width=True)

# 📋 Description
st.markdown("""
This app compares uploaded resumes against a job description and gives a **matching score**.  
It also highlights resumes that may need improvements based on missing skills or keywords.
""")
st.markdown("Project by **Rahul Kumar**")

# 📄 Load Job Description
try:
    with open("job_description.txt", "r", encoding='utf-8') as f:
        jd_raw = f.read()
    jd_clean = clean_text(jd_raw)
except FileNotFoundError:
    st.error("🚫 Job description file not found. Please ensure 'job_description.txt' is in the app folder.")
    st.stop()

# 📝 Display Job Description
st.subheader("📌 Job Description")
st.info(jd_raw)

# 📥 Upload Resumes
st.subheader("📤 Upload Resumes")
uploaded_files = st.file_uploader("Upload multiple resumes (PDF)", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    st.subheader("📊 Resume Match Results")
    results = []

    for uploaded_file in uploaded_files:
        resume_filename = uploaded_file.name
        resume_text = extract_text_from_pdf(uploaded_file)
        resume_clean = clean_text(resume_text)

        # Extract name and email
        name = extract_name(resume_text)
        email = extract_email(resume_text)

        # Calculate similarity score
        score = calculate_similarity(resume_clean, jd_clean)

        # Find missing keywords (basic approach)
        missing_keywords = []
        for word in jd_clean.split():
            if word not in resume_clean and len(word) > 5:
                missing_keywords.append(word)
        keyword_hint = ", ".join(missing_keywords[:5]) if score < 70 else ""

        # Append result
        results.append({
            "Resume File": resume_filename,
            "Name": name,
            "Email": email,
            "Score (%)": score,
            "Recommendation": "✅ Strong Match" if score >= 70 else "⚠️ Needs Improvement",
            "Missing Keywords": keyword_hint
        })

    # 📊 Display Ranked Results
    df = pd.DataFrame(sorted(results, key=lambda x: x["Score (%)"], reverse=True))

    # 🔋 Add green bars to Score column
    styled_df = df.style.bar(
        subset=["Score (%)"],
        color="#90ee90",
        vmin=0,
        vmax=100
    ).format({
        "Score (%)": "{:.2f}"
    })

    st.dataframe(styled_df)

    # 💾 Download CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Ranked Results as CSV",
        data=csv,
        file_name="ranked_resumes.csv",
        mime="text/csv"
    )
else:
    st.warning("Please upload at least one resume to begin screening.")
