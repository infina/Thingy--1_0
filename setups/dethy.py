from game import Game, games
from role import Voter
import random

x = 0
class SerialKiller(Voter):
        def __init__(self, game, rolename):
                Voter.__init__(self, game, rolename)
                self.role = "SK"
                self.alignment = "Scum"
                self.alignmentinsane = "Town"
                self.sanity = "Sane"
                
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

class SaneCop(Voter):
        def __init__(self, game, rolename):
                Voter.__init__(self, game, rolename)
                self.role = "SaneCop"
                self.alignment = "Town"
                self.alignmentinsane = "Scum"
                self.sanity = "Sane"
                
        def gameStart(self):
                Voter.gameStart(self)
                self.game.tell("Role: Cop", self.game.names[self])
                self.game.commentary(self.game.names[self] + ": " + "Sane Cop")
                
        def action(self, msg):
                args = msg.split(" ")
                if ((args[0] == "cop") and (self.game.phase == "night")):
                        if ((len(args) >= 2) and (args[1] in self.game.roles)):
                                if args[1] == self.game.get_role("SK"):
                                        self.game.tell(args[1] + " is Scum.", self.game.names[self])
                                        self.game.mkDay()
                                else:
                                        self.game.tell(args[1] + " is Town.", self.game.names[self])
                                        self.game.mkDay()
                        else:
                                self.game.tell("You must pick a valid target.", self.game.names[self])
                else:
                        Voter.action(self, msg)

class InsaneCop(Voter):
        def __init__(self, game, rolename):
                Voter.__init__(self, game, rolename)
                self.role = "InsaneCop"
                self.alignment = "Town"
                self.alignmentinsane = "Scum"
                self.sanity = "Insane"
                
        def gameStart(self):
                Voter.gameStart(self)
                self.game.tell("Role: Cop", self.game.names[self])
                self.game.commentary(self.game.names[self] + ": " + "Insane Cop")
                
        def action(self, msg):
                args = msg.split(" ")
                if ((args[0] == "cop") and (self.game.phase == "night")):
                        if ((len(args) >= 2) and (args[1] in self.game.roles)):
                                if args[1] == self.game.get_role("SK"):
                                        self.game.tell(args[1] + " is town", self.game.names[self])
                                        self.game.mkDay()
                                else:
                                        self.game.tell(args[1] + " is scum", self.game.names[self])
                                        self.game.mkDay()
                        else:
                                self.game.tell("You must pick a valid target.", self.game.names[self])
                else:
                        Voter.action(self, msg)

class ParanoidCop(Voter):
        def __init__(self, game, rolename):
                Voter.__init__(self, game, rolename)
                self.role = "ParanoidCop"
                self.alignment = "Town"
                self.alignmentinsane = "Scum"
                self.sanity = "Paranoid"
                
        def gameStart(self):
                Voter.gameStart(self)
                self.game.tell("Role: Cop", self.game.names[self])
                self.game.commentary(self.game.names[self] + ": " + "Paranoid Cop")
                
        def action(self, msg):
                args = msg.split(" ")
                if ((args[0] == "cop") and (self.game.phase == "night")):
                        if ((len(args) >= 2) and (args[1] in self.game.roles)):
                                self.game.cop = args[1]
                                self.game.tell(args[1] + " is Scum.", self.game.names[self])
                                self.game.mkDay()
                        else:
                                self.game.tell("You must pick a valid target.", self.game.names[self])
                else:
                        Voter.action(self, msg)

class NaiveCop(Voter):
        def __init__(self, game, rolename):
                Voter.__init__(self, game, rolename)
                self.role = "NaiveCop"
                self.alignment = "Town"
                self.alignmentinsane = "Scum"
                self.sanity = "Naive"
                
        def gameStart(self):
                Voter.gameStart(self)
                self.game.tell("Role: Cop", self.game.names[self])
                self.game.commentary(self.game.names[self] + ": " + "Naive Cop")
                
        def action(self, msg):
                args = msg.split(" ")
                if ((args[0] == "cop") and (self.game.phase == "night")):
                        if ((len(args) >= 2) and (args[1] in self.game.roles)):
                                self.game.cop = args[1]
                                self.game.tell(args[1] + " is Town." , self.game.names[self])
                                self.game.mkDay()
                        else:
                                self.game.tell("You must pick a valid target.", self.game.names[self])
                else:
                        Voter.action(self, msg)

class RandomCop(Voter):
        def __init__(self, game, rolename):
                Voter.__init__(self, game, rolename)
                self.role = "RandomCop"
                self.alignment = "Town"
                self.alignmentinsane = "Scum"
                self.sanity = "Random"
                
        def gameStart(self):
                Voter.gameStart(self)
                self.game.tell("Role: Cop", self.game.names[self])
                self.game.commentary(self.game.names[self] + ": " + "Random Cop")
                
        def action(self, msg):
                args = msg.split(" ")
                if ((args[0] == "cop") and (self.game.phase == "night")):
                        if ((len(args) >= 2) and (args[1] in self.game.roles)):
                                self.game.cop = args[1]
                                randalign = random.choice(['Scum','Town'])
                                self.game.tell(args[1] + " is %s." % randalign, self.game.names[self])
                                self.game.mkDay()
                        else:
                                self.game.tell("You must pick a valid target.", self.game.names[self])
                else:
                        Voter.action(self, msg)
                       


class Game_Dethy(Game):
        def __init__(self, players, announce, tell, commentary, gameover):
                self.roles = [SerialKiller, SaneCop, InsaneCop, ParanoidCop, NaiveCop, RandomCop]
                rolenames = [("Mafia", "Mafia"), ("Cop", "Cop"),("Cop", "Cop"), ("Cop", "Cop"), ("Cop", "Cop"), ("Cop", "Cop")]
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
                if self.game.x == 6:
                        self.announce("Daytime! " + self.nk + " was killed during the night.")
                        self.announce(self.nk + " was a " + self.roles[self.nk].role + ".")
                        self.removePlayer(self.nk)
                        if (self.deadp != None):
                                self.announce("Yesterday's lynch, " + self.deadp_name + ", was a " + self.deadp.role + ".")
                        Game.mkDay(self)
                        self.game.x = 0
                else:
                        self.game.x = self.game.x + 1


games["dethy"] = (Game_Dethy, 6)