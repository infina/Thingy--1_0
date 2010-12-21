import random

games = {}

class Game(object):
        def __init__(self, roles, players, rolenames, announce, tell, commentary):
                self.announce = announce
                self.tell = tell
                self.commentary = commentary
                self.phase = "startup"
                
                self.voters = {}
                self.votees = {"NL": []}
                
                random.shuffle(players)
                
                self.roles = {}
                self.names = {}
                
                for player in players:
                        self.insert(player, roles.pop(), rolenames.pop())
                self.phase = "day"
                
        def action(self, sender, msg):
                self.roles[sender].action(msg)
                
        def votecount(self):
                if (self.phase != "day"):
                        return "There is only voting during the day."
                        
                votes = []
                for votee in self.votees:
                        if (self.votees[votee] != []):
                                msg = str(len(self.votees[votee])) + " "
                                msg += self.names.get(votee, "NL") + " ("
                                voters = []
                                for voter in self.votees[votee]:
                                        voters.append(self.names[voter])
                                msg += ", ".join(voters) + ")"
                                votes.append(msg)
                ret = ", ".join(votes)
                
                if (ret == ""):
                       return "No votes. Get with the lynching"
                return ret
                
        def majorityCheck(self):
                for votee in self.votees:
                                if (len(self.votees[votee]) >= (len(self.voters) / 2 + 1)):
                                        return True
                return False
                
        def removePlayer(self, player):
                del self.voters[self.roles[player]]
                del self.votees[self.roles[player]]
                        
                for votee in self.votees:
                        if (self.roles[player] in self.votees[votee]):
                                self.votees[votee].remove(self.roles[player])
                        
                del self.names[self.roles[player]]
                del self.roles[player]
                
        def mkNight(self):
                self.phase = "night"
                self.clearVotes()

        def mkDay(self):
                self.phase = "day"

        def clearVotes(self):
                for votee in self.votees:
                        self.votees[votee] = []
                for voter in self.voters:
                        self.voters[voter] = None

        def insert(self, name, role, rolename):
                self.roles[name] = role(self, rolename)
                self.names[self.roles[name]] = name
                self.roles[name].gameStart()
                
        def get_role(self, rolename):
                for role in self.names:
                        if (role.role == rolename):
                                return self.names[role]
                return None

        