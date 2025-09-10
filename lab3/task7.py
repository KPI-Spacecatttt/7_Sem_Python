import re

def is_valid_ukrainian_postal_code(postal_code):
    # Regular expression pattern for a 5-digit postal code
    pattern = r'^\d{5}$'
    # Check if postal code matches the pattern
    return bool(re.match(pattern, postal_code))

# Example usage
postal_code = input("Enter a Ukrainian postal code: ")
if is_valid_ukrainian_postal_code(postal_code):
    print("The postal code is valid.")
else:
    print("The postal code is invalid.")