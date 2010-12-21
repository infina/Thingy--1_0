from game import Game, games
from role import Voter
import random
 
class Assassin(Voter):
        def __init__(self, game, rolename):
                Voter.__init__(self, game, rolename)
                self.role = "Assassin"
               
        def gameStart(self):
                Voter.gameStart(self)
                self.game.tell("Role: Assassin", self.game.names[self])
                self.game.commentary(self.game.names[self] + ": " + "Assassin")
               
        def action(self, msg):
                args = msg.split(" ")
                if ((args[0] == "kill") and (self.game.phase == "night" or self.game.phase == "day")):
                        if (deadp == "NK"):
                                        self.deadp = None
                                        self.announce("It is now night. Zzz...")
                               
                        elif   ((len(args) >= 2) and (args[1] in self.game.roles)):
                                self.game.nk = args[1]
                                self.game.tell(args[1] + " has been killed.", self.game.names[self])
                                self.game_over()
                                     
                        else:
                                self.game.tell("You must pick a valid target.", self.game.names[self])
                else:
                        Voter.action(self, msg)
class King(Voter):
        def __init__(self, game, rolename):
                Voter.__init__(self, game, rolename)
                self.role = "King"
               
        def gameStart(self):
                Voter.gameStart(self)
                self.game.tell("Role: King", self.game.names[self])
                self.game.commentary(self.game.names[self] + ": " + "King")
 
               
class Guard(Voter):
        def __init__(self, game, rolename):
                Voter.__init__(self, game, rolename)
                self.role = "Guard"
                self.target = self.game.get_role("King")
               
        def gameStart(self):
                Voter.gameStart(self)
                self.game.tell("Role: Guard for " + self.target, self.game.names[self])
                self.game.commentary(self.game.names[self] + ": " + "Guard")
 

class Game_SINS5(Game):
        def __init__(self, players, announce, tell, commentary, gameover):
                self.roles = [King, Assassin, Guard, Guard, Guard]
                rolenames = [("Assassin", "Assassin"), ("King", "King"), ("Guard", "Guard"), ("Guard", "Guard"), ("Guard", "Guard")]
                Game.__init__(self, self.roles, players, rolenames, announce, tell, commentary)
                self.game_over = gameover
                self.announce("Game started. Get with the lynching!")
               
        def mkDay(self):
                for votee in self.votees:
                        if (len(self.votees[votee]) >= (len(self.voters) / 2 + 1)):
                                deadp = votee
                                if (deadp == "NL"):
                                        self.deadp = None
                                        self.announce("Daytime!")
                                        Game.mkDay(self)
                                        return
                                elif (deadp.role == "King"):
                                        self.announce("The Assassin, " + self.get_role("Assassin") + " has gotten his target killed! Assassin win!")
                                        self.game_over()
                                        self.announce("The town has lynched the assassin! Town win!")
                                        if (self.get_role("King") != None):
                                                self.announce("King was " + self.get_role("King") + ".")
                                                
                                elif (deadp.role == "Assassin"):
                                        self.announce("The Assassin, " + self.get_role("Assassin") + " has gotten his killed! Town win!")
                                        self.game_over()
                                        self.announce("The town has lynched the assassin! Town win!")
                                        if (self.get_role("King") != None):
                                                self.announce("King was " + self.get_role("King") + ".")
                                else:
                                        self.deadp = deadp
                                        self.deadp_name = self.names[deadp]
                                        self.removePlayer(self.names[deadp])
                                        if (self.deadp != None):
                                            self.announce("Daytime! Yesterday's lynch, " + self.deadp_name + ", was a " + self.deadp.role + ".")
                                        Game.mkDay(self)
                                        return
                self.game_over()
       
                                
                
               
games["sins5"] = (Game_SINS5,5)