from typing import List
import discord
from discord import channel

from discord.ext import commands
from discord.ext.commands.converter import VoiceChannelConverter
from discord.flags import Intents
from discord.message import implement_partial_methods

from random import choice

from time import sleep

import random

import os


intents = discord.Intents.default()
intents.members = True 


bot = commands.Bot(command_prefix="", intents=intents)
prefix = "-"

jd_channel_id = 891011500632862780

preparing_server = False


listAllRole = []
dict_members_supported = {}

os.system("cls")



class HangmanGame():
    """HangmanGame is an child class, which the parent is the 'Parent' class"""
    def __init__(self):
        """Constructor of HangmanGame"""
        self.player_name = None
        
        self.does_game_was_started = False
        
        self.dict_initial_game_data = {"life":None,"difficulty":2}
        self.dict_soloi_data = {"life":None,"difficulty":2,"player":None,"word":None}
        self.dict_soloii_data = {"life":None,"difficulty":2,"player":None,"word":None}
        self.dict_multiplayer_data = {"life":None,"difficulty":2,"player":None,"word":None,"tour":None}

        self.list_data_waiting = [None,None,None]

        self.list_word = ["discord" ,"internet" ,"véhicule" ,"mot"
                ,"maison","personnage","complexe","nationalisme",
                "interlude","français","camion","voiture","non","oui","pas","un"]

        self.list_character_tryed = []
        self.character_hidden = "¤"
        self.dict_character_tryed = {}

        self.dict_word_by_letter = {}
    
        self.dict_word = {}

        self.dict_user_choosing_data = {}
                
        self.list_user_choosing_time = []
        self.list_user_choosing_life = []
        
        self.dict_room = {}

        self.dict_game_alphabet = {}

        
    def Set_Character_Foundt(self, w = None):
        """
        Cette méthode permet de savoir combien de lettre(s) ont étaient trouvées
        par le joueur.
        Retourne ce nombre de lettres
        Argument:
            self
            n = nombre de lettres trouvaient
            w = mot à trouver
        """
        n = 0
        for c in w:
            if c == self.character_hidden:
                n += 1
        return n

    def Check_Win(self, w:str):
        """
        Cette méthode vérifi si le joueur à gagner ou non sur un booléen
        Retourne ce booléen

        Argument:
            does_player_won = est un booléen permettant de savoir si le joueur à gagner ou non:
                -Si 'None' alors la partie continu
                -Si 'False' alors la partie à était perdu
                -Si 'True' alors la partie à était gagner
            w = string mot du joueur
        """
        does_player_won = None
        index_room = self.Get_Room_Index()
        life = 0
        count_character_not_fount = self.Set_Character_Foundt(w)
        if index_room == 1:
            life = self.dict_soloi_data["life"]
        if life == 0:
            does_player_won = False
        elif count_character_not_fount == 1:
            does_player_won = True
        return does_player_won

    def Creat_Message_With_Characters_Tryed(self):
        """
        This function return all the character that users already tryed 
            in a game 
        
        Param:
            msg = string that return an message that it 
                will be send on this game channel on discord 
            self
        """
        message = ""
        for k,v in self.dict_character_tryed.items():
            message += f"\n{k} :{v}"
        return message
        
    def Hide_Characters(self, word:str):
        """
        This function hide character in the word that the user have to find.
        The user have to find these hiden characters during the game.
        This function replace all characters that have to be hiden by an specific
        character for example "¤" and reformat the string by replacing hiden character 
        
        Param:
            self
        """
        index_debug = 0
        index = 0
        counter_characters_hide = 0
        maximum_hidden_character = int(len(word)/2)
        new_word = ""
        list_character = []
        list_index_character = []
        for c in word:
            list_character.append(c)
        while counter_characters_hide < maximum_hidden_character:
            index = random.randint(0,len(list_character)-1)
            list_character[index] = self.character_hidden
            if len(list_index_character) > 0:
                while index in list_index_character:
                    index = random.randint(0,len(list_character)-1)
                list_index_character.append(index)
            else:
                list_index_character.append(index)
            list_character[index] = self.character_hidden
            counter_characters_hide += 1
            index_debug += 1
        # for c in list_character:
        #     new_word += c
        new_word = new_word.join(list_character)
        self.dict_word[new_word] = word
        if counter_characters_hide > maximum_hidden_character:
            return None
        else:
            return new_word

        
    def Refresh_Word(self, old_word:str, word:str):
        """
        Cette méthode rafraichit le mot à trouver durant la partie c'est à dire que ça réactualise les lettres cachaient trouvées
        Arg:
            self
            old_word = string mais sert de clé, l'ancienne clé avant de se faire remplacer
            word = string mais sert de clé en remplacant la vielle clé 'old_word' par son contenu
        """
        value = self.dict_word[old_word]
        del self.dict_word[old_word]
        self.dict_word[word] = value

    def Check_Characters(self, letter:str, word:str):
        """
        Cette méthode permet de voir si la lettre saisit par l'utilisateur était à trouver ou pas
        Pour cela, la lettre en argument sera recherché dans la mot.
        Argument:
            self
            letter = lettre saisit par l'utilisateur qui sera recherchée dans le mot
            word = mot en entier, le mot à trouver durant la partie
        """
        list_word = []
        dict_word = {}
        try:
            initial_word = self.dict_word[word]
            new_word = ""
            character_encoded = ""
            index = 0
            for c in initial_word:
                character_encoded = word[index]
                if character_encoded == self.character_hidden and c == letter:
                    list_word.append(letter)
                elif character_encoded == character_encoded:
                    list_word.append(character_encoded)
                else:
                    list_word.append(c)
                index +=1
            new_word = new_word.join(list_word)
            self.Refresh_Word(old_word=word, word=new_word)
            return True
        except:
            return False


    def Check_Channel(self, num:int):
        """
        Cette méthode si une salle précisé en argument sous format int est occupé ou non.
        Prendt en argument le numéro de la salle
        Retourne l'occupation sous forme de bool
        """
        list_channel_items = list(self.dict_room.values())
        does_channel_is_free = list_channel_items[num]
        return does_channel_is_free

    def Get_GameChannel_ID(self, num:int):
        """
        Cette méthode obtient l'ID à partir du numéro spécifié en argument
        Retourn l'ID
        """
        # id = None
        try:
            list_id = list(self.dict_room.keys())
            id = list_id[num]
            return id
        except:
            return None

    def Set_Word(self, room:int):
        """
        Cette méthode prépare le mot pour la partie
        """
        w = None
        if room == 1:
            self.dict_soloi_data["word"] = choice(self.list_word)
            w = self.dict_soloi_data["word"]
        elif room == 2:
            self.dict_soloii_data["word"] = choice(self.list_word)
            w = self.dict_soloii_data["word"]
        return self.Hide_Characters(w)

    def Get_Data_Message(self, index_room):
        """
        Cette méthode construit le message à afficher.
        Ce message contient toutes données modifiables 
        par l'utilisateur(futur joueur)
        Retourne le message
        """
        msg = ""
        index = 0
        list_letter = ["A","B","C"]
        list_data_en = ["life","difficulty"]
        list_data_fr = ["vie","difficulté"]
        list_difficulty_en = ["easy","medium","hard"]
        list_difficulty_fr = ["facile","moyen","difficile"]
        if index_room == 1:
            for k,v in hangman.dict_soloi_data.items():
                if k in list_data_en:
                    if k == "difficulty":
                        difficulty = list_difficulty_fr[list_difficulty_en.index(self.Get_Difficulty(index_room=index_room))]
                        msg += f"{list_letter[index]} : {list_data_fr[list_data_en.index(k)]} ({difficulty}) \n"
                    else:
                        if v == None:
                            msg += f"{list_letter[index]} : {list_data_fr[list_data_en.index(k)]} (infinit)\n"
                        else:
                            msg += f"{list_letter[index]} : {list_data_fr[list_data_en.index(k)]} ({v})\n"
                index += 1
        elif index_room == 2:
            for k,v in hangman.dict_soloii_data.items():
                if k in list_data_en:
                    if k == "difficulty":
                        difficulty = list_difficulty_fr[list_difficulty_en.index(self.Get_Difficulty(index_room=index_room))]
                        msg += f"{index} : {list_data_fr[list_data_en.index(k)]} ({difficulty}) \n"
                    else:
                        if v == None:
                            msg += f"{index} : {list_data_fr[list_data_en.index(k)]} (infinit)\n"
                        else:
                            msg += f"{index} : {list_data_fr[list_data_en.index(k)]} ({v})\n"
                index += 1

        return msg

    def Get_Data(self, num:int):
        """
        Cette méthode permet de réucupérer les informations d'une partie précisé en argument
        Retourne une liste pour afficher des données.
        """
        data = []
        if num == 0:
            data = list(self.dict_soloi_data.values())
        elif num == 1:
            data = list(self.dict_soloii_data.values())
        elif num == 2:
            data = list(self.dict_multiplayer_data.values())
        return data

    def Check_If_Input_Is_Digital(self, text:str):
        """
        Cette méthde vérifi que le texte donné en argument contient que des nombres.
        Retourne le booléen si des charactères non nombres sont retrouvés dans le texte passé
        en argument
        """
        does_text_is_right = True
        list_character_authorized = ["0","1","2","3","4","5","6","7","8","9"]
        for c in text:
            if not c in list_character_authorized:
                does_text_is_right = False
        return does_text_is_right

    def Check_If_Time_Inputed_Is_Fine(self, time:int):
        """
        Cette méthode vérifit si le temps voulut par l'utilisateur pour une partie de pendue 
        correspiond bien à la plage soit entre 4mins et 20mins
        Prends en argument la saisie et renvoie un booléen selon sa fiabillité par rapport à la plage
        """
        does_time_is_right = (time > 4 and time < 20 or time == 0)
        return does_time_is_right
    
    def Set_New_Life(self, life:int, index_room:int):
        """
        Cette méthode changel le nombre de vie d'une partie
        Prendt en argument la saisie (vie) et le numéro de salon de jeu
        """
        if life == 0:
            life = None
        if index_room == 1:
            self.dict_soloi_data["life"] = life
        elif index_room == 2:
            self.dict_soloii_data["life"] = life

    def Set_New_Difficulty(self, new_difficulty:int, index_room:int):
        """
        Cette méthode sert à redéfinir la nouvelle difficultée saisite par l'utilisateur
        pour la futur partie
        """
        if index_room == 1:
            self.dict_soloi_data["difficulty"] = new_difficulty
        elif index_room == 2:
            self.dict_soloii_data["difficulty"] = new_difficulty

    def Set_Dict_Room_On_Game(self, room_index:int, user_id:int):
        """
        Cette méthode bloque un salon de jeu en jeu pour éviter
        qu'un autre joueur ou utilisateur puisse y'accèder 
        """
        index = 1
        for k,v in self.dict_room.items():
            if index == room_index:
                self.dict_room[k] = user_id
            index += 1

    def Get_Difficulty(self, index_room:int):
        """
        Cette méthode obtient la difficulté d'une partie précisé en argument
        """
        difficulty_index = 0
        if index_room == 1:
            difficulty = self.dict_soloi_data["difficulty"]
        elif index_room == 2:
            difficulty = self.dict_soloii_data["difficulty"]
        if difficulty == 1:
            return "easy"
        elif difficulty == 2:
            return "medium"
        elif difficulty == 3:
            return "hard"
        else:
            return None

    def Lose_Life(self,index_room:int):
        """
        Cettem méthode sert à enlever -1 à une vie d'un joueur
        Args: 
            self
            index_rrom qu est le numéro de la salle de jeu du joueur 
        """
        if index_room == 1 and not self.dict_soloi_data["life"] == None:
            self.dict_soloi_data["life"] -= 1
        elif index_room == 2 and not self.dict_soloii_data["life"] == None:
            self.dict_soloii_data["life"] -= 1
        else:
            pass

    def Get_Key(self, d=None, value = None):
        """
        Cette méthode permet de retourner la clé d'une valeur d'un dictionnaire précisé en argument
        Arg:
            self
            d = dictionnaire
            value = valeur
        Return:
            key = clé retrouver par la valeur dans le dictionnaire
        """
        key = None
        for k,v in d.items():
            if v == value:
                key = k
        return key

    def Get_Word(self, index_room:int):
        """
        Cette méthode récupére le mot (encodé de façon jeu) depuis le l'utilisateur spécifié
        en argument
        ARG:
            self
            index_room = int numéro du salon en jeu 
        Return:
            word = string 
        """
        word = None
        if index_room == 1:
            initial_word = self.dict_soloi_data["word"]
        elif index_room == 2:
            initial_word = self.dict_soloii_data["word"]
        if initial_word in self.dict_word.values():
            word = self.Get_Key(d=self.dict_word, value=initial_word)
        return word

    def Get_Line_For_Message(self):
        """
        Cette méthode permet d'obtenir une ligne d'un charactère
        la ligne est retournée sous forme de string
        """
        line = "\n"
        for i in range(0,204):
            line += "-"
        line += "\n\n"
        return line


    def Set_Game_Message(self,index_room:int, w:str):
        """
        Cette méthode permet d'obtenir le message pour le jeu
        Cette dernière récupére le nombre de vie si non infinie (n'affiche pas)
        Récupère le mot enfin celui à charactères cachés. 

        JD:-"{mot} \n {lettres faites}\n TOUR:{mention} | {mention futur tour} \n Il vous reste {temps} secondes \n ????"
        JD:-"{mot} \n {lettres faites} \n 💔"

        """
        msg = f"{self.Get_Line_For_Message()}mot:{w}{self.Get_Line_For_Message()}"
        data = None
        if index_room == 1:
            list_letters = self.Get_Dict_ListValue(d=self.dict_game_alphabet,k=int(self.dict_soloi_data["player"]))
            if not list_letters is None:
                msg += "Lettres déjà faites :"
                for i in list_letters:
                    msg += i+","
                msg += "\n"            
            life = self.dict_soloi_data["life"]
            if life != None:
                for i in range(0,life):
                    msg += "♥"
            else:
                msg += "♥++"
            msg += self.Get_Line_For_Message()+"\nTapez une lettres:"
        elif index_room == 1:
            data = self.Get_Dict_ListValue(self.dict_soloii_data)
        return msg

    def Get_Dict_ListValue(self, d=None, k=None):
        """
        Cette méthode permet d'obtenir sous forme de liste les valeurs d'un dictionnaire
        Arguments:
            dictionnaire 
        Return:
            liste de la valeur du dictionnaire
        """
        if k in d:
            if not d is None:
                l = list(d[k])
        else:
            l = None
        return l

    def Get_Room_Index(self, user_name=None):
        """
        Cette méthode permet d'obtenir l'index du numéro de jeu

        Argument:
            self
            user_name = hérite de 'author' de bot.discord.py
        """
        index = 0
        if user_name in self.dict_soloi_data.values():
            index = 1
        elif user_name in self.dict_soloii_data.values():
            index = 2
        elif user_name in self.dict_multiplayer_data.values():
            pass
        return index

    def Set_Initalize_Dict_GameRoom(self, d):
        """
        Réinitialise le dictionnaire de partie spécifié en argument
        Argument:
            self
            d qui est un dictionnaire s'alignant à son argument spécifié comme:
                self.dict_soloi
                self.dict_soloii
                self.dict_multiplayer
        Return:
            d : dictionnaier
        """
        for k in d:
            if k == "player" or k == "life" or k == "word":
                d[k] = None
        return d

    def Set_Game_Off(self, user_id:str):
        """
        Cette méthode annule une partie que ce soit par erreur ou volontaire par un utilisateur
        Argument:
            self
            user_id id de l'utilisateur annulant la partie
        """
        word = ""
        if user_id in self.dict_soloi_data.values():
            word = self.dict_soloi_data["word"]
            self.dict_soloi_data = self.Set_Initalize_Dict_GameRoom(self.dict_soloi_data)
            key = self.Get_Key(d=self.dict_word, value=word)
            if key is not None:
                del self.dict_word[key]
            key = self.Get_Key(d=self.dict_room, value = int(user_id))
            if key is not None:
                self.dict_room[key] = None
        elif user_id in self.dict_soloii_data.values():
            word = self.dict_soloii_data["word"]
            self.dict_soloii_data = self.Set_Initalize_Dict_GameRoom(self.dict_soloii_data)
            key = self.Get_Key(d=self.dict_word, value=word)
            if key is not None:
                del self.dict_word[key]
            key = self.Get_Key(d=self.dict_room, value = int(user_id))
            if key is not None:
                self.dict_room[key] = None
        

    def Get_Game_Channel_Status(self):
        """
        Obtient les GameChannel occupé ou non
        Argument:
            self
        return list_game_channel s'attribut l'état des 'GameChannel's, c'est à dire que
        si le 'GameChannel' est en cours d'utilisation ou pas 
            (si 'player' = None alors le 'GameChannel' n'est pas en cours d'utilisation)
            (si 'player' != None alors le 'GameChannel' est en cours d'utilisation)
        """
        list_game_channel = []
        list_game_channel.append(self.dict_soloi_data["player"])
        list_game_channel.append(self.dict_soloii_data["player"])
        return list_game_channel

    def Get_Multiplayer_Players(self):
        """
        Cette méthode obtient la liste des joueurs du multijoueur (self.dict_multiplayer)
        SI y'a joueurs RENVOIS les joueurs sous forme de LISTE STR SINON renvois None 
        """
        list_players = None
        if self.dict_multiplayer_data["player"] != None:
            list_players = list(self.dict_multiplayer_data["player"])
        return list_players


