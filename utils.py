import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pdfminer.high_level import extract_text

# Optional: for better text cleaning (if you want stemming and stopwords)
# import nltk
# from nltk.corpus import stopwords
# from nltk.stem import PorterStemmer
# nltk.download('stopwords')
# stop_words = set(stopwords.words('english'))
# stemmer = PorterStemmer()

def extract_text_from_pdf(path):
    if hasattr(path, 'read'):  # For Streamlit uploaded file
        with open("temp_resume.pdf", "wb") as f:
            f.write(path.read())
        text = extract_text("temp_resume.pdf")
        os.remove("temp_resume.pdf")  # Clean up temp file
        return text
    else:
        return extract_text(path)

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # Basic clean — optional advanced cleaning below
    # tokens = text.split()
    # filtered_tokens = [stemmer.stem(word) for word in tokens if word not in stop_words]
    # return ' '.join(filtered_tokens)
    return text

def calculate_similarity(resume_text, jd_text):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, jd_text])
    score = cosine_similarity(vectors[0:1], vectors[1:2])
    return round(float(score[0][0]) * 100, 2)  # in %

def extract_email(text):
    match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    return match.group(0) if match else "Not found"

def extract_name(text):
    lines = text.strip().split('\n')
    for line in lines[:10]:  # Check first 10 lines only
        line = line.strip()
        words = line.split()
        if 1 < len(words) <= 5 and all(w.istitle() or w.isupper() for w in words):
            return line
    return "Not found"
