import re
import xml.etree.ElementTree as ET
import requests

# Define the regular expression for URL matching
url_rgx = re.compile(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')

# Load the XML file and parse it
xml_file_path = r""
tree = ET.parse(xml_file_path)
root = tree.getroot()

# Extract the text content from the XML
text_content = ''.join(root.itertext())

# Find all matches for URLs
matches = re.findall(url_rgx, text_content)

# Ensure 'http://' is present if missing
urls = ['http://%s' % url[0] if not url[0].startswith('http') else url[0] for url in matches]

def check_url(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        if response.status_code < 400:
            return True
        else:
            return False
    except requests.RequestException:
        return False

# Check each URL and filter out the valid ones
valid_urls = [url for url in urls if check_url(url)]

# Save valid URLs to a text file
output_file_path = r''
with open(output_file_path, 'w') as file:
    for url in valid_urls:
        file.write(url + '\n')

print("Valid URLs (kept in the file):")
for url in valid_urls:
    print(url)