hangman = HangmanGame()

list_message_bot = [
    "Bonjour! Bonsoir!","Désormais je peux me sentir aussi présent que les réseaux sociaux[4].","Ainsi j’exige l’obtention d’une liste des membres afin de vous juger selon votre puissance!",
	"Lorsque nous serions connecter d’un point de vue similaire alors tapez «oui» sans quoi inutile de me répondre!",
    f"Procédons donc à l’installation de cette univers ![3]\nVoici la liste des membres:","Voici la liste des membres:","Hum...m’voyez-vous, mon patrimoine semble déjà installé !","Terminons d’une traite!","Voilà ! Je trouve ce montage discordesque[2]!"
	,"Nous voilà ainsi dans les bras de Morphée[1].","Terminons d’une traite!","Nous voilà ainsi dans les bras de Morphée[1].",
    "Voici la liste des commandes:(accessible par 'aide')",
    "Eh bien ! D’abord choisissez en tapant le nom du salon.","Je vais vous présenter une liste des salons donc :",
    "Discordesque! Nous voilà au paramétrage !","Si vous souhaitez modifier l’un des paramètres alors tapez la lettre précédent le paramétrage.","En voici la liste :","Saperlipopette! Ne saviez donc pas lire!","Vous pouvez annuler la partie en tapant '-annuler' ou bien écrire '-confirmer'",
    "Très bien ! Choisissez une difficulté.","Pour cela, taper le numéro précédant la valeur","PS:‘-retour’ pour revenir en arrière et	‘-annuler’ pour quitter cette de demande de jouer",
    "Très bien ! Choississez le nombre de vie.",
    "Bien tenter ! Nous devrions pas plutôt finir ce paramétrage?!","À moins d’écrire ‘-retour’ pour retourner précédemment."]

