import os
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import PyPDF2
import io
from docx import Document

# File containing the list of URLs
urls_file = r""
output_file = r""

# Create the output directory if it doesn't exist
os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(urls_file, "r") as file, open(output_file, "w", encoding="utf-8") as text_file:
    for idx, url in enumerate(file.readlines(), start=1):
        url = url.strip()
        text_file.write(f"\n\n******************************{idx}******************************\n\n")
        try:
            if url.endswith(".pdf"):
                # Handle PDF URL
                response = requests.get(url, verify=False)  # Disable SSL verification
                pdf_file = io.BytesIO(response.content)
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                pdf_text = ""
                for page in pdf_reader.pages:
                    pdf_text += page.extract_text() if page.extract_text() else ""
                text_file.write(pdf_text)
            elif url.endswith(".docx"):
                # Handle DOCX URL
                response = requests.get(url, verify=False)  # Disable SSL verification
                docx_file = io.BytesIO(response.content)
                doc = Document(docx_file)
                doc_text = "\n".join([para.text for para in doc.paragraphs])
                text_file.write(doc_text)
            else:
                # Handle HTML URL
                response = requests.get(url, verify=False)  # Disable SSL verification
                soup = BeautifulSoup(response.content, features="html.parser")

                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.extract()

                # Get text
                text = soup.get_text()

                # Break into lines and remove leading and trailing space on each
                lines = (line.strip() for line in text.splitlines())
                # Break multi-headlines into a line each
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                # Drop blank lines
                text = '\n'.join(chunk for chunk in chunks if chunk)

                text_file.write(text)
        except Exception as e:
            text_file.write(f"Failed to process URL {url} due to {e}\n")
