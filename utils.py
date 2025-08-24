import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pdfminer.high_level import extract_text

# Extract text from PDF (works with both local files and Streamlit uploads)
def extract_text_from_pdf(path):
    if hasattr(path, 'read'):  # Streamlit uploaded file
        with open("temp_resume.pdf", "wb") as f:
            f.write(path.read())
        text = extract_text("temp_resume.pdf")
        os.remove("temp_resume.pdf")
        return text
    else:
        return extract_text(path)

# Clean text: lowercase, remove special chars
def clean_text(text):
    text = text.lower()
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

# Calculate similarity (hybrid: cosine + keyword match)
def calculate_similarity(resume_text, jd_text):
    # Step 1: Cosine similarity
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, jd_text])
    cosine_score = float(cosine_similarity(vectors[0:1], vectors[1:2])[0][0]) * 100

    # Step 2: Keyword match percentage
    jd_keywords = set(jd_text.split())
    resume_words = set(resume_text.split())
    matched_keywords = jd_keywords.intersection(resume_words)
    keyword_match_percentage = (len(matched_keywords) / len(jd_keywords)) * 100 if jd_keywords else 0

    # Step 3: Weighted score
    final_score = (0.6 * cosine_score) + (0.4 * keyword_match_percentage)
    return round(final_score, 2)

# Extract email address
def extract_email(text):
    match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    return match.group(0) if match else "Not found"

# Extract name (heuristic: first few lines, looks like a name)
def extract_name(text):
    lines = text.strip().split('\n')
    for line in lines[:10]:  # check first 10 lines only
        line = line.strip()
        words = line.split()
        if 1 < len(words) <= 5 and all(w.istitle() or w.isupper() for w in words):
            return line
    return "Not found"
