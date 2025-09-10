import re

import nltk
import stanza
from nltk.tokenize import word_tokenize
from uk_stemmer import UkStemmer

# necessary NLTK data packages are downloaded
nltk.download("punkt")

# Читання текстового файлу
with open("lab3/text_ukrainian.txt", "r", encoding="utf-8") as file:
    text = file.read()

# Читання файлу зі стоп-словами
with open("lab3/stop_words_ukrainian.txt", "r", encoding="utf-8") as stop_file:
    stop_words = set([line.strip() for line in stop_file])

# Токенізація тексту за словами та видалення розділових знаків
words = word_tokenize(text)
words_cleaned = [re.sub(r"[^\w\s]", "", word) for word in words if word not in ",.!?"]

# Видалення стоп-слів
filtered_words = [word for word in words_cleaned if word.lower() not in stop_words]

# Стемінг
stemmer = UkStemmer()
stemmed_words = [stemmer.stem_word(word) for word in filtered_words]

# Apply lemmatization
filtered_text = " ".join(filtered_words)
stanza.download("uk")
nlp = stanza.Pipeline("uk")
doc = nlp(filtered_text)
lemmatized_words = [word.lemma for sentence in doc.sentences for word in sentence.words]


# Збір статистики
input_text_length = len(words)
punctuation_count = len([word for word in words if word in ",.!?"])
stop_words_count = len([word for word in words_cleaned if word.lower() in stop_words])
output_text_length = len(filtered_words)

# Вивід результатів
print("Original Text Length (Word Count):", input_text_length)
print("Number of Punctuation Marks:", punctuation_count)
print("Number of Stop Words:", stop_words_count)
print("Word Count After Stop Words Removal:", output_text_length)
print("Filtered Words:", filtered_words)
print("Stemmed Words:", stemmed_words)
print("Lemmatized Words:", lemmatized_words)
