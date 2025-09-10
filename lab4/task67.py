import nltk
import matplotlib.pyplot as plt
from nltk.corpus import gutenberg

# Download necessary resources if not already available
nltk.download('gutenberg')
nltk.download('punkt')

# Load the text of Shakespeare's "Hamlet" from the Gutenberg library
hamlet_text = nltk.Text(gutenberg.words('shakespeare-hamlet.txt'))

# Task 6: Plotting word distribution
target_words = ['Hamlet', 'Horatio', 'Ghost', 'Polonius']
hamlet_text.dispersion_plot(target_words)
plt.show()

# Words that occur only once
freq_dist = nltk.FreqDist(hamlet_text)
hapaxes = freq_dist.hapaxes()
print(f"Number of hapaxes: {len(hapaxes)}")
print("List of hapaxes:", hapaxes[:10])  # Display first 10 hapaxes for brevity

# Word length distribution
word_lengths = [len(word) for word in hamlet_text if word.isalpha()]
length_freq_dist = nltk.FreqDist(word_lengths)

# Most common word length
most_common_length = length_freq_dist.max()
print(f"Most common word length: {most_common_length}")

# Plot word length frequency distribution
plt.figure(figsize=(12, 6))
length_freq_dist.plot(18)
plt.title("Word Length Distribution in Hamlet")
plt.xlabel("Word Length")
plt.ylabel("Frequency")
plt.savefig("hamlet_word_length_distribution.png")
plt.show()
