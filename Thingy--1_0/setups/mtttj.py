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

                
class Jester(Voter):
        def __init__(self, game, rolename):
                Voter.__init__(self, game, rolename)
                self.role = "Jester"
                
        def gameStart(self):
                Voter.gameStart(self)
                self.game.tell("Role: Jester", self.game.names[self])
                self.game.commentary(self.game.names[self] + ": " + "Jester")
                
class Townie(Voter):
        def __init__(self, game, rolename):
                Voter.__init__(self, game, rolename)
                self.role = "Townie"
                
        def gameStart(self):
                Voter.gameStart(self)
                self.game.tell("Role: Townie", self.game.names[self])
                self.game.commentary(self.game.names[self] + ": " + "Townie")

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
                
games["mtttj"] = (Game_MTTTJ, 5)