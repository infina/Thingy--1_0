from game import Game, games
from role import Voter
import random

class SerialKiller(Voter):
        def __init__(self, game, rolename):
                Voter.__init__(self, game, rolename)
                self.role = "SK"
                
        def gameStart(self):
                Voter.gameStart(self)
                self.game.tell("Role: Serial Killer", self.game.names[self])
                self.game.commentary(self.game.names[self] + ": " + "Serial Killer")
                
        def action(self, msg):
                args = msg.split(" ")
                if ((args[0] == "kill") and (self.game.phase == "night")):
                        if ((len(args) >= 2) and (args[1] in self.game.roles)):
                                self.game.nk = args[1]
                                self.game.tell(args[1] + " has been nightkilled.", self.game.names[self])
                                self.game.mkDay()
                        else:
                                self.game.tell("You must pick a valid target.", self.game.names[self])
                else:
                        Voter.action(self, msg)

class SerialJester(Voter):
        def __init__(self, game, rolename):
                Voter.__init__(self, game, rolename)
                self.role = "SJ"
                
        def gameStart(self):
                Voter.gameStart(self)
                self.game.tell("Role: Serial Jester, use !kill or !nokill", self.game.names[self])
                self.game.commentary(self.game.names[self] + ": " + "Serial Jester")
                
        def action(self, msg):
                args = msg.split(" ")
                if ((args[0] == "kill") and (self.game.phase == "night")):
                        if ((len(args) >= 2) and (args[1] in self.game.roles)):
                                self.game.nk = args[1]
                                self.game.tell(args[1] + " has been nightkilled.", self.game.names[self])
                                self.game.mkDay()        
                        else:
                                self.game.tell("You must pick a valid target.", self.game.names[self])
                elif ((arg[0] == "nokill") and (self.game.phase == "night")):
                        self.game.tell("No one has died")
                        self.game.mkDay
                else:
                        Voter.action(self, msg)
                        
class Jester(Voter):
        def __init__(self, game, rolename):
                Voter.__init__(self, game, rolename)
                self.role = "Jester"
                
        def gameStart(self):
                Voter.gameStart(self)
                self.game.tell("Role: Jester", self.game.names[self])
                self.game.commentary(self.game.names[self] + ": " + "Jester")

class Lyncher(Voter):
        def __init__(self, game, rolename):
                Voter.__init__(self, game, rolename)
                self.role = "Lyncher"
                self.target = self.game.get_role("Lynchee")
                
        def gameStart(self):
                Voter.gameStart(self)
                self.game.tell("Role: Lyncher for " + self.target, self.game.names[self])
                self.game.commentary(self.game.names[self] + ": " + "Lyncher")
                
class Lynchee(Voter):
        def __init__(self, game, rolename):
                Voter.__init__(self, game, rolename)
                self.role = "Lynchee"
                
        def gameStart(self):
                Voter.gameStart(self)
                self.game.tell("Role: Townie", self.game.names[self])
                self.game.commentary(self.game.names[self] + ": " + "Lynchee")
                
class Townie(Voter):
        def __init__(self, game, rolename):
                Voter.__init__(self, game, rolename)
                self.role = "Townie"
                
        def gameStart(self):
                Voter.gameStart(self)
                self.game.tell("Role: Townie", self.game.names[self])
                self.game.commentary(self.game.names[self] + ": " + "Townie")

