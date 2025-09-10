import re

# Sample string with time and date in full format
text = "The meeting was scheduled at 14:30:25 on 2023-10-15, and another event at 09:15:45 on 2021-05-23."

# Extract time and date in full format using regex
time_date_list = re.findall(r'(\d{2}:\d{2}:\d{2}) on (\d{4}-\d{2}-\d{2})', text)

# Extract hours and years separately
hours = [match[0][:2] for match in time_date_list]  # Get the hours part from time
years = [match[1][:4] for match in time_date_list]  # Get the year part from date

# Display results
print(time_date_list, hours, years)
