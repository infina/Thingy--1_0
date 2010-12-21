from game import Game, games
from role import Voter
import random

class Shirts_Delusional(Voter):
        def __init__(self, game, rolename):
                Voter.__init__(self, game, rolename)
                self.role = "Delusional"
                self.description = game.descriptions.pop()
                
        def gameStart(self):
                Voter.gameStart(self)
                sk_name = self.game.get_role("Sane")
                self.game.tell("Role: Witness", self.game.names[self])
                self.game.tell("You: " + self.description, self.game.names[self])
                self.game.tell("You saw: " + self.game.roles[sk_name].description, self.game.names[self])
                
                self.game.commentary(self.game.names[self] + ": " + "Delusional Witness")
                
class Shirts_Sane(Voter):
        def __init__(self, game, rolename):
                Voter.__init__(self, game, rolename)
                self.role = "Sane"
                self.description = game.descriptions.pop()
                
        def gameStart(self):
                Voter.gameStart(self)
                sk_name = self.game.get_role("SK")
                self.game.tell("Role: Witness", self.game.names[self])
                self.game.tell("You: " + self.description, self.game.names[self])
                self.game.tell("You saw: " + self.game.roles[sk_name].description, self.game.names[self])
                
                self.game.commentary(self.game.names[self] + ": " + "Sane Witness")
                
class Shirts_SerialKiller(Voter):
        def __init__(self, game, rolename):
                Voter.__init__(self, game, rolename)
                self.role = "SK"
                self.description = game.descriptions.pop()
                
        def gameStart(self):
                Voter.gameStart(self)
                self.game.tell("Role: Murderer", self.game.names[self])
                self.game.tell("You: " + self.description, self.game.names[self])
                self.game.commentary(self.game.names[self] + ": " + "Murderer")

class Game_Shirts(Game):
        def __init__(self, players, announce, tell, commentary, gameover):
                roles = [Shirts_Delusional, Shirts_Sane, Shirts_SerialKiller]
                rolenames = [('Sane', 'Sane'), ('Delusional', 'Sane'), ('Serial Killer', 'Serial Killer')]
                self.descriptions = ["Red Shirt", "Green Shirt", "Blue Shirt"]
                announce("Colours: " + ", ".join(self.descriptions))
                random.shuffle(self.descriptions)
                Game.__init__(self, roles, players, rolenames, announce, tell, commentary)
                self.game_over = gameover
                self.announce("Game started. Get with the lynching!")
                
        def mkNight(self):
                for votee in self.votees:
                        if (len(self.votees[votee]) >= (len(self.voters) / 2 + 1)):
                                deadp = votee
                                if (deadp.role == "SK"):
                                        self.announce("The Murderer has been lynched. Town wins!")
                                else:
                                        self.announce("An innocent witness has been hung. " + self.get_role("SK") + ", the murderer, kills the last townie and wins!")
                                self.game_over()

games["shirts"] = (Game_Shirts, 3)