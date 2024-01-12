''' 
file_handler Module for Employ Ease

This module is responsible for handling all file operations for the Employ Ease application.

Key Functionalities:
- File Organization: Log files and transcripts are organized under specific directories, ensuring easy accessibility and review.
- File Reading/Writing: Reads and writes to files from the file system.
- Ability to parse different file types: Supports txt, json, pdf, doc, and docx files.

Author: Courtney Palmer
'''

#region Imports
import os
import json
import PyPDF2
import configparser
import docx
import textract
#endregion

#region Definitions
def create_empty_ini_file(filepath, filename):
    if not os.path.exists(filepath):
        # Create a new config parser object
        config = configparser.ConfigParser()
        match filename:
            case "config.ini":
                # Add sections and settings
                config['Communication'] = {'APIKey': 'Your API Key Here'}
                config.set('Settings', '; 0 = False, 1 = True')
                config.set('Settings', '; If you want ChatGPT to load your Resume, Job Description, and Company Description on launch, set this to 1')
                config['Settings'] = {
                    'load_on_launch': '0',
                }
                config.set('filepaths_to_load_on_launch', '; If you want ChatGPT to load your Resume, Job Description, and Company Description on launch, ensure that load_on_launch is set to 1')
                config.set('filepaths_to_load_on_launch', '; Supported filetypes are: TXT, PDF, JSON, DOC, and DOCX')
                config['filepaths_to_load_on_launch'] = {
                    'resume_path': 'C:/your/path/to/resume.txt',
                    'job_path': 'C:/your/path/to/job_description.txt',
                    'company_path': 'C:/your/path/to/company_description.txt',
                }
                config['Theme'] = {
                    'os_color': 'green',
                    'user_color': 'violet',
                    'bot_color': 'bright_cyan',
                    'comment': "Any colour that is valid for within 'rich' library is valid here.",
                    'comment2': 'See the list of colours here: https://rich.readthedocs.io/en/latest/appendix/colors.html'
                }
            case "single_source_of_truth.ini":
                config['application'] = {
                    'job_name': '',
                    'job_description': '',
                    'company_name': '',
                    'company_description': '',
                    'company_website': '',
                }
                config['candidate'] = {
                    'resume': ''
                }
            case "prompts.ini":
                config['Job Description'] = {
                    '1': "Provide a brief summary of <company_name> job description for <job_name>.",
                    '2': "Identify the main keywords in <company_name> job description for <job_name>.",
                    '3': "Provide me with a detailed outline of the core responsibilities, qualifications, and skills required in in <company_name> job description for <job_name>.",
                    '4': "Using the provided job description, give me a list of 10 skills I should highlight on my resume."
                    }
                config['Resume'] = {
                    '1': "Tailor my resume to the job description for <job_name>.",
                    '2': "What can I do to make my resume stand out from other candidates for <job_name>?",
                    '3': "What are the most important skills I should highlight on my resume for <job_name>?",
                    '4': "What are the most important keywords for applicant tracking systems to include in my resume based on <company_name>s job description for <job_name>?"
                    }
                config['Cover Letter'] = {
                    '1': "Provide a brief summary of <company_name> job description for <job_name>.",
                    '2': "Identify the main keywords in <company_name> job description for <job_name>.",
                    '3': "How can I start my cover letter in a way that grabs the hiring managers attention?",
                    '4': "Given the company description that I provided earlier, tell me you know about the company <company_name>. How can I use this information to enhance my cover letter?"
                    }
                config['Interview'] = {
                    '1': "You are an interviewer for the role of <job_name>. Can you come up with 3-5 interview questions based on this job description for <job_name>?",
                    '2': "What are some common interview questions I should prepare for?",
                    '3': "What are some questions I should ask during my interview with <company_name>?",
                    '4': "Ask me a series of interview questions for the <job_name> role one question at a time. I will provide an answer. Give me feedback on my answer as if you are the hiring manager. What elements of my story stood out? What pieces were missing? Given interview best practices, what did I do well, and what could I do differently?"
                    }
                config['Job Offer Negotiations'] = {
                    '1': "Can you help me research the average salary and benefits for the role of <job_name>?",
                    '2': "What are effective negotiation techniques for job offers for the role of <job_name>?",
                    '3': "What are the most important things to consider when negotiating a job offer for the <job_name> role?",
                    '4': "How can I negotiate a higher salary without coming off as demanding?"
                    }
                
        with open(filepath + f"\\{filename}", 'w') as configfile:
            config.write(configfile)   

def read_file_content(filepath):
    ''' Reads the content of a file based on its type. Supported file types include txt, json, pdf, doc, and docx.
    
    filepath: the path to the file to read
    return: the content of the file
    '''
    # Check if file exists
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"The file {filepath} does not exist.")

    # Extract file extension
    _, file_extension = os.path.splitext(filepath)

    try:
        if file_extension == '.txt':
            return read_text_file(filepath)
        elif file_extension == '.json':
            return read_json_file(filepath)
        elif file_extension == '.pdf':
            return read_pdf_file(filepath)
        elif file_extension == '.docx':
            return read_docx_file(filepath)
        elif file_extension == '.doc':
            return read_doc_file(filepath)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}. Please try a txt, json, pdf, doc, or docx file instead.")

    except Exception as e:
        raise e

def read_text_file(filepath):
    ''' Opens a file and returns the content.
    
    filepath: the path to the file to open
    return: the content of the txt file
    '''
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def read_json_file(filepath):
    ''' Reads the contents of a JSON file.
    
    filepath: the path to the JSON file to load
    return: the contents of the JSON file
    '''
    with open(filepath, 'r', encoding='utf-8') as infile:
        return json.load(infile)

def read_doc_file(filepath):
    ''' Reads content from a DOC file. 
    
    filepath: the path to the DOC file to read
    return: the text extracted from the DOC file
    '''
    return textract.process(filepath).decode('utf-8')
      
def read_pdf_file(filepath):
    ''' Reads a PDF file and returns the text.
    
    filepath: the path to the PDF file to read
    return: the text extracted from the PDF file
    '''
    pdf_text = ""
    with open(filepath, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            pdf_text += page.extract_text() + "\n"
    return pdf_text

def read_docx_file(filepath):
    ''' Reads content from a DOCX file. 
    
    filepath: the path to the DOCX file to read
    return: the text extracted from the DOCX file
    '''
    doc = docx.Document(filepath)
    return '\n'.join([para.text for para in doc.paragraphs])

def create_json_file(filepath, payload):
    ''' Saves the given JSON payload to the given file.
    
    filepath: the path to the file to save
    payload: the JSON payload to save to the file
    '''
    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))
    with open(filepath, 'w', encoding='utf-8') as outfile:
        json.dump(payload, outfile, ensure_ascii=False, sort_keys=True, indent=2)

def load_ini(file_path, file_name):
    ''' Loads the given INI file.
    
    file_name: the name of the ini file to load
    return: the configparser object
    '''
    # Check if file exists
    if not os.path.exists(f"{file_path}\\{file_name}"):
        create_empty_ini_file(os.getcwd(), file_name)
    parser = configparser.ConfigParser()
    parser.read(f"{file_path}\\{file_name}")
    return parser
#endregion
