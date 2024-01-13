'''
Employ Ease - Main Module

This module is the main entry point for the Employ Ease application, a Python-based console tool designed to assist job seekers. It integrates OpenAI's GPT models to provide comprehensive support during various stages of the job application process. 

Key Functionalities:
- Dynamic Menu Presentation: Displays various user options and navigational menus.
- Customized User Assistance: Processes user inputs and provides specific guidance using ChatGPT.
- Interactive Update Mechanisms: Allows users to update their job description, company description, and resume.
- General Query Handling: Offers a platform for users to ask open-ended questions for personalized advice.

The main module orchestrates the application flow, handling user inputs, displaying options, and managing conversations. It dynamically generates options based on predefined categories and questions, and interfaces with other components for specific functionalities

Usage:
To run the application, execute this script from the command line. Ensure all dependencies are installed and the necessary configuration files are in place.

Author: Courtney Palmer
'''

#region Imports
import os
from time import time
import shutil
from rich import print
from rich.panel import Panel
from rich.table import Table
from src.scripts.single_source_of_truth import single_source_of_truth
from src.scripts.conversation import send_prompt, prime_chatgpt, prime_information, themed_print
from src.scripts.file_handler import load_ini
#endregion

ssot = single_source_of_truth()

#region Definitions
def display_intro():
    '''
    Displays the intro to the user 
    '''
    header = '''
███████╗███╗   ███╗██████╗ ██╗      ██████╗ ██╗   ██╗    ███████╗ █████╗ ███████╗███████╗
██╔════╝████╗ ████║██╔══██╗██║     ██╔═══██╗╚██╗ ██╔╝    ██╔════╝██╔══██╗██╔════╝██╔════╝
█████╗  ██╔████╔██║██████╔╝██║     ██║   ██║ ╚████╔╝     █████╗  ███████║███████╗█████╗  
██╔══╝  ██║╚██╔╝██║██╔═══╝ ██║     ██║   ██║  ╚██╔╝      ██╔══╝  ██╔══██║╚════██║██╔══╝  
███████╗██║ ╚═╝ ██║██║     ███████╗╚██████╔╝   ██║       ███████╗██║  ██║███████║███████╗
╚══════╝╚═╝     ╚═╝╚═╝     ╚══════╝ ╚═════╝    ╚═╝       ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝
    '''
    
    panel = Panel(header, expand=False)
    themed_print(panel)
    print(
        '''
Employ Ease is a tool that uses ChatGPT to assist in all stages of the job application process.
This includes help with [bold yellow]Job Descriptions[/bold yellow], [bold yellow]Resumes[/bold yellow], [bold yellow]Cover Letters[/bold yellow], [bold yellow]Interviews[/bold yellow], and [bold yellow]Job Offer Negotiations[/bold yellow].
To start, select an option below.
    '''
    )

def print_menu_options(title, prompt_dict, terminal_size):
    ''' Prints the set of options for the user to choose from
    
    title: The title of the menu
    prompt_dict: The dictionary of options to choose from
    terminal_size: The width of the terminal window
    '''
    title = f" {title} "
    if "MENU" in title:
        menu_options = {}
        for index, catagory in enumerate(prompt_dict):
            index = str(index + 1)
            menu_options[index] = catagory
        menu_options["G"] = "General Questions"
        menu_options["U"] = "Update Application Info"
        menu_options["Q"] = "Exit"
        menu_as_string = str(menu_options).replace("'", "").replace(':', ' -').replace(',', '\n').replace('{', ' ').replace('}', '')
        panel = Panel(menu_as_string, title=title, expand=False)
        themed_print(panel)
    else:
        catagory_options = {}
        for key in prompt_dict:
            question = prompt_dict[key].replace('"', '')
            catagory_options[key] = f'{question},'
        catagory_options["Q"] = "Return to Main Menu"
        catagory_as_string = str(catagory_options).replace("'", "").replace(':', ' -').replace('{', ' ').replace('}', '').replace(',,', '\n')
        panel = Panel(catagory_as_string, title=title, expand=False)
        themed_print(panel)

def update_application_info(terminal_size, session_timestamp):
    ''' Provides the user with a list of options to choose from and then sends the user input to ChatGPT for a response
    
    terminal_size: The width of the terminal window
    session_timestamp: The time stamp of the session
    '''
    # create a dictionary holding the options for updating the application info

    update_options = {
        "1": "Change Job Description",
        "2": "Change Company Description",
        "3": "Change Resume",
        "4": "Change All",
        "5": "Check Contents in Memory"
    }
    user_setting_choice = ""
    while user_setting_choice != 'q':
        print_menu_options("Update Application Info", update_options, terminal_size)

        user_setting_choice = input('\nUSER: ')
        match user_setting_choice:
            case '1':
                prime_information(session_timestamp, "job")
                ssot.update_truth()
            case '2':
                prime_information(session_timestamp, "company")
                ssot.update_truth()
            case '3':
                prime_information(session_timestamp, "resume")
                ssot.update_truth()
            case '4':
                prime_information(session_timestamp, "job")
                prime_information(session_timestamp, "company")
                prime_information(session_timestamp, "resume")
                ssot.update_truth()
            case '5':
                display_contents_in_memory(ssot)
            case 'q':
                break
            case '_':
                themed_print(f"Command '{user_setting_choice}' not recognized.", "Error")