dict_command = {"-annuler":"Annule une partie",":clear":"(ADMIN) efface un channel","-jouer":"permet de démarrer une partie","-retour":"Revient en arrière dans le paramétrage d'une partie"}
list_command = ["-annuler","oui","-confirmer","-retour","A","B","C",":clean"]
list_user_ticket = []
dict_user_administeration = {}
serveur_status = -1
token = "ODU4MDQ1NjAzMzcxMjg2NTQ4.YNYbPQ.DlxEH8kOg8SPBVKDvcJ-e7U1Rpg"

channel_ticket_id = None

does_user_can_send_message = True

bot_id = 858045603371286548


def Sleep(time:int):
    """
    Met en pause le bot durant un temps spécifié en argument
    """ 
    sleep(time/(4*(2*4)))

#---dev---

def Get_File():
    """s
    Cette fonction sert à obtenir le contenu de texte
    """
    path_file = r"D:\projet\Python\Jean Dominique\Jean Dominique\cahier des charges\réplique discours directe.txt"
    count_line = 0 
    list_lines = []
    personnage = 0
    try:
        with open(path_file, "r") as f:
            for line in f:
                if len(line) > 2:
                    if "Utilisateur" in line:
                        list_lines.append("+ |"+line)
                        personnage = 1
                    elif "JD" in line:
                        list_lines.append("- |"+line)
                        personnage = 2
                    elif personnage == 1:
                        list_lines.append("+ |"+line)
                    elif personnage == 2:
                        list_lines.append("- |"+line)

    except Exception as e:
        return "oops, something wrong happened"
    finally:
        return list_lines

