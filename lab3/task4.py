import re

# Sample string with email addresses and their owners
text = "John Doe <john.doe@example.com>, Jane Smith <jane.smith@company.org>, Bob Brown <bob.brown@service.net>"

# Extract domains from email addresses using regex
domains = re.findall(r'@([\w\.-]+)', text)

# Display the list of domains
print(domains)
