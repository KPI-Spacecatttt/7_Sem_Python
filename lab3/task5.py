import re

# Sample text with sequences of numbers, some with repeated digits
text = "333334 555 5555 123 2334 55555 55678 3455 755"

# Use regular expressions to find numbers with sequences of the digit '5' in lengths of 2 or 3
matching_numbers = re.findall(r'\b\d*5{2,3}\d*\b', text)

# Display the matching numbers
print(matching_numbers)