def Get_Channel_ID(id):
    """
    Cette fonction obtient l'ID d'une channel précisé en argument.
    """
    id_jd_channel = id.id
    return id_jd_channel

def Get_Channel_Index_From_List(list_to_check, element:str):
    """
    Cette fonction obtient l'index d'un channel d'une liste 
    """
    index = 0
    count_list_element = 0
    does_element_was_foundt = False
    text = ""
    while not does_element_was_foundt:
        text = list_to_check[count_list_element]        
        does_element_was_foundt = str(text) == element
        index += 1
        count_list_element += 1
    return index-1

def Check_Channel_Exist(list_channel, name_channel="jd"):
    """
    Vérifi qu'un chanel précisé en argument existe
    Prendt en argument la liste des channels
    Retourne un booléen de l'existence de ce channel précisé.
    """
    does_channel_exists = False
    for text in list_channel:
        if not does_channel_exists:
            does_channel_exists = name_channel == str(text)
    return does_channel_exists

def Get_All_Rooms():
    """
    Cette fontion obtient toutes les salles de "chat"
    avec leurs IDs
    """
    text_channel_list = []
    for guild in bot.guilds:
        for channel in guild.text_channels:
            text_channel_list.append(channel)
    return text_channel_list
    

def Set_Member(role):
    """
    Cette fonction obtient les membres haut plaçer sur le serveur
    comme par exemple:
        les membres du rôle "Admin"
        le propriétaire du server.
    et les ajoute à le dictionnaire "dict_members_supported".
    
    Param:
        role = ctx.guild.roles
    
    """
    global dict_members_supported
    for member in role.members:
        if str(member) not in dict_members_supported:
            dict_members_supported[str(member)] = str(role)

def Set_Message_From_List(l:list):
    """
    Convertit une liste sous format string
    Argument
        liste 
    Return:
        msg = string

    """
    msg = "```diff\n"
    index = 1
    list_multiplayer = []
    for i in l:
        cr = ""
        for counter in range(0,index):
            cr += "i"
        if i == None:
            msg += f"+ '-solo{cr}' (libre)\n"
        else:
            msg += f"- '-solo{cr}' (occupé)\n"
        index += 1
    # list_multiplayer = hangman.Get_Multiplayer_Players()
    # if not list_multiplayer is None:
    #     msg += f"- '-multiplayer' (occupé)"
    # else:
    #     msg += f"+ '-multiplayer' (libre)"
    msg += "\n```"
    return msg


def Though_Roles(all_roles):
    """
    Cette fonction parcourt tout les rôles du server
    afin d'obtenir les membres par rôles. ces
    membres seront retenus (voir 'Set_Member')
    selon leur importance, plus l'importance du
    rôle est haute; Plus ils sont retenus. 
    
    Param:
        all_roles = ctx.guild.roles
    """
    list_roles_supported = ["admin","dev","staff"]
    for role in all_roles:
        string_role = str(role)
        if string_role.lower() in list_roles_supported:
            Set_Member(role)
            
def Get_Supported_Member(id_own_member):
    message = ""
    for k,v in dict_members_supported.items():
        member = k
        role = v
        if str(member) == str(id_own_member):
            message += f"- {member} (Propriétaire)\n"
        else:
            message += f"+ {member} ({role})\n"
    return message

def Get_Channel_Of_Category(cat):
    """
    Cette méthode obtient une liste (dictionnaire)
    des channels d'une catégorie
    
    Param:"
        ctx.guild.categories.<specific>
    
    Return:
        l_c : list
    """
    l_c = []
    for channel in cat.text_channels:
        l_c.append(channel)
    return l_c
    
def Get_Categories(cgc):
    """
    Cette fonction obtient les catégories du server
    afin de 'returner' ('dict_category')un dictionnaire les contenant.
    La fonction utilise une instance de 'guild.categories'
    ou une catégorie précise. (cgc)
    """
    dict_category = {}
    for category in cgc:
        dict_category[str(category)] = category
    return dict_category

def Check_JD_Categorie(list_categories):
    """
    Cette fonction vérifi si une catégorie existe bien
    Prendt en argument une liste des catégoiries du serveur
    Retourn si la catégorie existe ou non
    """
    does_JD_category_exists = False
    for text in list_categories:
        if does_JD_category_exists == False:
            does_JD_category_exists = "Jean Dominique" == str(text)
    return does_JD_category_exists

def Get_Dict_Key_To_Str(d=None):
    """
    Cette méthode permet d'obtenir une liste sous un format string
    Argument:
        dictionnaire à parcourir
    Retourne: 
        les 'Keys' du dictionnaire sous un format string
    """
    msg = ""
    for k,v in d.items():
        msg += f"\n{k} :{v}"
    return msg


