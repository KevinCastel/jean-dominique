import xml.etree.ElementTree as ET

import os
from os import getcwd, listdir, system
from os.path import isfile

class FileEnvironnement:
    """
    Class FileEnvironnement is used for File Gestion.
    This class allows you to load and parse XML
    (Not polymorphism)    
    """
    
    def __init__(self, lang='en', ):
        """
        

        Args:
            path ([type]): [description]
            lang (str, optional): [description]. Defaults to 'en'.
        """
        self.lang = lang
        self.dict_command, self.dict_message, self.dict_error = {}, {}, {}
        self.dict_path_file = {}
        
        self.dict_authorized_roles = {}
                
    def Parse_Xml_File(self):
        path = getcwd() + r"\version 1.1 (rewrite)\message.xml"
        if isfile(path):
            file = ET.parse(path)
            root = file.getroot()
            lang_root = root.findall(self.lang)
            
            for environnement_data in lang_root:
                command = environnement_data.find("command")
                message = environnement_data.find("message")
                error = environnement_data.find("errors")
                for subchild in command:
                    self.dict_command[subchild.tag] = subchild.text
                for subchild in message:
                    self.dict_message[subchild.tag] = subchild.text
                for subchild in error:
                    self.dict_error[subchild.tag] = subchild.text


    def Add_Word(self):
        """
            This method add word precised by the user on discord
            
            Args:
                self for acces of File class 
        """
        pass
