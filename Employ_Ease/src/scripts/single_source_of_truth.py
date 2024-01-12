'''
Single Source of Truth Module for Employ Ease

This file is responsible for maintaining a Single Source of Truth (SSOT) for the application.
It achieves this by storing all relevant information in a single INI file, named SingleSourceOfTruth.ini.
The SSOT acts as the central memory for the application, storing key information such as:
    - Job Description
    - Job Name
    - Company Description
    - Company Name
    - Company Website
    - Resume

A single_source_of_truth class object is created to represent the SSOT internally. 
The class object is initialized with the values from the SingleSourceOfTruth.ini file.
The ini file is used to remember SSOT information between sessions.
    
The main purpose of this file is to uphold the integrity of the SSOT and to provide functions for other components of the application to access and update the SSOT as needed.

Author: Courtney Palmer
'''

#region Imports
import os
import configparser
from src.scripts.file_handler import load_ini
#endregion

SSOT_FILE_PATH = "src\\internal\\single_source_of_truth.ini"

#region Class Definition
class single_source_of_truth:
    config_obj = configparser.ConfigParser()
    job_name = ""
    job_description = ""
    company_name = ""
    company_description = ""
    resume = ""

    def __init__(self):
        self.config_obj.read(os.getcwd() + f"\\{SSOT_FILE_PATH}", encoding='utf-8')
        self.job_name = self.config_obj.get('application', 'job_name').strip()
        self.job_description = self.config_obj.get('application', 'job_description').strip()
        self.company_name = self.config_obj.get('application', 'company_name').strip()
        self.company_description = self.config_obj.get('application', 'company_description').strip()
        self.resume = self.config_obj.get('candidate', 'resume').strip()
        self.company_website = self.config_obj.get('application', 'company_website').strip()
        
    def update_truth(self):
        self.config_obj.read(os.getcwd() + f"\\{SSOT_FILE_PATH}", encoding='utf-8')
        self.job_name = self.config_obj.get('application', 'job_name').strip()
        self.job_description = self.config_obj.get('application', 'job_description').strip()
        self.company_name = self.config_obj.get('application', 'company_name').strip()
        self.company_description = self.config_obj.get('application', 'company_description').strip()
        self.company_website = self.config_obj.get('application', 'company_website').strip()
        self.resume = self.config_obj.get('candidate', 'resume').strip()

    def job_name(self):
        return self.job_name
    def job_description(self):
        return self.job_description
    def company_name(self):
        return self.company_name
    def company_description(self):
        return self.company_description
    def resume(self):
        return self.resume
    def company_website(self):
        return self.company_website
    
    @staticmethod
    def update_ssot_ini_info(**kwargs):
        ''' General function to update single_source_of_truth.ini with various information. 
    
        **kwargs: the key-value pairs to update in the SSOT
        '''
        updates = {}
        for key, value in kwargs.items():
            section, option = key.split("_", 1)
            if section not in updates:
                updates[section] = {}
            updates[section][option] = value
    
        parser = load_ini(f"{os.getcwd()}\\{SSOT_FILE_PATH}", "single_source_of_truth.ini")
        for section, options in updates.items():
            for option, value in options.items():
                parser.set(section, option, f"\"{value}\"")
        try:
            with open(os.path.join(os.getcwd(), SSOT_FILE_PATH), 'w', encoding= 'utf-8') as configfile:
                parser.write(configfile)
        except IOError as e:
            print(f"Error writing to file: {e}")
#endregion
