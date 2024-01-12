''' 
logger Module for Employ Ease

This module is responsible for handling all logging functionalities of the Employ Ease application. It ensures that various types of logs are systematically created and maintained.

Key Functionalities:
- Log File Management: Creates and maintains log files for different types of data, organized by session timestamps.
- Transcript Creation: Generates a transcript file for each session, which records the detailed conversation history for user review.
- File Organization: Log files and transcripts are organized under specific directories, ensuring easy accessibility and review.

Author: Courtney Palmer
'''

import os
from src.scripts.file_handler import create_json_file

#region Definitions
def create_new_memory_file(session_timestamp, speaker, msg_timestamp, info):
    ''' Creates a new memory file at logs/Session_{session_timestamp}/{speaker}Log_{msg_timestamp}.json
    
    session_timestamp: the time stamp of the session
    speaker: the speaker of the message
    msg_timestamp: the time stamp of the message
    info: the information to save to the memory file
    '''  
    filepath_to_session_memory = os.getcwd() + f"\\src\\internal\\memory\\Session_{session_timestamp}"
    create_json_file(f"{filepath_to_session_memory}\\{speaker}Log_{msg_timestamp}.json", info)

def create_new_transcript(session_timestamp):
    ''' Creates a new transcript file at logs/Session_{session_timestamp}/Transcript.txt
    
    session_timestamp: the time stamp of the session
    '''
    # check if logs folder exists
    if not os.path.exists(os.getcwd() + "\\logs"):
        os.mkdir(os.getcwd() + "\\logs")
    # check if session folder exists
    if not os.path.exists(os.getcwd() + f"\\logs\\Session_{session_timestamp}"):
        os.mkdir(os.getcwd() + f"\\logs\\Session_{session_timestamp}")
    # Create a new transcript file at logs/Session_{session_timestamp}/Transcript.txt
    log_file = os.getcwd() + f"\\logs\\Session_{session_timestamp}\\Transcript.txt"
    with open(log_file, "w", encoding = 'utf-8') as f:
        f.write("TRANSCRIPT FILE\n")

def append_transcript(message, session_timestamp):
    ''' Appends the given message to the current transcript file.
    
    message: the message to append to the transcript file
    session_timestamp: the time stamp of the session
    '''
    message = message.encode('utf-8', 'ignore')
    with open(os.getcwd() + f"\\logs\\Session_{session_timestamp}\\Transcript.txt", "a", encoding = 'utf-8') as f:
        f.write("="*80)
        f.write(f'\n{message}\n')
#endregion
