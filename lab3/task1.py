import re

# Sample text variable with 5 sentences
text = """This is a text variable for analysis. In this text, we will search for words.
          Some words start with vowels, others with consonants. We will also determine the word count in the text.
          Finally, we will try replacing one word with a surname."""

# a. Count the number of words in the text
word_count = len(re.findall(r'\b\w+\b', text))

# b. Find words that start with a vowel and their count
vowel_words = re.findall(r'\b[AEIOUYaeiouy]\w*\b', text)
vowel_word_count = len(vowel_words)

# c. Find words that start with a consonant
consonant_words = re.findall(r'\b[^AEIOUYaeiouy\s]\w*\b', text)

# d. Choose three words and find their positions
sample_words = ["text", "analysis", "consonants"]
sample_positions = {word: [m.start() for m in re.finditer(r'\b' + word + r'\b', text)] for word in sample_words}

# e. Replace a word in the text with the surname "Hudz"
modified_text = re.sub(r'\bvariable\b', "Hudz", text)

# Display the results
print(word_count, vowel_words, vowel_word_count, consonant_words, sample_positions, modified_text)
