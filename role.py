class Role:
        def __init__(self, game, rolename):
                self.game = game
                self.rolename = rolename
        
        def gameStart(self):
                pass

class Voter(Role):
        def __init__(self, game, rolename):
                Role.__init__(self, game, rolename)
                
        def gameStart(self):
                self.game.voters[self] = None
                self.game.votees[self] = []
        
        def vote(self, target):
                self.trueTarget = None
                for player in self.game.roles:
                    if target.upper() == player.upper():
                        if (self.game.voters[self] == self.game.roles[player]):
                            self.game.announce("You are already voting for that person")
                            return
                        
                        if (self.game.voters[self] != None):
                            self.unvote()
                        
                        self.game.voters[self] = self.game.roles[player]
                        self.game.votees[self.game.roles[player]].append(self)
                        
                        if self.game.majorityCheck():
                            self.game.announce("A majority has been reached for " + player +"!")
                            self.game.announce(self.game.votecount())
                            self.game.mkNight()
                            return
                        
                        self.game.announce(self.game.votecount())
                        return
                        
                self.game.announce("There is no player by that name to vote for")
                return            
                
        def unvote(self):
                if (self.game.voters[self] == None):
                        self.game.announce("You have no vote to unvote")
                
                self.game.votees[self.game.voters[self]].remove(self)
                self.game.voters[self] = None
                
        def nolynch(self):
                if (self.game.voters[self] != None):
                        self.unvote()

                self.game.voters[self] = "NL"
                self.game.votees["NL"].append(self)

                if self.game.majorityCheck():
                        self.game.announce(self.game.votecount())
                        self.game.announce("The town has decided to lynch no one.")
                        self.game.mkNight()
                else:
                        self.game.announce(self.game.votecount())
        
        def action(self, msg):
                args = msg.split(" ")
                if (self.game.phase == "day"):
                        if (args[0] == "vote"):
                                self.vote(args[1])
                        elif (args[0] == "unvote"):
                                self.unvote()
                                self.game.announce(self.game.votecount())
                        elif (args[0] == "nolynch"):
                                self.nolynch()