import re
import spacy
import trafilatura

nlp = spacy.load("en_core_web_sm")
nlp.max_length = 200000000
def extract_main_text(content):
    """
    If content is HTML, extract main readable text using trafilatura.
    Otherwise, assume plain text and return as is.
    """
    if "<html" in content.lower() or "<body" in content.lower() or "<div" in content.lower():
        downloaded = trafilatura.extract(content)
        return downloaded if downloaded else ""
    else:
        return content

def normalize_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

def remove_stopwords_and_lemmatize(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)

def preprocess_html(content):
    text = extract_main_text(content)
    text = normalize_text(text)
    text = remove_stopwords_and_lemmatize(text)
    return text