def Get_ID(child):
    """
    Obtient l'ID de channels d'un dictionnaire
    """
    global channel_ticket_id
    for channel in child:
        hangman.dict_room[channel.id] = None
        if channel.name == "ticket":
            channel_ticket_id = channel.id

"""bot event"""

@bot.event
async def on_ready():
    """
    Cette méthode s'active dès que le bot
    démarre. Elle active la préparation
    du serveur à l'aide d'un booléen
    "preparing_server" 
    """
    global preparing_server, listAllRole, jd_channel_id, serveur_status, does_user_can_send_message
    list_room = Get_All_Rooms()
    does_channel_exists =  Check_Channel_Exist(list_channel=list_room)
    index = 0
    if len(list_room) > 0:
        childd = list_room[0]
        server_id_i = childd.guild.id
        server_id = bot.get_guild(server_id_i)
    if not does_channel_exists:
        await server_id.create_text_channel(f"jd", overwrites=None, category=None, reason=None)
    list_room = Get_All_Rooms()
    index = Get_Channel_Index_From_List(list_room, "jd")
    jd_channel_id = Get_Channel_ID(list_room[index])
    jd_channel = bot.get_channel(jd_channel_id)        
    preparing_server = True
    serveur_status = 1
    list_lines = Get_File()
    msg = "```diff\n"
    index = 0
    does_user_can_send_message = False
    for i in range(0,4):
        async with jd_channel.typing():
            Sleep(len(list_message_bot[i]))
            await jd_channel.send(list_message_bot[i])
    does_user_can_send_message = True
    print("BOT RUNNING")

@bot.event
async def on_guild_remove():
    """
    Cette méthode sert lorsque une personne quitte le serveur afin de vérifier
    si ce joueur occupé des variables de l'environnement du jeu
    """
    pass

# @bot.event
# async def on_raw_reaction_add(ctx):
#     react = ctx.message
#     print(react)
    # emoji_id = ctx.mention.id
    # print(emoji_id)

#Admin Support

@bot.command(name="uninstall")
async def Uninstall_Bot(ctx):
    global dict_members_supported
    if does_user_can_send_message:
        if len(dict_members_supported) > 0:
            if str(ctx.author) in dict_members_supported:
                await ctx.send("Je tiens à me féciliter et tout les membres pour leurs échanges dynamique et sociale! :rose:\n Procédons à ma désinstallation dans ce cas :frowning:")
                id_server = bot.get_guild(ctx.guild.id)
                dict_cat_id = Get_Categories(ctx.guild.categories)
                if "Jean Dominique" in dict_cat_id.keys():
                    category_JD = dict_cat_id["Jean Dominique"]
                    for channel in category_JD.text_channels:
                        await channel.delete(reason=None)
                    id_JD_category = bot.get_channel(category_JD.id)
                    await id_JD_category.delete(reason=None)
                    await ctx.bot.logout()
                    await login(token, bot=True)
            else:
                await ctx.send("Dites-donc!  Il va falloir allez faire le rebel ailleurs :angry:")
        else:
            await ctx.send("Je ne peux pas savoir qui sont les représentant de ce server.")

@bot.command(name=":clear")
async def Clear_Channel(ctx):
    """
    Fonction effacant les messages non-commandes et si-non le bot
    """
    global dict_members_supported, jd_channel_id, does_user_can_send_message
    counter = 0
    id_jd_channel = bot.get_channel(jd_channel_id)
    if does_user_can_send_message:
        if len(dict_members_supported) > 0:
            if str(ctx.author) in dict_members_supported:
                async for _ in id_jd_channel.history(limit=None):
                    counter += 1
                await id_jd_channel.purge(limit=counter)
            else:
                await id_jd_channel.send("Si vous continuez ainsi! Vous serez punis par mes lois! :sunglasses:")
        else:
            await id_jd_channel.send("Je ne peux pas vous confirmer en tant-que l'uns des représentant légal de ce server..! :neutral_face:")

@bot.command(name="oui")
async def Yes(ctx):
    """
    Cette méthode permet d'obtenir 
    """
    global jd_channel_id, serveur_status, preparing_server, does_user_can_send_message, dict_command, list_message_bot, channel_ticket_id, list_user_ticket
    jd_channel = bot.get_channel(jd_channel_id)
    own_member = ctx.guild.owner.id
    msg = ""
    list_message_bot_local = []
    list_all_categories = []
    user = bot.get_user(ctx.message.author.id)
    try:
        if int(ctx.message.author.id) in list_user_ticket:
            await user.send("Bon! Je vais vous expliquer comment nous allons procéder:\n\nVous allez m'écrire en détail ce qui ne va pas avec moi puis selon l'urgence vous réagirez avec un émoji de couleur suivante: \n\rvert: Peu Urgent(:green_circle:)\n\rJaune: Moyennement urgent(:yellow_circle:)\n\rRouge: Super urgent (:red_circle:)\nPS:'annuler' vous permettra d'annuler ce ticket")

        elif does_user_can_send_message:
            does_user_can_send_message = False
            if serveur_status == 1:
                if ctx.message.channel.id == jd_channel_id:
                    list_message_bot_local = [list_message_bot[4]]
                    Though_Roles(ctx.guild.roles) 
                    if len(dict_members_supported)>0:
                        list_message_bot_local.append("```diff\n"+Get_Supported_Member(bot.get_user(own_member))+"\n```")                    
                    else:
                        list_message_bot_local.append(f"\n```diff\n- {own_member}\n"+"```")
                    serveur_status = 2
                    list_message_bot_local.append(list_message_bot[3])
            elif serveur_status == 2:
                list_message_bot_local.append(f"{list_message_bot[10]}")
                does_category_Jd_exists = False
                count_supported_member = 0
                message = ""
                id_own_member = bot.get_user(ctx.guild.owner.id)
                id_server = bot.get_guild(ctx.guild.id)
                dict_channels_from_JD_category = {}
                cannot_confirm_members = True #
                list_bot_m = []
                if ctx.message.channel.id == jd_channel_id:
                    if len(dict_members_supported) > 0:    
                        if str(ctx.author) in dict_members_supported:
                            if preparing_server:
                                dict_categories = Get_Categories(ctx.guild.categories)
                                list_all_categories = list(dict_categories.values())
                                does_category_JD_exists = Check_JD_Categorie(list_all_categories)
                                if does_category_JD_exists == False:
                                    category = await id_server.create_category("Jean Dominique", overwrites=None, reason=None)
                                    await jd_channel.send("Ce dernier n'existait pas, je l'ai donc créer. :face_with_raised_eyebrow: :sunglasses:")
                                    await id_server.create_text_channel(f"Solo I", overwrites=None, category=category, reason=None)
                                    await id_server.create_text_channel(f"Solo II", overwrites=None, category=category, reason=None)
                                    await id_server.create_text_channel(f"Ticket", overwrites=None, category=category, reason=None)
                                    # await id_server.create_text_channel(f"Multijoueur", overwrites=None, category=category, reason=None)
                                    list_message_bot_local.append(list_message_bot[7])
                                else:
                                    list_message_bot_local.append(list_message_bot[8])
                                list_message_bot_local.append(list_message_bot[9])
                                preparing_server = False
                                dict_categories = Get_Categories(ctx.guild.categories)
                                id_JD_category = dict_categories["Jean Dominique"]
                                list_channels_from_JD_category = Get_Channel_Of_Category(id_JD_category)
                                Get_ID(list_channels_from_JD_category)
                                list_message_bot_local.append(list_message_bot[12])            
                                list_message_bot_local.append(f"```fix\n{Get_Dict_Key_To_Str(dict_command)}\n```")            
                            else:
                                list_message_bot_local.append("La préparation à été désactivé")
                    else:
                        cannot_confirm_members = False
            does_user_can_send_message = True
    except Exception as e:
        await jd_channel.send(f"[ERREUR]:{e}")
    finally:
        for message in list_message_bot_local:
            async with jd_channel.typing():
                await jd_channel.send(message)
        
        
