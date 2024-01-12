# Employ Ease with ChatGPT 3.5 API

## About Employ Ease

This project is a chatbot that helps you find a job. It uses the ChatGPT 3.5 API to generate responses to prompts that are focused around job hunting. The bot will ask you questions about your job search, and then give you advice based on your answers.

## How to install Employ Ease
Follow these simple steps to install and run the Employ Ease project on your system:

### Prerequisites

Before you begin, ensure that you have provided an API key to the config.ini file. This file is located in the root directory of the Employ Ease project.
You can get an API key by signing up for the ChatGPT 3.5 API at https://chatgpt.com/. 
Once you have an API key, you can add it to the Communication section of the config.ini file

### Step-by-Step Installation

1. **Open Command Line Interface**: Navigate to the directory where the Employ_Ease project folder is located.

2. **Install the Project**:
   
   Run the following command in your command line interface:

   ```bash
   pip install .

3. **Run the Project**:
   
   Run the following command in your command line interface:

   ```bash
   employ_ease

## How to change this project for your own use case

The main way to change tailor this project is to go to the 'prompts.ini' file, located in the ./src/internal folder. This file contains all of the prompts that are used to interact with the Employ Ease bot.
You can change these prompts to whatever you want, and the bot will respond accordingly. In this case, the prompts are all focused around job hunting. 

Instead, you could change the prompts to be about a different topic, such as sports, or movies, or anything else you can think of. Feel free to clone and use this project to use for your own puposes.

## Found an issue or want to contribute?

If you found an issue or would like to submit an improvement to this project, please submit an issue using the issues tab above. If you would like to submit a PR with a fix, please reference the issue you created.

Your contributions, whether big or small, are greatly valued.
