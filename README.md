# 📄 AI Resume Screener using NLP

This is a simple yet powerful AI-driven web application that helps screen resumes against a job description using Natural Language Processing (NLP). It calculates a match score, highlights potential resume improvements, and supports batch upload of multiple PDFs.
▶️ **https://ai-powered-resume-screening-and-ranking-systemgit-rahul.streamlit.app/**
---

## 🔍 Features

- 📤 Upload multiple resumes (PDFs)
- 🧠 NLP-based similarity matching using TF-IDF + Cosine Similarity
- 📌 Compares resumes against a provided Job Description
- 📊 Match score with progress bars and recommendations
- 🔎 Highlights potential missing keywords
- 🎨 Clean Streamlit UI with sidebar and enhancements

---

## 🚀 How it Works

1. **Upload resumes** (PDF format)
2. **Job description** is loaded from a `job_description.txt` file
3. App cleans and analyzes the text using NLP
4. Calculates a similarity score between each resume and the JD
5. Displays recommendations:
   - ✅ Strong Match (Score ≥ 70%)
   - ⚠️ Needs Improvement (Score < 70%)
6. Highlights missing keywords (basic rule-based logic)

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Scikit-learn (TF-IDF + Cosine Similarity)
- pdfminer.six (PDF text extraction)

---

## 📁 Project Structure

resume-screener-nlp/ ├── app.py # Main Streamlit app ├── utils.py # Text extraction, cleaning, similarity functions ├── job_description.txt # Sample JD file to compare resumes ├── requirements.txt # Dependencies └── sample_resumes/ # (Optional) Folder for testing resumes

---

## ✅ To Run Locally

1. Clone the repository  
2. Install dependencies  
    pip install -r requirements.txt
3. Add your job description in a `job_description.txt` file  
4. Run the app  

streamlit run app.py

---

## 📌 Sample

| Resume File       | Match Score | Recommendation       |
|-------------------|-------------|----------------------|
| `resume1.pdf`     | 82.3%       | ✅ Strong Match       |
| `resume2.pdf`     | 56.7%       | ⚠️ Needs Improvement |

---

## 💡 Future Ideas

- AI-powered resume feedback (LLM-based)
- PDF/Markdown export of resume scores
- JD upload option
- Skill visualization or radar charts

---

## 🧑‍💻 Author

    Made with ❤️ by Rahul Kumar

---

## 📜 License

This project is open-source and free to use under the MIT License.