class Game_MTTTL(Game):
        def __init__(self, players, announce, tell, commentary, gameover):
                self.roles = [SerialKiller, Townie, Townie, Lyncher, Lynchee]
                rolenames = [("Mafia", "Mafia"), ("Townie", "Townie"), ("Townie", "Townie"), ("Townie", "Townie"), ("Lynchee", "Townie"), ("Lyncher", "Lyncher")]
                Game.__init__(self, self.roles, players, rolenames, announce, tell, commentary)
                self.game_over = gameover
                self.announce("Game started. Get with the lynching!")
                
        def mkNight(self):
                for votee in self.votees:
                        if (len(self.votees[votee]) >= (len(self.voters) / 2 + 1)):
                                deadp = votee
                                if (deadp == "NL"):
                                        self.deadp = None
                                        self.announce("It is now night. Zzz...")
                                        Game.mkNight(self)
                                        return
                                elif (deadp.role == "Lynchee"):
                                        self.announce("The Lyncher, " + self.get_role("Lyncher") + " has gotten his target lynched! Lyncher win!")
                                        self.game_over()
                                elif ((deadp.role != "SK") and (len(self.voters) <= 3)):
                                        self.announce("The mafia, " + self.get_role("SK") + ", has gained dominance over the town! Mafia win!")
                                elif (deadp.role == "SK"):
                                        self.announce("The town has lynched the mafia! Town win!")
                                        if (self.get_role("Lyncher") != None):
                                                self.announce("Lyncher was " + self.get_role("Lyncher") + ".")
                                                self.announce("Lynchee was " + self.get_role("Lynchee") + ".")
                                else:
                                        self.deadp = deadp
                                        self.deadp_name = self.names[deadp]
                                        self.removePlayer(self.names[deadp])
                                        self.announce("It is now night. Zzz...")
                                        Game.mkNight(self)
                                        return
                self.game_over()
        
        def mkDay(self):
                self.announce("Daytime! " + self.nk + " was killed during the night.")
                self.announce(self.nk + " was a " + self.roles[self.nk].role + ".")
                self.removePlayer(self.nk)
                if (self.deadp != None):
                        self.announce("Yesterday's lynch, " + self.deadp_name + ", was a " + self.deadp.role + ".")
                Game.mkDay(self)

class Game_MTTTJ(Game):
        def __init__(self, players, announce, tell, commentary, gameover):
                self.roles = [SerialKiller, Townie, Townie, Townie, Jester]
                rolenames = [("Mafia", "Mafia"), ("Townie", "Townie"), ("Townie", "Townie"), ("Townie", "Townie"), ("Townie", "Townie"), ("Jester", "Jester")]
                Game.__init__(self, self.roles, players, rolenames, announce, tell, commentary)
                self.game_over = gameover
                self.announce("Game started. Get with the lynching!")
                
        def mkNight(self):
                for votee in self.votees:
                        if (len(self.votees[votee]) >= (len(self.voters) / 2 + 1)):
                                deadp = votee
                                if (deadp == "NL"):
                                        self.deadp = None
                                        self.announce("It is now night. Zzz...")
                                        Game.mkNight(self)
                                        return
                                elif (deadp.role == "Jester"):
                                        self.announce("The Jester, " + self.get_role("Jester") + " has gotten himself lynched! Jester win!")
                                        self.game_over()
                                elif ((deadp.role != "SK") and (len(self.voters) <= 3)):
                                        self.announce("The mafia, " + self.get_role("SK") + ", has gained dominance over the town! Mafia win!")
                                elif (deadp.role == "SK"):
                                        self.announce("The town has lynched the mafia! Town win!")
                                        if (self.get_role("Jester") != None):
                                                self.announce("Jester was " + self.get_role("Jester") + ".")
                                else:
                                        self.deadp = deadp
                                        self.deadp_name = self.names[deadp]
                                        self.removePlayer(self.names[deadp])
                                        self.announce("It is now night. Zzz...")
                                        Game.mkNight(self)
                                        return
                self.game_over()
        
        def mkDay(self):
                self.announce("Daytime! " + self.nk + " was killed during the night.")
                self.announce(self.nk + " was a " + self.roles[self.nk].role + ".")
                self.removePlayer(self.nk)
                if (self.deadp != None):
                        self.announce("Yesterday's lynch, " + self.deadp_name + ", was a " + self.deadp.role + ".")
                Game.mkDay(self)

