import os
import json
import requests
import PyPDF2

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

# Sample job description
job_description = """
Software Engineer
We are looking for a software engineer with experience in software development, problem-solving skills, and familiarity with programming languages like Python and Java.
"""

# Path to the resume PDF
pdf_resume_path = 'path_to_your_resume.pdf'  # Update this to your PDF file path

# Extract text from the PDF resume
resume_text = extract_text_from_pdf(r"C:\Users\user\Desktop\misc\Uni work\year 3\Sem 1\hackathon\code\pythonProject\resumes\Anna.pdf")

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
