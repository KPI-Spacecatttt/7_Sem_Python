import re

# Text string with programming languages and some non-language words
text = "Python, 123, Java, C++, programming, JavaScript, Ruby!, Swift, Kotlin, PHP, Go, Rust, TypeScript, 456, randomWord"

# Regex pattern with a broader match for typical programming language structures
# This filters out words with a generic format but avoids matching common English terms
languages = re.findall(r'\b[A-Z][A-Za-z]*\b', text)

# Display the result
print(languages)
