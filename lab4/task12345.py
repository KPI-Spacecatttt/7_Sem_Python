import math
import re

import matplotlib.pyplot as plt
import pandas as pd

# English text with 4 sentences (varying word counts and some repeated words)
english_text = """Machine learning is a fascinating field of artificial intelligence that focuses on building systems capable of learning and improving automatically from experience.
Artificial intelligence and machine learning are closely related but not identical concepts, as machine learning is a subset of artificial intelligence.
The goal of machine learning is to develop algorithms that can process large datasets, recognize patterns, and make decisions without human intervention.
Learning from data is the core principle of machine learning, and it enables systems to improve their performance over time with minimal human involvement.
"""

# Step 1: Bag of Words
unique_words_english = sorted(set(re.findall(r"\b\w+\b", english_text.lower())))
print("Unique words (Bag of Words):")
print(unique_words_english, "\n")

# Tokenizing the English text into individual documents (sentences)
tokenized_docs = [
    re.findall(r"\b\w+\b", sentence.lower())
    for sentence in english_text.split(".")
    if sentence.strip()
]
print("Tokenized documents:")
print(tokenized_docs, "\n")

# Step 2: Term Frequency (TF) for each word in each document
tf = []
for doc in tokenized_docs:
    total_words_in_doc = len(doc)
    tf.append(
        {word: doc.count(word) / total_words_in_doc for word in unique_words_english}
    )
print("TF (Term Frequency):")
print(tf, "\n")

# Step 3: Inverse Document Frequency (IDF) for each word
num_docs = len(tokenized_docs)
idf = {}
for word in unique_words_english:
    doc_count = sum(1 for doc in tokenized_docs if word in doc)
    idf[word] = math.log(
        num_docs / (1 + doc_count)
    )  # Adding 1 to avoid division by zero
print("IDF (Inverse Document Frequency):")
print(idf, "\n")

# Step 4: TF-IDF calculation for each word in each document
tf_idf = []
for doc_tf in tf:
    tf_idf.append({word: doc_tf[word] * idf[word] for word in unique_words_english})

# Displaying results in DataFrame
results = pd.DataFrame(tf_idf, index=[f"Document {i + 1}" for i in range(num_docs)])
print("TF-IDF matrix:")
print(results, "\n")

# Step 5: Plot TF-IDF for each document
for i, doc in enumerate(tf_idf):
    plt.figure(figsize=(12, 6))
    plt.bar(unique_words_english, doc.values(), color="skyblue")
    plt.title(f"TF-IDF Scores for Document {i + 1}")
    plt.xlabel("Words")
    plt.ylabel("TF-IDF Score")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
