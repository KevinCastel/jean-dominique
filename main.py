import datetime
from datetime import time


from os import read, system
from re import M
from unicodedata import category
from aiohttp import client
from discord import CategoryChannel, Color, channel, command, guild, user


from File import FileEnvironnement

from HangmanGame import HangmanGame

from Word import Word

import discord
from discord.ext import commands

import discord_message
from discord_message import Discord_Command

class Application(discord.Client):
      
    def __init__(self, loop=None):
        super().__init__(loop=loop)
        # intents= discord.Intents.default()
        
        intent = self.intents.default()
        intent.members = True

        self.bot = commands.Bot(command_prefix=":", intents=intent)
        
        self.hg = HangmanGame()
        
        self.dict_jean_dominique_room_by_guild = {}
        #(int(server_id) : {name_channel:channel_id})

        self._dict_hangmans_by_guild = {}
        #(int(server_id) : {user_id:[word_object, channel_id]})

    
    
    """
    Message
    """
    
    @commands.Cog.listener()
    async def on_ready(self):
        """
            on_ready method from discord.py API
        """
        print("Launched")
        
        self._dict_command = {
            "aide"      : "commande d'aide",
            "jouer"     : "commande pour démarrer une partie",
            "stop"      : "permet d'arrêter une partie si vous êtes en jeu",
            "uninstall" : "désinstalle l'environnement de l'application"
        }
        
        jean_dominique_category_exist = False        
        jean_dominique_category_id:int
        jean_dominique_category:discord.CategoryChannel
        
        jean_dominique_discuss_channel_exist = False
        
        dict_channel_name_exists = {
            "discuss" : False,
            "log-room" : False
        }
        
        dict_channel_id = {
            "discuss" : int,
            "log-room" : int
        }
        
        list_jean_dominique_category_channel_id = []
        
        for guild in self.guilds:
            self._dict_hangmans_by_guild[guild.id] = {}
            
            jean_dominique_category_exist = self.check_category_exists(
                list_categories=guild.categories,
                category_name="jean-dominique")
            
            if not jean_dominique_category_exist:
                await guild.create_category(name="jean-dominique")

            jean_dominique_category_id = self.get_category_id(
                categories=guild.categories,
                category_name="jean-dominique")
            
            jean_dominique_category = self.get_category_by_id(
                list_categories=guild.categories,
                category_id = jean_dominique_category_id
            )
            
            for channel_name in dict_channel_name_exists.keys():
                dict_channel_name_exists[channel_name] = self.check_channel_exists(
                    list_channels_from_cat=jean_dominique_category.channels,
                    channel_name=channel_name)
                
            for channel_name,channel_exists in dict_channel_name_exists.items():
                if not channel_exists:
                    # await jean_dominique_category.create_text_channel()
                    await jean_dominique_category.create_text_channel(name=channel_name)
                
                dict_channel_id[channel_name] = self.get_channel_id_by_name(
                    name=channel_name,
                    list_channels_from_cat=jean_dominique_category.channels)
                        
            self.dict_jean_dominique_room_by_guild[guild.id] = dict_channel_id
            dict_channel_id = {
                "discuss":int,
                "log-room":int
            }
            
    
        # for dict_channel in self.dict_jean_dominique_room_by_guild.values():
        #     chan = self.get_channel(dict_channel["discuss"])
        #     await chan.send("Hey!\nI'm finally back.")
        
    #command
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 858045603371286548:
            return
        
        dict_channels_from_jean_dominique = {
            "discuss" : None,
            "log-room" : None
            }
        jean_dominique_category = message.channel.category
        # for channel in jean_dominique_category.channels:
        #     if channel.name in dict_channels_from_jean_dominique:
        #         dict_channels_from_jean_dominique[channel.name] = self.get_channel(channel.id)
        
        dict_channels_from_jean_dominique = self.dict_jean_dominique_room_by_guild[message.guild.id]
        
        new_game_channel = discord.channel
        
        dict_hangman = {}
        
        is_user_in_game = self.check_user_in_game(
            user_id=message.author.id,
            guild_id=message.guild.id)
        
        guild_id = message.guild.id
        
        jd_user = self.get_user(858045603371286548)
        
        
        
        
        list_sub_command = []
        list_g = []
        is_cmd_valid = False
        
        list_game_data = []
        
        cmd = str(message.content)
        command_object = Discord_Command(command=cmd)
        if not is_user_in_game:
            if message.channel.id == dict_channels_from_jean_dominique["discuss"]:
                match_obbject = command_object.get_match()
                if not match_obbject is None:
                    list_g = command_object.get_match_group_elements(
                        m=match_obbject)
                    is_cmd_valid = command_object.check_command_valid(list_g[0])
                    if is_cmd_valid:
                        list_sub_command = command_object.get_subcommand_by_command(
                            list_g[0])
                        if not list_sub_command is None:
                            is_subcommand_valid = command_object.check_subcommand(
                                subcommand=list_g[1],
                                list_subcommand=list_sub_command
                            )
                            if list_g[0] == "play":
                                if list_g[1] == "solo":
                                    try:
                                        dict_hangman = self._dict_hangmans_by_guild[guild_id]
                                        
                                        word_object = Word()
                                        word_object._set_word_with_hidden_characters()
                                        
                                        channel_name = "solo "+str(self.count_solo_channels(channels_solo=jean_dominique_category.channels))
                                        new_game_channel = await jean_dominique_category.create_text_channel(name=channel_name)
                                        
                                        dict_hangman[message.author.id] = [word_object, new_game_channel]
                                        
                                        self._dict_hangmans_by_guild[guild_id] = dict_hangman

                                        e = discord.Embed(title="HangmanGame", colour=0x7D1784)
                                        if len(word_object.list_chars_tryed)>0:
                                            e.add_field(name="Charactères essayaient:", value=word_object.get_chars_tryed(), inline=False)
                                            
                                        e.add_field(name="Mot:", value=word_object._word_with_hidden_characters, inline=False)

                                        await new_game_channel.send(embed=e)
                                        
                                        
                                        # e = discord.Embed(title=f"AT {datetime.now()}")
                                        # e.add_field(name="")
                                    except:
                                        await message.reply("Désolé mais une erreur est survenue...")
                                # elif list_g[1] == "multi":
                                #     print("multi")
                            elif list_g[0] == "aide":
                                if list_g[1] == "play" or "jouer":
                                    await message.reply(f"'play' is used with subcommand as '-solo' (for playing singleplayer)")
                        elif list_g[0] == "uninstall":
                            list_channels = self.get_category_channels_by_guild_id(
                                guild_id=guild_id)
                            
                            for c in list_channels:
                                chan = self.get_channel(c)
                                jean_dominique_category = chan.category
                                await chan.delete(reason="uninstall")
                            await jean_dominique_category.delete(reason="uninstall")
                        elif list_g[0] == "aide":
                            msg = "Voici le message d'aide:\n```fix\n"
                            for command_name, function_command in self._dict_command.items():
                                msg += f"{command_name} : {function_command}\n"
                            msg += "```"
                            await message.reply(msg)
                else:
                    await message.reply("La commande est invalide.")
        else:
            dict_hangman = self._dict_hangmans_by_guild[message.guild.id]
            list_game_data = dict_hangman[message.author.id]
            if list_game_data[1].id == message.channel.id:
                if message.content == "$stop":
                    await list_game_data[1].delete()
                    
                    del dict_hangman[message.author.id]
                    self._dict_hangmans_by_guild = dict_hangman
                else:
                    if len(message.content) == 1:
                        word_object = list_game_data[0]
                        word_object.add_char_to_list_tryed(c=message.content)
                        word_object.refresh_word(char_typed=message.content)
                        user_win = word_object.check_win()
                        if not user_win:
                            list_game_data[0] = word_object

                            e = discord.Embed(title="HangmanGame", colour=0x7D1784)
                            if len(word_object.list_chars_tryed)>0:
                                e.add_field(name="Charactères essayaient:", value=word_object.get_chars_tryed(), inline=False)
                                
                            e.add_field(name="Mot:", value=word_object._word_with_hidden_characters, inline=False)
                            
                            new_game_channel = list_game_data[1]
                            await new_game_channel.send(embed=e)
                        else:
                            await self.get_channel(dict_channels_from_jean_dominique["discuss"]).send(f"{message.author.mention} Bravo!!!")
                            await list_game_data[1].delete()
                            
                            del dict_hangman[message.author.id]
                    else:
                        await message.delete()
                
    
    #embed
    # def get_solo_game_embed(self, w):
    #     e = discord.Embed(title="HangmanGame", colour=0x7D1784)
    #     # pcte = 
    #     e.set_author(name="Jean-Dominique")
    #     e.add_field(name="Charactère essayaient:", value=w.get_chars_tryed())
    #     # e.add_field(name="Mot:", value=w._word_with_hidden_chars, inline=False)
        
    #     return e
    
    #gestion user
    def check_user_in_game(self, user_id:int, guild_id:int):
        dict_user_in_game = self._dict_hangmans_by_guild[guild_id]
        if len(dict_user_in_game) > 0:
            return (user_id in dict_user_in_game.keys())
        else:
            return False
   
 
    #gestion channels
    def delete_game_channel(self):
        pass
        
    
    def count_solo_channels(self, channels_solo:discord.CategoryChannel.channels):
        """
            Count channels with the name wich start with "solo" 
            
        Args:
            channels_solo (discord.CategoryChannel.channels): list of all channels from an category

        Returns:
            num(int): index of channels
        """
        num = 0
        for c in channels_solo:
            if c.name.startswith("solo"):
                num += 1
        return num
    
    def get_channel_id_by_name(self, name:str, list_channels_from_cat:discord.CategoryChannel.channels):
        """
            Search an channel by his name to get and return his id

        Args:
            name (str): name of the channel to search
            list_channels_from_cat (discord.CategoryChannel.channels): list of existing channels in a category

        Returns:
            int : id of the channel to find
        """
        id:int
        for c in list_channels_from_cat:
            if c.name == name:
                id = c.id
        return id
    
    def check_channel_exists(self, list_channels_from_cat:discord.CategoryChannel.channels ,channel_name:str):
        """
            Check if an channel exists in list of channels from an guild by the channel name wich is searched        

        Args:
            list_channels_from_cat (discord.CategoryChannel.channels): list of the the whole categories from an guild
            channel_name (str): name of the channel wich is researched

        Returns:
            bool : if the channel exists or not
        """
        channel_exist = False
        for c in list_channels_from_cat:
            if not channel_exist:
                channel_exist = (c.name == channel_name)
        
        return channel_exist
    
    #gestion category
    def get_category_by_id(self, list_categories:discord.CategoryChannel, category_id:int):
        """
            Search an category by her id and returned as discord.CategoryChannel object

        Args:
            list_categories (discord.CategoryChannel): list of whole category from an guild
            category_id (int): id of the category searched

        Returns:
            discord.CategoryChannel wich is the category that was searched 
        """
        category = discord.CategoryChannel
        for c in list_categories:
            if c.id == category_id:
                category = c
        
        return category
    
    def check_category_exists(self, list_categories:discord.CategoryChannel, category_name:str):
        """
            Check if the category name specified as
                parameters

        Args:
            category_name (str): name of the category
            list_categories (discord.CategoryChannel) : list of all existing categories on an guild

        Returns:
            bool: if the category exist or not
        """
        category_exist = False; category_id = None        
        category_exist = False
        for category in list_categories:
            if not category_exist:
                category_exist = (category.name == "jean-dominique")

        return category_exist
    
    def get_category_id(self, categories:discord.CategoryChannel, category_name:str):
        """
            Get the ID of the category by searching by her name in the whole list of
                the categories of an guild

        Args:
            categories (discord.CategoryChannel): list of all categories existing on a guild
            category_name (str): name of the category wich is researched

        Returns:
            int: id of the category searched
        """
        id = 0
        for category in categories:
            if category.name == category_name:
                id = category.id
        
        return id
    
    def get_category_channels_by_guild_id(self, guild_id:int):
        list_channels = []
        for g_id,chan in self.dict_jean_dominique_room_by_guild.items():
            if g_id == guild_id:
                for chan_id in chan.values():
                    list_channels.append(chan_id)
        
        return list_channels


debug = Application()
debug.run("deleted :'(")