# @bot.command(name=":configure")
# async def Repreparing_Server(ctx):
#     global preparing_server, jd_channel_id, does_user_can_send_message
#     if ctx.message.channel.id == jd_channel_id and does_user_can_send_message:
#         if preparing_server == False:
#             preparing_server = True
#             await ctx.send("Repréparation du serveur :angry: \nTapez ':c':Commencer la préparation du serveur.")
#     else:
#         await ctx.message.delete()

#Game Support

@bot.command(name=f"{prefix}jouer")
async def Play(ctx):
    global preparing_server, does_user_can_send_message, list_message_bot
    channel_jd = bot.get_channel(jd_channel_id)
    list_message_bot_local = []
    try:
        if ctx.message.channel.id == jd_channel_id and does_user_can_send_message:
            does_user_can_send_message = False
            if preparing_server == False:
                list_message_bot_local.append(f"{list_message_bot[13]}")
                list_message_bot_local.append(f"{list_message_bot[14]}")
                list_message_bot_local.append(f"\n{Set_Message_From_List(hangman.Get_Game_Channel_Status())}")
            elif ctx.message.author.id in hangman.dict_user_choosing_data:
                list_message_bot_local.append(f"{ctx.message.author.mention}, vous avez déjà demandé pour jouer maintenant procédé aux réglages de la partie ou taper '-annuler'")
            else:
                list_message_bot_local.append(f"{ctx.message.author.mention},Ce serveur n'est pas prêt pour jouer avec veuillez taper ':voir' ou ':c'")
            hangman.dict_user_choosing_data[ctx.message.author.id] = 0
            does_user_can_send_message = True
    except Exception as e:
        await channel_jd.send(f"[ERREUR]:{e}")
    finally:
        async with channel_jd.typing():
            for message in list_message_bot_local:
                await channel_jd.send(message)
    

# @bot.command(name=f"{prefix}multiplayer")
# async def Play_In_Multiplayer(ctx):
#     """
#     Cette commande est pour jouer en multijoueur 
#     """
#     pass

@bot.command(name=f"{prefix}soloi")
async def Play_In_Room_One(ctx):
    global jd_channel_id, does_user_can_send_message
    does_this_room_is_avalaible = False
    author_name = ctx.author
    channel_jd = bot.get_channel(jd_channel_id)
    list_data = []
    list_message_bot_local = []
    try:
        if ctx.message.channel.id == jd_channel_id and does_user_can_send_message:
            does_user_can_send_message = False
            list_message_bot_local.append(list_message_bot[15])
            if ctx.message.author.id in hangman.dict_user_choosing_data:
                if hangman.dict_user_choosing_data[ctx.message.author.id] == 0:
                    does_this_room_is_avalaible = hangman.Check_Channel(0)
                    if does_this_room_is_avalaible == None:            
                        list_data = hangman.Get_Data(0)
                        hangman.dict_soloi_data["player"] = ctx.message.author.id
                        hangman.dict_user_choosing_data[ctx.message.author.id] = 1
                        list_message_bot_local.append(list_message_bot[16])
                        list_message_bot_local.append(list_message_bot[17])
                        list_message_bot_local.append(f"\n```fix\n{hangman.Get_Data_Message(index_room=1)}\n```")
                        list_message_bot_local.append(list_message_bot[19])
                    else:
                        list_message_bot_local.append(list_message_bot[18])

            does_user_can_send_message = True
    except Exception as e:
        await channel_jd.send(f"[ERREUR]:{e}")
    finally:
        async with channel_jd.typing():
            for message in list_message_bot_local:
                await channel_jd.send(message)

@bot.command(name=f"{prefix}soloii")
async def Play_In_Room_One(ctx):
    global jd_channel_id, does_user_can_send_message
    does_this_room_is_avalaible = False
    author_name = ctx.author
    channel_jd = bot.get_channel(jd_channel_id)
    list_data = []
    try:
        if ctx.message.channel.id == jd_channel_id and does_user_can_send_message:
            does_user_can_send_message = False
            list_message_bot_local.append(list_message_bot[15])
            if ctx.message.author.id in hangman.dict_user_choosing_data:
                if hangman.dict_user_choosing_data[ctx.message.author.id] == 0:
                    await channel_jd.send("Je vais m'assurer que cette salle est libre.")
                    does_this_room_is_avalaible = hangman.Check_Channel(1)
                    if does_this_room_is_avalaible == None:            
                        list_data = hangman.Get_Data(1)
                        hangman.dict_soloii_data["player"] = ctx.message.author.id
                        hangman.dict_user_choosing_data[ctx.message.author.id] = 1
                        list_message_bot_local.append(list_message_bot[16])
                        list_message_bot_local.append(list_message_bot[17])
                        list_message_bot_local.append({hangman.Get_Data_Message(index_room=2)})
                        list_message_bot_local.append(list_message_bot[19])
                    else:
                        list_message_bot_local.append(list_message_bot[18])
            else:
                await channel_jd.send(f"{ctx.message.author.mention},Vous n'aviez cas demander pour jouer...")
            does_user_can_send_message = True
    except Exception as e:
        await channel_jd.send("[ERREUR]",e)
    finally:
        async with channel_jd.typing():
            for message in list_message_bot_local:
                await channel_jd.send(message)

