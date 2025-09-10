import re

# Given text variable with 6 words
text = "This is a simple textb example"

# Remove spaces to get a list of characters without spaces
characters = re.findall(r'\S', text)

# Get the first two letters of each word
first_two_letters = [word[:2] for word in re.split(r'\s+', text)]

# Create a new list excluding characters 'a' and 'b'
filtered_characters = [char for char in characters if char.lower() not in ['a', 'b']]

# Display the results
print("Characters without spaces:", characters)
print("First two letters of each word:", first_two_letters)
print("Filtered characters (excluding 'a' and 'b'):", filtered_characters)

