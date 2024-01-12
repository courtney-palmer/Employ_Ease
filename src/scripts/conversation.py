''' 
Conversations Module for Employ Ease

This module, part of the Employ Ease application, is responsible for handling all interactions with ChatGPT. It facilitates the communication process, manages conversation history, and ensures seamless integration of ChatGPT's capabilities into the application. 

Key Functionalities:
- Communication with ChatGPT: Sends user inputs to ChatGPT and retrieves responses, both with and without contextual information.
- Conversation History Management: Maintains a detailed record of conversations, storing them in a structured JSON format.
- User Interaction: Handles user inputs for updating application-specific information like resumes, job descriptions, and company details.

Author: Courtney Palmer
'''

#region imports
import sys
import os
from time import time
from uuid import uuid4
import requests
from rich.console import Console
import re
from src.scripts.logger import create_new_memory_file, create_new_transcript, append_transcript
from src.scripts.single_source_of_truth import single_source_of_truth
from src.scripts.memory import fetch_memories, summarize_memories, gpt3_embedding, timestamp_to_datetime, get_last_messages, load_convo
from src.scripts.file_handler import load_ini, read_file_content
#endregion

#region Definitions
def themed_print(message, theme = "bold green"):
    ''' Prints a message to the console in a themed style
    
    message: The message to print
    theme: The theme to use
    '''

    # If the theme is not in the dictionary, set the theme to the default theme
    if theme not in themes:
        theme = "bold " + themes["os_color"]
    else :
        theme = "bold " + themes[theme]

    console = Console()
    console.print(message, style = theme, highlight=False)

def send_prompt(prompt, session_timestamp):
    '''
    Sends a prompt to ChatGPT and returns the response.
    
    prompt: The prompt to send to ChatGPT.
    session_timestamp: The timestamp of the current session.
    '''
    # Create a transcript file if one does not exist
    if not os.path.exists(os.getcwd() + f"\\logs\\Session_{session_timestamp}\\Transcript.txt"):
        create_new_transcript(session_timestamp)
       
    console = Console()
    with console.status(
          themed_print(f"User: {prompt}...", "user_color"),
          spinner="aesthetic",
          speed=1,
          spinner_style="green",
    ):

        user_prompt_vector = save_message(prompt, session_timestamp, "User")[0]
        user_prompt_with_context = get_conversation(session_timestamp, user_prompt_vector)
        bot_response_message = save_message(user_prompt_with_context, session_timestamp, "EmployEase")[1]
        return bot_response_message

def save_message(user_prompt, session_timestamp, speaker):
    '''Takes a user prompt, sends it to ChatGPT, and saves the response to a json file.
    
    user_prompt: The user's message to send to ChatGPT.
    session_timestamp: The timestamp of the current session.
    speaker: The speaker of the message (either "User" or "EmployEase").
    returns: A list containing the vector representation of the message and the message text itself.
    '''
    # First, distinguish between the user (who sends a prompt), and the bot (who responds to the prompt).
    # Check if the speaker is the user. If so, record the user prompt info to a JSON file.
    # Otherwise, the speaker is our chatgpt bot. We must first send the user prompt to ChatGPT for a response. Then, record the response info to a JSON file.
    content = ""
    if speaker == "User":
        content = user_prompt
    else:
        bot_response = send_message(user_prompt)
        content = bot_response

    # set vector, msg_timestamp, msg_timestring, and message for the 'info' dictionary
    vector = gpt3_embedding(content)
    msg_timestamp = time()
    msg_timestring = timestamp_to_datetime(msg_timestamp)
    message = content
    info = {'speaker': f'{speaker}', 'time': msg_timestamp, 'vector': vector, 'message': message, 'uuid': str(uuid4()), 'timestring': msg_timestring}

    create_new_memory_file(session_timestamp, speaker, msg_timestamp, info)
    append_transcript(f"{speaker}: {content}", session_timestamp)
    
    if speaker != "User":
        themed_print(f"\n{speaker}: {content}", "bot_color")

    prompt_vector_and_text = [vector, content]

    return prompt_vector_and_text

def send_message(message):
    '''
    Sends a message to ChatGPT and returns the response.
    '''
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {APIKey}'
    }

    data = {
        'model': "gpt-3.5-turbo-1106",
        'messages': [{'role': 'system', 'content': 'You are a helpful assistant for active job hunters.'},
                     {'role': 'user', 'content': message}]
    }

    api_url = 'https://api.openai.com/v1/chat/completions'
    response = requests.post(api_url, headers=headers, json=data, timeout=60)
    response_json = response.json()
    return response_json['choices'][0]['message']['content']