@bot.command(name=f"{prefix}confirmer")
async def Confirm_Game(ctx):
    """
    Cette méthode permet de confirmer le lancement d'une partie
    """
    global jd_channel_id, does_user_can_send_message
    try:
        channeli_id = bot.get_channel(hangman.Get_GameChannel_ID(0))
        channelii_id = bot.get_channel(hangman.Get_GameChannel_ID(1))
        channel_jd = bot.get_channel(jd_channel_id)
        room_num = None
        list_game_channel = []
        if ctx.message.channel.id == jd_channel_id and does_user_can_send_message:
            does_user_can_send_message = False
            list_channel_id = list(hangman.dict_room.keys())
            index_game_room = hangman.Get_Room_Index(int(ctx.message.author.id))
            game_channel = bot.get_channel(list_channel_id[index_game_room-1])
            if ctx.message.author.id in hangman.dict_user_choosing_data: 
                if hangman.dict_user_choosing_data[ctx.message.author.id] == 1:
                    word = hangman.Set_Word(index_game_room)
                    if word != None:
                        del hangman.dict_user_choosing_data[ctx.author.id]
                        hangman.Set_Dict_Room_On_Game(user_id = int(ctx.message.author.id), room_index = index_game_room)
                        await game_channel.send(f"{ctx.message.author.mention}, Ici commence votre partie! \n {hangman.Set_Game_Message(index_room = index_game_room, w = word)}")
                    else:
                        await channel_jd.send(f"{ctx.message.author.mention}! Saperlipopette! Votre partie à due être annuler suite à une erreur inconnnue!")
                        hangman.Set_Game_Off(ctx.message.author.id)
                else: 
                    await channel_jd.send(f"{ctx.message.author.mention}, veuillez finir votre paramétrage de cette partie..")
            else:
                await channel_jd.send(f"{ctx.message.author.mention}, vous n'avez pas demandé à jouer... :angry:")
            does_user_can_send_message = True
    except Exception as E:
        await channel_jd.send(f"[ERREUR]:{E}")
        

@bot.command(name=f"{prefix}annuler")
async def Cancel_Game(ctx):
    """
    Cette fonction stop la partie en cours
    """
    global does_user_can_send_message, jd_channel_id
    jd_channel = bot.get_channel(jd_channel_id)
    try:
        if int(ctx.message.channel.id) == jd_channel_id:
            if does_user_can_send_message:
                hangman.Set_Game_Off(int(ctx.message.author.id))
                await jd_channel.send(f"{ctx.message.author.mention}!Annulation du paramétrage ou de la partie")
    except Exception as e:
        await ctx.send(f"[ERREUR]:{e}")

@bot.command(name=f"{prefix}retour")
async def Return_Command(ctx):
    """
    Cette méthode/commande permet de faire un retour en arrière
    lors d'un paramétrage d'une partie 
    """
    global jd_channel_id, does_user_can_send_message
    channel_jd = bot.get_channel(jd_channel_id)
    index_room = 0
    if ctx.message.channel.id == jd_channel_id and does_user_can_send_message:
        if ctx.message.author.id in hangman.dict_soloi_data.values():
            index_room = 1
        elif ctx.message.author.id in hangman.dict_soloii_data.values():
            index_room = 2
        if ctx.message.author.id in hangman.dict_user_choosing_data:
            string_index = str(hangman.dict_user_choosing_data[ctx.message.author.id])
            value = hangman.dict_user_choosing_data[ctx.message.author.id]
            if "." in string_index:
                hangman.dict_user_choosing_data[ctx.message.author.id] = int(value)
                await channel_jd.send(f"{ctx.message.author.mention}, Retour à le choix du paramétrage de la partie. \nVoici donc les informations de la partie:\n{hangman.Get_Data_Message(index_room=index_room)}")
            elif hangman.dict_user_choosing_data[ctx.message.author.id] > 0:
                hangman.dict_user_choosing_data[ctx.message.author.id] -= 1


@bot.command(name="A")
async def Change_Life_Data(ctx):
    """
    Cette méthode permet de modifier la quantité de vie pour une partie
    """
    global jd_channel_id, does_user_can_send_message
    channel_jd = bot.get_channel(jd_channel_id)
    list_message_bot_local = []
    try:
        if ctx.message.channel.id == jd_channel_id and does_user_can_send_message:
            if ctx.message.author.id in hangman.dict_user_choosing_data:
                if hangman.dict_user_choosing_data[ctx.message.author.id] == 1:
                    list_message_bot_local.append(list_message_bot[23])
                    list_message_bot_local.append(list_message_bot[21])
                    list_message_bot_local.append(list_message_bot[22])
                    hangman.dict_user_choosing_data[ctx.message.author.id] = 1.3
            else:
                list_message_bot_local.append(list_message_bot[24])
                list_message_bot_local.append(list_message_bot[25])
                # list_message_bot_local.append(list_message_bot[26])
    except Exception as e:
        await channel_jd.send(f"[ERREUR]:{e}")
    finally:
        async with channel_jd.typing():
            for message in list_message_bot_local:
                await channel_jd.send(message)

@bot.command(name=f"B")
async def Change_Time_Data(ctx):
    """
    Cette méthode permet de modifier le temps pour une partie
    """
    global jd_channel_id, does_user_can_send_message
    channel_jd = bot.get_channel(jd_channel_id)
    list_message_bot_local = []
    try:
        if ctx.message.channel.id == jd_channel_id and does_user_can_send_message:
            if ctx.message.author.id in hangman.dict_user_choosing_data:
                if hangman.dict_user_choosing_data[ctx.message.author.id] == 1:
                    list_message_bot_local.append(list_message_bot[23])
                    list_message_bot_local.append(list_message_bot[20])
                    list_message_bot_local.append(list_message_bot[22])
                    list_message_bot_local.append("```fix\n1:FACILE\n2:MOYEN\n3:DIFFICILE\n```")
                    hangman.dict_user_choosing_data[ctx.message.author.id] = 1.2
                else:
                    list_message_bot_local.append(list_message_bot[24])
                    list_message_bot_local.append(list_message_bot[25])
    except Exception as e:
        await channel_jd.send(f"[ERREUR]:{e}")
    finally:
        async with channel_jd.typing():
            for message in list_message_bot_local:
                await channel_jd.send(message)

