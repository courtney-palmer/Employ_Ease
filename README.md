# Employ Ease with ChatGPT 3.5 API

## About Employ Ease

This project is a chatbot that helps you find a job. It uses the ChatGPT 3.5 API to generate responses to prompts that are focused around job hunting. The bot will ask you questions about your job search, and then give you advice based on your answers.

## How to install Employ Ease
Follow these simple steps to install and run the Employ Ease project on your system:

### Prerequisites

Before you begin, ensure that you have provided an API key to the config.ini file. This file is located in the root directory of the Employ Ease project.
You can get an API key by signing up for the ChatGPT 3.5 API at https://chatgpt.com/. After signing up, you may generate your API key here: https://platform.openai.com/api-keys

Once you have an API key, you can add it to the Communication section of the config.ini file

### Step-by-Step Installation

1. **Open Command Line Interface**:  Open your preferred CLI and navigate to the directory where the Employ_Ease project folder is located.

2. **Install the Project**:
   
   Run the following command in your command line interface:

   ```bash
   pip install .

3. **Run the Project**:
   
   Run the following command in your command line interface:

   ```bash
   employ_ease


The following menu will display after launching Employ Ease:

![image](https://github.com/courtney-palmer/Employ_Ease/assets/28797810/29472fd1-60d9-443d-a831-7605edd5e9c3)

## Using the tool
Employ Ease needs to know three things in order to provide advice with the proper context. These are: a Job Description, a Company Description, and a Resume. 

There are two different ways you can provide this information. 

1. Select 'U' in the Menu to update your application info. You can then provide either a body of text or a filepath that contains the new info.
2. Toggle on the 'load on launch' setting in the config.ini file. You can then provide filepaths in config.ini which Employ Ease will read every time it is launched.

To see what is currently in memory, select 'U' -> '5': Check Contents in Memory. 

After Employ Ease is provided with the proper context, it will be ready to help answer questions about job descriptions, resumes, cover letters, interviews, and job negotiations. 

## How to change this project for your own use case

The main way to modify this project is to go to the 'prompts.ini' file, located in the ./src/internal folder. This file contains all of the prompts that are used to interact with the Employ Ease bot.
You can change these prompts to whatever you want, and the bot will respond accordingly. In this case, the prompts are all focused around job hunting. 

Instead, you could change the prompts to be about a different topic, such as sports, or movies, or anything else you can think of. Feel free to clone and use this project to use for your own puposes.

## Found an issue or want to contribute?

If you found an issue or would like to submit an improvement to this project, please submit an issue using the issues tab above. If you would like to submit a PR with a fix, please reference the issue you created.

Your contributions, whether big or small, are greatly valued.