def get_conversation(session_timestamp, vector):
    ''' Gets the conversation from the current session, and returns a prompt for the bot to respond to.
    
    session_timestamp: The timestamp of the current session.
    vector: The vector representation of the user's message.
    '''

    conversation = load_convo(f"Session_{session_timestamp}")
    memories = fetch_memories(vector, conversation, 5)
    notes = ""
    if memories != []:
        notes = summarize_memories(memories)
    recent = get_last_messages(conversation, 4)
    prompt = f"I am a chatbot named EmployEase. My goals are to increase user success rate in securing job offers. I will read the conversation notes and recent messages, and then I will provide an answer. The following are notes from earlier conversations with USER: {notes} The following are the most recent messages in the conversation: {recent} I will now provide a response. EmployEase: "
    return prompt

def is_file_path(input_string):
    '''Heuristic function to check if the input string is likely a file path.

    input_string: The input string to check.
    returns: True if the input string resembles a file path, False otherwise.
    '''
    # Regular expression for common file extensions
    file_extension_pattern = r'\.[a-zA-Z0-9]+$'

    # Check for presence of path separators and a file extension pattern
    if ('/' in input_string or '\\' in input_string) and re.search(file_extension_pattern, input_string):
        # Additional check for the existence of directories in the path
        directory_path = os.path.dirname(input_string)
        if os.path.exists(directory_path):
            return True
    return False

def request_filepath_or_text(content_name):
    themed_print(f"Please provide the new {content_name} for your job application. Enter ctrl-d or ctrl-z to finish")
    user_input = sys.stdin.read()   # Use Ctrl d or ctrl z to stop the input

    if is_file_path(user_input) and os.path.exists(user_input):
        # Attempt to read file content
        file_content = read_file_content(user_input)
        if file_content is not None:
            return file_content
        else:
            themed_print("Treating the input as direct text due to file reading error.", "Info")

    # Treating the input as direct text
    return user_input.encode(encoding='ASCII', errors='ignore').decode()

def prime_information(session_timestamp, info_type, filepath=""):
    '''Primes ChatGPT with information about the user's resume, company description, or job description.
    
    session_timestamp: The timestamp of the current session.
    info_type: Type of information to prime ('resume', 'company', 'job').
    filepath: The file path to the information file.
    '''
    new_info = ""
    if filepath != "":
        new_info = read_file_content(filepath)
    else:
        new_info = request_filepath_or_text(info_type)

    if new_info is None:
        return

    send_prompt(f"Your goal is to remember the contents of this {info_type} for future questioning:\n{new_info}", session_timestamp)

    if info_type == 'company':
        new_company_name = send_prompt(f"Given the company description, tell me the company name. Do not provide any other text:\n{new_info}", session_timestamp)
        if new_company_name is not None:
            company_website = send_prompt(f"Provide me the website for the company {new_company_name}. Do not provide any other text", session_timestamp)
        single_source_of_truth.update_ssot_ini_info(application_company_description=new_info, 
                         application_company_name=new_company_name, 
                         application_company_website=company_website)

    elif info_type == 'job':
        new_job_name = send_prompt(f"Given the job description, provide the job title. Do not provide any other text:\n{new_info}", session_timestamp)
        single_source_of_truth.update_ssot_ini_info(application_job_description=new_info, 
                         application_job_name=new_job_name)

    elif info_type == 'resume':
        single_source_of_truth.update_ssot_ini_info(candidate_resume=new_info)

def prime_chatgpt(session_timestamp, new_config):
    '''Primes ChatGPT with information about the user's resume, the job description, and the company description.
    Use the filepaths provided in config.ini to retrieve the information.
    
    session_timestamp: The timestamp of the current session.
    new_config: The config object to retrieve the file paths from.
    '''
    resume_path = new_config.get('filepaths_to_load_on_launch', 'resume_path')
    job_path = new_config.get('filepaths_to_load_on_launch', 'job_path')
    company_path = new_config.get('filepaths_to_load_on_launch', 'company_path')
    prime_information(session_timestamp,"resume", resume_path)
    prime_information(session_timestamp, "company", company_path)
    prime_information(session_timestamp, "job", job_path)
#endregion

#region Global Variables
config_object = load_ini(os.getcwd(), "config.ini")
APIKey = config_object.get('Communication', 'APIKey')

# Create a dictionary of themes in the format {themeName: theme}
# load themes from config.ini, append them to the themes dictionary
themes = {
    "Error": "bold red",
    "Warning": "bold yellow",
    "Info": "bold blue",
    "Success": "bold green"
    }
for (each_key, each_val) in config_object.items('Theme'):
    themes[each_key] = each_val
#endregion