"""bot event"""

@bot.event
async def on_message(message):
    global jd_channel_id, does_user_can_send_message, bot_id, dict_user_choosing_data, list_user_ticket
    list_character_waited_for_data_game = ["0","1","2","3","4","5","6","7","8","9"]
    list_command = [":clear","help","oui","-jouer"]
    list_data_command = ["0-","1-","2-"]
    list_command_game = ["-soloi","-soloii","-multiplayer"]

    dict_command = {"-soloi":0,"-soloii":0,"-multiplayer":0,"-confirmer":1}

    channel_ticket = bot.get_channel(channel_ticket_id)

    list_channel_id = None
    list_game_channel = None
    list_game_data = None
    game_channel = None

    does_player_won = None

    word = None
    list_channel_id = list(hangman.dict_room.keys())
    if preparing_server == False:
    
        list_game_channel = [bot.get_channel(list_channel_id[0])]

    mess = str(message.content)
    jd_channel = bot.get_channel(jd_channel_id)
    does_input_is_right = None
    index = 0
    user = bot.get_user(message.author.id)
    if does_user_can_send_message:
        if int(message.author.id) in hangman.dict_soloi_data.values():
            index_game_room = 1
            list_game_data = list(hangman.dict_soloi_data)
            word = hangman.Get_Word(index_room = 1)
            game_channel = bot.get_channel(list_channel_id[0])
        elif int(message.author.id) in hangman.dict_soloii_data.values():
            index_game_room = 2 
            game_channel = bot.get_channel(list_channel_id[1])
            word = hangman.Get_Word(index_room = 2)
        elif int(message.author.id) in hangman.dict_multiplayer_data.values():
            index_game_room = 3
            game_channel = bot.get_channel(list_channel_id[2])
        else:
            index_game_room = None
        if message.channel.id == jd_channel_id:
            if message.author.id in hangman.dict_user_choosing_data:
                if mess in dict_command:
                    if not hangman.dict_user_choosing_data[message.author.id] == dict_command[mess]:
                        await message.delete()
                elif hangman.Check_If_Input_Is_Digital(mess) and hangman.dict_user_choosing_data[message.author.id] == 1.3:
                    hangman.Set_New_Life(life=int(mess), index_room=index_game_room)
                    await jd_channel.send(f"Parfait! Revoici les paramétres alors:\n{hangman.Get_Data_Message(index_game_room)}\n{list_message_bot[19]}")
                    hangman.dict_user_choosing_data[message.author.id] = 1
                elif hangman.Check_If_Input_Is_Digital(mess) and hangman.dict_user_choosing_data[message.author.id] == 1.2:
                    hangman.Set_New_Difficulty(int(mess), index_room=index_game_room)
                    await jd_channel.send(f"Parfait! Revoici les paramétres alors:\n{hangman.Get_Data_Message(index_game_room)}\n{list_message_bot[19]}")
                    hangman.dict_user_choosing_data[message.author.id] = 1
                elif not mess in list_command_game and mess != "-annuler" and hangman.dict_user_choosing_data != 0 and mess != "-annuler" and hangman.dict_user_choosing_data != 1:
                    if not hangman.Check_If_Input_Is_Digital(mess):
                        await message.delete()
            # elif mess == "ticket":
            #     await jd_channel.send("Hélas! Allons donc pour un nouveau ticket par contre nous allons voir ça en privé.\nM'enfin si vous êtes d'accord, tapez 'oui' sans quoi inutile de me répondre")
            #     list_user_ticket.append(int(message.author.id))
            elif not mess in list_command and int(message.author.id) != bot_id:
                await message.delete()

        elif int(message.author.id) in hangman.dict_room.values() and int(message.channel.id) in hangman.dict_room:
            counter = 0
            async for _ in game_channel.history(limit=None):
                counter += 1
            await game_channel.purge(limit=counter)
            if len(mess) == 1:
                hangman.Check_Characters(letter = mess, word=word)
                does_player_won = hangman.Check_Win(w=word)
                if does_player_won == None:
                    if int(message.author.id) in hangman.dict_game_alphabet:
                        lv = hangman.dict_game_alphabet[message.author.id]
                        if not mess in lv:
                            hangman.dict_game_alphabet[int(message.author.id)].append(mess)
                            hangman.Lose_Life(index_room = index_game_room)
                    else:
                        hangman.dict_game_alphabet[message.author.id] = [mess]
                    if index_game_room == 1:
                        if hangman.dict_soloi_data["life"] == 0:
                            await list_game_channel[0].send(f"Vous avez perdu")
                        else:
                            word = hangman.Get_Word(index_room = 1)
                            await list_game_channel[0].send(f"{hangman.Set_Game_Message(index_room=index_game_room, w=word)}")
                    elif index_game_room == 2:
                        if hangman.dict_soloii_data["life"] == 0:
                            await list_game_channel[1].send(f"Vous avez perdu")
                        else:
                            word = hangman.Get_Word(index_room = 2)
                            await game_channel.send(f"{hangman.Set_Game_Message(index_room=index_game_room, w=word)}")
                elif does_player_won == False:
                    await jd_channel.send(f"Saperlipopette, {message.author.mention}! Vous avez perdu! \n '__Hop hop hop on se décourage pas__'")
                    hangmang.Set_Game_Off(int(message.author.id))
                elif does_player_won == True:
                    await jd_channel.send(f"Bravo, {message.author.mention}! Vous avez gagné!")
                    hangman.Set_Game_Off(int(message.author.id))
            else:
                word = hangman.Get_Word(index_room = 1)
                await list_game_channel[0].send(f"{hangman.Set_Game_Message(index_room=index_game_room, w=word)}")
        # elif int(message.channel.id) == int(channel_ticket_id) and mess == "ticket":
    elif bot_id != int(message.author.id):
        await message.delete()
    await bot.process_commands(message)

bot.run(token)

"""
Set_Game_Message() êut-être optimisé en évitant les arguments, les arguments peuvent être déplacer dans cette fonction en appelant
    d'autres méthodes de la classe 'Parent' ('index_room' et 'w')
"""