class Game_MTTT(Game):
        def __init__(self, players, announce, tell, commentary, gameover):
                self.roles = [SerialKiller, Townie, Townie, Townie]
                rolenames = [("Mafia", "Mafia"), ("Townie", "Townie"), ("Townie", "Townie"), ("Townie", "Townie"), ("Townie", "Townie")]
                Game.__init__(self, self.roles, players, rolenames, announce, tell, commentary)
                self.game_over = gameover
                self.announce("Game started. Get with the lynching!")
                
        def mkNight(self):
                for votee in self.votees:
                        if (len(self.votees[votee]) >= (len(self.voters) / 2 + 1)):
                                deadp = votee
                                if (deadp == "NL"):
                                        self.deadp = None
                                        self.announce("It is now night. Zzz...")
                                        Game.mkNight(self)
                                        return
                                elif (deadp.role == "Jester"):
                                        self.announce("The Jester, " + self.get_role("Jester") + " has gotten himself lynched! Jester win!")
                                        self.game_over()
                                elif ((deadp.role != "SK") and (len(self.voters) <= 3)):
                                        self.announce("The mafia, " + self.get_role("SK") + ", has gained dominance over the town! Mafia win!")
                                elif (deadp.role == "SK"):
                                        self.announce("The town has lynched the mafia! Town win!")
                                        if (self.get_role("Jester") != None):
                                                self.announce("Jester was " + self.get_role("Jester") + ".")
                                else:
                                        self.deadp = deadp
                                        self.deadp_name = self.names[deadp]
                                        self.removePlayer(self.names[deadp])
                                        self.announce("It is now night. Zzz...")
                                        Game.mkNight(self)
                                        return
                self.game_over()
        
        def mkDay(self):
                self.announce("Daytime! " + self.nk + " was killed during the night.")
                self.announce(self.nk + " was a " + self.roles[self.nk].role + ".")
                self.removePlayer(self.nk)
                if (self.deadp != None):
                        self.announce("Yesterday's lynch, " + self.deadp_name + ", was a " + self.deadp.role + ".")
                Game.mkDay(self)                

class Game_MTTJ(Game):
        def __init__(self, players, announce, tell, commentary, gameover):
                self.roles = [SerialJester, Townie, Townie, Jester]
                rolenames = [("SerialJester", "SerialJester"), ("Townie", "Townie"), ("Townie", "Townie"), ("Jester", "Jester")]
                Game.__init__(self, self.roles, players, rolenames, announce, tell, commentary)
                self.game_over = gameover
                self.announce("Game started. Get with the lynching!")
                
        def mkNight(self):
                for votee in self.votees:
                        if (len(self.votees[votee]) >= (len(self.voters) / 2 + 1)):
                                deadp = votee
                                if (deadp == "NL"):
                                        self.deadp = None
                                        self.announce("It is now night. Zzz...")
                                        Game.mkNight(self)
                                        return
                                elif (deadp.role == "Jester"):
                                        self.announce("The Jester, " + self.get_role("Jester") + " has gotten himself lynched! Jester win!")
                                        self.game_over()
                                elif ((deadp.role != "SJ") and (len(self.voters) <= 2)):
                                        self.announce("The Serial Jester, " + self.get_role("SJ") + ", has gained dominance over the town! Town win!")
                                elif (deadp.role == "SJ"):
                                        self.announce("The town has lynched the Serial Jester! Serial Jester win!")
                                        if (self.get_role("Jester") != None):
                                                self.announce("Jester was " + self.get_role("Jester") + ".")
                                else:
                                        self.deadp = deadp
                                        self.deadp_name = self.names[deadp]
                                        self.removePlayer(self.names[deadp])
                                        self.announce("It is now night. Zzz...")
                                        Game.mkNight(self)
                                        return
                self.game_over()
        
        def mkDay(self):
                self.announce("Daytime! " + self.nk + " was killed during the night.")
                self.announce(self.nk + " was a " + self.roles[self.nk].role + ".")
                self.removePlayer(self.nk)
                if (self.deadp != None):
                        self.announce("Yesterday's lynch, " + self.deadp_name + ", was a " + self.deadp.role + ".")
                elif ((deadp.role != "SJ") and (len(self.voters) <= 2)):
                        self.announce("The Serial Jester, " + self.get_role("SJ") + ", has gained dominance over the town! Town win!")        
                Game.mkDay(self)
                
games["mtttl"] = (Game_MTTTL, 5)
games["mtttj"] = (Game_MTTTJ, 5)
games["mttt"] = (Game_MTTT, 4)
games["mttj"] = (Game_MTTJ, 4)