def general_questions(session_timestamp):
    ''' Allows the user to ask any question and then sends the user input to ChatGPT for a response 
    
    session_timestamp: The time stamp of the session
    '''
    user_input = ""
    themed_print("Ask me anything! Type 'q' to quit.\n")
    while True:
        user_input = input('USER: ')
        if user_input.lower() == 'q':
            break
        send_prompt(user_input, session_timestamp)
        themed_print("Done chatting? Type 'q' to quit.\n")
        
def display_contents_in_memory(ssot):
    ''' Displays the contents of the single_source_of_truth class object
    
    ssot: The single_source_of_truth class object
    '''
    attributes = {
        "Job Name": ssot.job_name,
        "Job Description": ssot.job_description,
        "Company Name": ssot.company_name,
        "Company Description": ssot.company_description,
        "Resume": ssot.resume,
        "Company Website": ssot.company_website
    }
    table = Table(show_header=True, header_style="bold white")

    table.add_column("Attribute", style="bold", width=20)
    table.add_column("Value", style="bold")

    for item in attributes:
        table.add_row(item, attributes[item].replace('"', ""))
        table.add_row("", "", end_section=True)

    panel = Panel(table, title="Contents in Memory", expand=False)
    print(panel)
#endregion

#region Main
def main():
    ''' The main entry point for the Employ Ease application 
    '''
    session_timestamp = time()
    display_intro()
    # Provide ChatGPT with the job description, company description, and resume so that this information is available in memory for all conversations
    config_object = load_ini(os.getcwd(), "config.ini")
    load_on_launch = config_object.get("Settings", "load_on_launch")
    if int(load_on_launch) == 1:
        prime_chatgpt(session_timestamp, config_object)

    # Catagories and prompte are dynamically generated from the prompts.ini file. Read prompts.ini and store the contents in a dictionary
    config_object = load_ini(f"{os.getcwd()}\\src\\internal", "prompts.ini")
    prompt_dict={s:dict(config_object.items(s)) for s in config_object.sections()}

    terminal_size = shutil.get_terminal_size().columns
    # Provide the user with a list of Menu catagories to choose from
    while True:
        print_menu_options("MENU", prompt_dict, terminal_size)
        user_catagory_choice = input('\nUSER: ')
        match user_catagory_choice:
            # Check if the user selected 'q' to quit
            case 'q':
                break
            case 'g':
                general_questions(session_timestamp)
                continue
            # Check if the user selected 'u' to go to update app info
            case 'u':
                update_application_info(terminal_size, session_timestamp)
                continue
            # Otherwise, the user should enter a number to select a catagory of questions
            case _:
                if int(user_catagory_choice) <= len(prompt_dict) and int(user_catagory_choice) > 0:
                    pass
                else:
                    themed_print(f"Command '{user_catagory_choice}' not recognized.", "Error")
                    continue

        # Retrieve the catagory name from the dictionary and print to console
        catagory_name = list(prompt_dict.keys())[int(user_catagory_choice) - 1]

        # Provide the user with a list of questions from their chosen catagory to choose from
        while True:
            questions_in_catagory = prompt_dict[catagory_name]
            for key in questions_in_catagory:
                question = questions_in_catagory[key]
                # Look for '<' '>' in the prompt. If they exist, replace them with their corresponding values.
                if '<' in question and '>' in question:
                    questions_in_catagory[key] = questions_in_catagory[key].replace('<job_name>', ssot.job_name)
                    questions_in_catagory[key] = questions_in_catagory[key].replace('<job_description>', ssot.job_description)
                    questions_in_catagory[key] = questions_in_catagory[key].replace('<company_name>', ssot.company_name)
                    questions_in_catagory[key] = questions_in_catagory[key].replace('<company_description>', ssot.company_description)
                    questions_in_catagory[key] = questions_in_catagory[key].replace('<resume>', ssot.resume)
                    questions_in_catagory[key] = questions_in_catagory[key].replace('<company_website>', ssot.company_website)
            print_menu_options(catagory_name, questions_in_catagory, terminal_size)
            user_question_choice = input('\nUSER: ')
            # Check if the user selected 'q' to return to the main menu
            if user_question_choice.lower() == 'q':
                break
            # Check if user entered a number and if that number is a valid question
            if user_question_choice.isdigit() is True and (int(user_question_choice)-1) in questions_in_catagory.keys():
                user_question_choice = int(user_question_choice) - 1 # Adjust input for 0 indexing
                send_prompt(questions_in_catagory[user_question_choice], session_timestamp)
            # Check if the user entered something other than a number and if that input is a valid question
            elif user_question_choice in questions_in_catagory.keys():
                send_prompt(questions_in_catagory[user_question_choice], session_timestamp)
            # Otherwise, the user entered an invalid command
            else:
                themed_print(f"Command '{user_question_choice}' not recognized.", "Error")
                continue

if __name__ == "__main__":
    main()
#endregion
