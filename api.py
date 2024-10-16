import os
import requests
import PyPDF2
from docx import Document
import win32com.client  # Only works on Windows for .doc files

# Set your Azure OpenAI credentials
AZURE_OPENAI_API_KEY = "aa742488a7984f4cbc2dddf01b5699ed"
AZURE_OPENAI_ENDPOINT = "https://minihackathon06.openai.azure.com/openai/deployments/gpt-4/chat/completions?api-version=2024-08-01-preview"

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text() + '\n'  # Adding a newline for better readability
    return text.strip()  # Remove leading/trailing whitespace

# Function to extract text from a .docx file
def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text.strip()

# Function to extract text from a .doc file (Windows only)
def extract_text_from_doc(doc_path):
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    doc = word.Documents.Open(doc_path)
    text = doc.Content.Text
    doc.Close()
    word.Quit()
    return text.strip()

# Paths to the resume and job description files
resume_path = r'C:\Users\user\Desktop\misc\Uni work\year 3\Sem 1\hackathon\code\pythonProject\resumes\CCHHTT_Java Developer.docx'  # Update this to your resume file path
job_description_path = r'C:\Users\user\Desktop\misc\Uni work\year 3\Sem 1\hackathon\code\pythonProject\job descriptions\Associate Software Developer in Test.docx'  # Update this to your job description file path

# Determine the file types and extract text accordingly
if resume_path.endswith('.pdf'):
    resume_text = extract_text_from_pdf(resume_path)
elif resume_path.endswith('.docx'):
    resume_text = extract_text_from_docx(resume_path)
elif resume_path.endswith('.doc'):
    resume_text = extract_text_from_doc(resume_path)
else:
    raise ValueError("Unsupported resume file format!")

if job_description_path.endswith('.pdf'):
    job_description = extract_text_from_pdf(job_description_path)
elif job_description_path.endswith('.docx'):
    job_description = extract_text_from_docx(job_description_path)
elif job_description_path.endswith('.doc'):
    job_description = extract_text_from_doc(job_description_path)
else:
    raise ValueError("Unsupported job description file format!")

# Create the prompt for the API
prompt = f"""You are an AI assistant that analyzes resumes and matches them with job descriptions.

Job Description: {job_description}

Resume: {resume_text}

Please analyze the resume and provide a match score (0-100), along with a brief explanation of why the resume is a good or bad fit for the job description.
"""

# Prepare the request payload
headers = {
    "Content-Type": "application/json",
    "api-key": AZURE_OPENAI_API_KEY
}

data = {
    "messages": [
        {"role": "user", "content": prompt}
    ],
    "temperature": 0.7,
    "max_tokens": 150
}

# Make the API request
response = requests.post(AZURE_OPENAI_ENDPOINT, headers=headers, json=data)

# Check for a successful response
if response.status_code == 200:
    # Extract and print the result
    result = response.json()
    message = result['choices'][0]['message']['content']
    print("Analysis Result:\n", message)
else:
    print("Error:", response.status_code, response.text)
