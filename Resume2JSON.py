import os
import json
import PyPDF2
from docx import Document
import pythoncom
import win32com.client as win32


# Function to extract text from PDF
def extract_pdf_text(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page].extract_text()
    return text


# Function to extract text from DOCX
def extract_docx_text(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])


# Function to extract text from DOC
def extract_doc_text(file_path):
    pythoncom.CoInitialize()
    word = win32.Dispatch("Word.Application")
    word.Visible = False

    try:
        doc = word.Documents.Open(file_path)
        text = doc.Content.Text  # Extract all text from the document
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        text = ""
    finally:
        doc.Close(False)
        word.Quit()

    return text


# Function to extract text from TXT
def extract_txt_text(file_path):
    with open(file_path, 'r') as file:
        return file.read()


# Function to format the extracted content into JSON structure
def format_into_json(content, query):
    json_structure = {
        "messages": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You are an AI assistant that helps people find information."
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": content  # Resume content here
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": query  # Query provided by the user
                    }
                ]
            }
        ],
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 800
    }
    return json_structure


# Function to clear the output directory of all files
def clear_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")


# General function to process files and convert them into structured JSON
def convert_resumes_to_json(input_directory, output_directory, query):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    else:
        # Clear the output directory if it already exists
        clear_directory(output_directory)

    for filename in os.listdir(input_directory):
        file_path = os.path.join(input_directory, filename)
        if filename.endswith('.pdf'):
            text = extract_pdf_text(file_path)
        elif filename.endswith('.docx'):
            text = extract_docx_text(file_path)
        elif filename.endswith('.doc'):
            text = extract_doc_text(file_path)
        elif filename.endswith('.txt'):
            text = extract_txt_text(file_path)
        else:
            print(f"Unsupported file format: {filename}")
            continue

        # Format the resume content into the required JSON structure
        formatted_json = format_into_json(text, query)

        # Create the output JSON path in the new folder
        json_file_name = f"{os.path.splitext(filename)[0]}.json"
        json_path = os.path.join(output_directory, json_file_name)

        # Write the structured JSON file to the specified output directory
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(formatted_json, json_file, ensure_ascii=False, indent=4)


# Specify the input directory containing the resumes
input_directory = r'C:\Users\user\Desktop\misc\Uni work\year 3\Sem 1\hackathon\resumes'

# Specify the output directory where JSON files will be saved
output_directory = r'C:\Users\user\Desktop\misc\Uni work\year 3\Sem 1\hackathon\ResumeJSONS'

# The query that the user would input (modify as needed)
user_query = "What skills does this person have?"

# Convert all resumes in the input directory and save them as structured JSON in the output directory
convert_resumes_to_json(input_directory, output_directory, user_query)
