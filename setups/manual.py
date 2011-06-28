from game import Game
from role import Voter


class Role_Manual(Voter):
        def __init__(self, game, rolename="Voter"):
                Voter.__init__(self, game, rolename)
                self.role = rolename
                
                
        def gameStart(self):
                """When the game starts up, this is called."""
                Voter.gameStart(self)
                self.game.tell("Role: " + self.role[1] + ".", self.game.names[self])
                self.game.commentary(self.game.names[self] + ": " + self.rolename[0])

        def __str__(self):
                return self.rolename[0]
                
class Game_Manual(Game):
        def __init__(self, players, rolenames, announce, tell, commentary):
                roles = []
                for rolename in rolenames:
                        roles.append(Role_Manual)
                Game.__init__(self, roles, players, rolenames, announce, tell, commentary)
                
        def modCmd(self, msg):
                cmd = msg.split()
                
                if (cmd[0] == "!day"):
                        #if (cmd[1] == "voice"):
                         #   self.playernumber = 0
                          #  for len(players):
                           #     self.playernumber ++
                            #    self.bot.client.sayTo("MODE #xkcdmafia +v %s" % player[playernumber])
                            #return
                        #return
                        self.mkDay()
                        self.announce("It is now day.")
                        
                            
                            
                elif (cmd[0] == "!night"):
                        #if (cmd[1] == "silent"):
                         #   playernumber = 0
                          #  for len(players):
                         #       playernumber ++
                          #      self.bot.client.sayTo("MODE #xkcdmafia -v %s" % player[playernumber])
                           # return
                        #return
                        self.mkNight()
                        self.announce("Night time. Zzz...")
                
                elif (cmd[0] == "!dead"):
                        if not(cmd[1] in self.roles):
                                self.announce("There is no player by that name to make dead.")
                                return
                        self.removePlayer(cmd[1])
                        self.announce(cmd[1] + " is now dead.")
                        
                elif (cmd[0] == "!insert"):
                        self.insert(cmd[1], Role_Manual, ("Voter", "Voter"))
                        self.announce(cmd[1] + " is now in the game")

                elif (cmd[0] == "!unmodchan"):
                      self.client.sayTo("/MODE #xkcdmafia -m")

                elif (cmd[0] == "!modchan"):
                    self.client.sayTo("/MODE #xkcdmafia +m")