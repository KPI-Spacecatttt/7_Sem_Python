import string

import nltk
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize

# necessary NLTK data packages are downloaded
nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("averaged_perceptron_tagger")
nltk.download("averaged_perceptron_tagger_eng")

# Sample text in English with at least 5 sentences
text = """
    Artificial Intelligence (AI) is transforming the world. Machines are learning to perform tasks that typically require human intelligence.
    For instance, image recognition and language processing are becoming increasingly advanced. AI also has the potential to revolutionize healthcare.
    The development of AI raises many ethical concerns, especially about privacy and job displacement. In the future, AI might be used in ways we can not even imagine today.
    """

# Step 1: Tokenize by sentences
sentences = sent_tokenize(text)

# Step 2: Tokenize by words and remove punctuation and stop words
words = word_tokenize(text)
filtered_words = [
    word
    for word in words
    if word.lower() not in stopwords.words("english") and word not in string.punctuation
]

# Step 3: Part-of-Speech (POS) tagging
pos_tags = pos_tag(filtered_words)

# Display results for each step
print("Tokenized Sentences:", sentences)
print("Filtered Words (No Stopwords, No Punctuation):", filtered_words)
print("POS Tags:", pos_tags)

# Analysis
# Count the number of words in each sentence
sentence_word_counts = [len(word_tokenize(sentence)) for sentence in sentences]

# Count the number of stopwords in the text
stop_words_count = len(
    [word for word in words if word.lower() in stopwords.words("english")]
)

# Find the longest word in the filtered words list
longest_word = max(filtered_words, key=len)

# Count the words in the text that contain exactly 4 characters
four_char_words_count = len([word for word in filtered_words if len(word) == 4])

# Display results for each step and analysis
print("Word Counts per Sentence:", sentence_word_counts)
print("Number of Stopwords in Text:", stop_words_count)
print("Longest Word:", longest_word)
print("Number of 4-Character Words:", four_char_words_count)

# Initialize stemmer and lemmatizer
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

# Apply stemming
stemmed_words = [stemmer.stem(word) for word in filtered_words]

# Apply lemmatization
lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_words]

# Display results
print("Stemmed Words:", stemmed_words)
print("Lemmatized Words:", lemmatized_words)
