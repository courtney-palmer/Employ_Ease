'''ChatGPT's API is incapable of memory, so we need to write our own solution for memory implementation of the chatbot.

This file is part of a project that is licensed under the GNU General Public License v3.0 (GPLv3).
It includes code adapted from David Shapiro's project LongtermChatExternalSources, which is licensed under the MIT License.
The adapted code is used under the terms of the MIT License, and this entire file is also subject to the terms of the GNU GPLv3.
 
The MIT-Licensed code from David Shapiro's project can be found at:
https://github.com/daveshap/LongtermChatExternalSources/blob/main/chat.py
 
The MIT License text as applied to David Shapiro's code is as follows:

MIT License

Copyright (c) 2022 David Shapiro

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

#region Imports
import os
import re
from openai import OpenAI
import numpy as np
from numpy.linalg import norm
import re
from time import sleep
import datetime
import configparser
import tiktoken
from src.scripts.file_handler import read_file_content
#endregion

config_obj = configparser.ConfigParser()
config_obj.read(os.getcwd() + "\\config.ini")
APIKey = config_obj.get('Communication', 'APIKey')
client = OpenAI(api_key=APIKey)
MaxTokenLimit = 4097
MaxTokenResponseLimit = 400

#region Definitions
def timestamp_to_datetime(unix_time):
    ''' Converts a UNIX timestamp to a datetime object.
    
    unix_time: the UNIX timestamp to convert
    return: the datetime object
    '''
    return datetime.datetime.fromtimestamp(unix_time).strftime("%A, %B %d, %Y at %I:%M%p %Z")

def gpt3_embedding(content, model='text-embedding-ada-002'):
    ''' Returns the embedding of the given content using the specified model.
    
    content: the content to embed
    model: the model to use for embedding
    return: the embedding of the content
    '''
    content = content.encode(encoding='ASCII',errors='ignore').decode()
    response = client.embeddings.create(input=content,model=model).data[0].embedding
    return response

def similarity(v1, v2):
    ''' Returns the cosine similarity between the two given vectors.
    based upon https://stackoverflow.com/questions/18424228/cosine-similarity-between-2-number-lists
    
    v1: the first vector
    v2: the second vector
    return: the cosine similarity between the two vectors
   '''
    return np.dot(v1, v2)/(norm(v1)*norm(v2))  # return cosine similarity

def fetch_memories(vector, logs, count):
    ''' Returns the top n memories that are most similar to the given vector.
    
    vector: the vector to compare to
    logs: the logs to search through
    count: the number of memories to return
    return: the top n memories that are most similar to the given vector
    '''
    scores = list()
    for log in logs:
        if vector == log['vector']:
            score = similarity(log['vector'], vector)
            log['score'] = score
            scores.append(log)
    ordered = sorted(scores, key=lambda d: d['score'], reverse=True)
    try:
        ordered = ordered[0:count]
        return ordered
    except:
        return ordered

def load_convo(sessionFolder):
    ''' Loads the conversation from the given session folder.
    
    sessionFolder: the session folder to load the conversation from
    return: the conversation
    '''
    filepath_to_session_memory = f"src\\internal\\memory\\{sessionFolder}"
    files = os.listdir(filepath_to_session_memory)
    files = [i for i in files if '.json' in i]  # filter out any non-JSON files
    result = list()
    for file in files:
        # data = read_json_file(f"{filepath_to_session_memory}\\{file}")
        data = read_file_content(f"{filepath_to_session_memory}\\{file}")
        result.append(data)
    ordered = sorted(result, key=lambda d: d['time'], reverse=False)  # sort them all chronologically
    return ordered

def encoding_getter(encoding_type: str):
    '''
    Returns the appropriate encoding based on the given encoding type (either an encoding string or a model name).
    '''
    if "k_base" in encoding_type:
        return tiktoken.get_encoding(encoding_type)
    else:
        return tiktoken.encoding_for_model(encoding_type)

def tokenizer(string: str, encoding_type: str) -> list:
    '''
    Returns the tokens in a text string using the specified encoding.
    '''
    encoding = encoding_getter(encoding_type)
    tokens = encoding.encode(string)
    return tokens

def token_counter(string: str, encoding_type: str) -> int:
    '''
    Returns the number of tokens in a text string using the specified encoding.
    '''
    num_tokens = len(tokenizer(string, encoding_type))
    return num_tokens

def summarize_memories(memories):
    ''' Summarizes the given memories into one payload.
    
    memories: the memories to summarize
    return: the summarized memories
    '''
    memories = sorted(memories, key=lambda d: d['time'], reverse=False)  # sort them chronologically
    block = ''
    identifiers = list()
    timestamps = list()
    for mem in memories:
        block += mem['message'] + '\n\n'
        identifiers.append(mem['uuid'])
        timestamps.append(mem['time'])
    block = block.strip()
    prompt = f"Write detailed notes of the following in a hyphenated list format like '-' {block} NOTES:"
    
    # Tokenize the prompt and add the number of tokens for the response. Check if the prompt is over the limit.
    tokensForPrompt = token_counter(prompt, "gpt-3.5-turbo") + MaxTokenResponseLimit 
    
    # print(f"===== PROMPT TOKENS: {tokensForPrompt} ===== ")
    if tokensForPrompt > MaxTokenLimit:
        #print(f"Warning: The prompt is {tokensForPrompt} tokens long, which is over the limit of {MaxTokenLimit} tokens. The prompt will be truncated.", "Warning")
        prompt = prompt[:MaxTokenLimit]
    notes = gpt3_completion(prompt)
    return notes

def get_last_messages(conversation, limit):
    ''' Returns the last n messages from the given conversation.
    
    conversation: the conversation to get the last messages from
    limit: the number of messages to return
    return: the last n messages from the given conversation
    '''
    try:
        short = conversation[-limit:]
    except:
        short = conversation
    output = ''
    for i in short:
        # data = read_json_file(i)
        output += '%s\n\n' % i['message']
    output = output.strip()
    return output

def gpt3_completion(prompt, model='gpt-3.5-turbo-instruct', temp=0.0, top_p=1.0, tokens=400, freq_pen=0.0, pres_pen=0.0, stop=['USER:', 'EmployEase:']):
    ''' Returns the response from GPT3 for the given prompt.
    
    prompt: the prompt to send to GPT3
    model: the model to use for the response
    temp: the temperature to use for the response
    top_p: the top p value to use for the response
    tokens: the number of tokens to use for the response
    freq_pen: the frequency penalty to use for the response
    pres_pen: the presence penalty to use for the response
    stop: the stop tokens to use for the response
    return: the response from GPT3 for the given prompt
    '''
    max_retry = 3
    retry = 0
    prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
    while True:
        try:
            response = client.completions.create(
                model=model,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop)
            text = response.choices[0].text.strip()
            
            text = re.sub('[\r\n]+', '\n', text)
            text = re.sub('[\t ]+', ' ', text)
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            # print(f'Error communicating with OpenAI{oops}', "Error")
            sleep(1)
#endregion
