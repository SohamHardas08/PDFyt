import fitz
import torch
import spacy
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from itertools import combinations
#from transformers import pipeline

nlp = spacy.load("en_core_web_sm")

def extract(file):
    text = ''
    document = fitz.open(file)
    for pages in range(len(document)):
        page = document.load_page(pages)
        text += page.get_text()
        
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)  # Add space between camel case
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    text = re.sub(r'\d+', '', text)  # Remove digits
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = text.lower()  # Convert to lowercase
    return text


def tokenize(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return ' '.join(tokens)

def keywords(text, num_keywords=5):
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), max_features=5000)
    X = vectorizer.fit_transform([text])
    
    feature_names = vectorizer.get_feature_names_out()
    avg_tfidf = X.mean(axis=0).A1
    sorted_indices = avg_tfidf.argsort()[-num_keywords:][::-1]
    
    top_keywords = [feature_names[i] for i in sorted_indices]
    
    return top_keywords

def generate_combinations(keywords, num_combinations=2):
    return [' '.join(combo) for combo in combinations(keywords, num_combinations)]

def queries(combinations, context_terms):
    search_queries = []
    
    for combo in combinations:
        for term in context_terms:
            search_queries.append(f"{combo} {term}")
    return search_queries

#def summarize_text(text):
    #summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    #summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    #return summary[0]['summary_text']
    




file = '9-PREDICATE LOGIC V2.pdf'
text = extract(file)
tokens = tokenize(text)
words = keywords(tokens)
keyword_combinations = generate_combinations(words, num_combinations=2)
terms = ['AI', 'Machine Learning']
search = queries(keyword_combinations, terms)
#summary = summarize_text(text)

#print(summary)



