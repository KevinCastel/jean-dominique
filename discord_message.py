import re

from os import system

from discord import command
from matplotlib.pyplot import cm

class Discord_Command:
    
    def __init__(self, command:str):
        super().__init__()
        
        self.regex = re
        
        self._command = command
        self._argument: list(str)
        
            
    
    def get_match(self):
        """
            Test patterns (list) wich are returned as group

        Returns:
            re.match.groups : list of match (re.match.groups())
        """
        list_patttern = [
            "^\$(?P<command>play|lang|aide)\s\++(?P<sub_command>solo|multi|play|lang)",
            "^\$(?P<command>uninstall|stop|aide)"
        ]
        m = None
        for p in list_patttern:
            if m is None:
                m = re.match(pattern=p, string=self._command)
        return m
    
    def get_match_group_elements(self,m):
        return list(m.groups())

    def check_command_valid(self, cmd:str):
        return (cmd in ["lang", "play","stop","uninstall","aide"])
    
    def get_subcommand_by_command(self, cmd:str):
        """
            Get subcommand of an command by the command

        Returns:
            list(str): list of subcommand from an command
        """
        dict_subcommand_by_command = {
            "lang": ["fr","en"],
            "play": ["solo","multi"],
            "stop": None,
            "uninstall":None,
            "aide":["play","lang"]
        }
        return dict_subcommand_by_command[cmd]

    def check_subcommand(self, subcommand:str, list_subcommand:str):
        return (subcommand in list_subcommand)
    