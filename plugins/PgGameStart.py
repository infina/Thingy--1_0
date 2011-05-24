from plugin import CommandsPlugin
import game
import manual

class PgSignups(CommandsPlugin):
        def event(self, event):
                if (self.bot.game == None): #Only activate when there's not a game on
                        CommandsPlugin.event(self, event)

        def cmd_nickchange(self, text, sender, senderMode, action, private, respondee):
                if (self.bot.players == None):
                        self.bot.client.sayTo("%s, ERROR, NO GAME." % sender, sender)
                        return
                
                args = text.split(" ")
                if (args[1] in self.bot.players):
                        self.bot.players.remove(args[1])
                        self.bot.players.append(args[2])
                        self.bot.client.announce("%s has been recorded as '%s'." % (args[1], args[2]))
                        return

                if (args[1] in self.bot.mod):
                        self.bot.mod = args[2]
                        self.bot.client.announce("%s has been recorded as '%s'." % (args[1], args[2]))
                        return
                
        def cmd_signups(self, text, sender, senderMode, action, private, respondee):
                """Starts signups for a game, manual or automatic"""
                if (self.bot.players != None):
                        self.bot.client.sayTo("%s, %s is already starting a game. Don't be rude." % (sender, self.bot.mod), respondee)
                        return
                
                args = text.split(" ")
                if len(args) > 1: #A game type has been specified.
                        if (args[1] in game.games): #If the game type is found
                                self.bot.gameType = game.games[args[1]][0]
                                self.bot.num_players = game.games[args[1]][1]
                                self.bot.client.announce("New %s game signups started by %s. Join all." % (args[1], sender))
                                chan = open('channel', 'r')
                                channel = chan.read()
                                self.bot.client.checktopic(channel)
                                #source = self.bot.game.players
                                #numplayers = len(source)
                                #playerlist = "Players: " + ", ".join(source)
                                #self.bot.client.prepend("%s's %s game %s %s" % (sender, args[1], numplayers, playerlist))
                        else:
                                self.bot.client.sayTo("%s, there is no gametype by the name '%s'." % (sender, args[1]), respondee)
                                return
                
                else: #Manual game
                        self.bot.client.announce("New manual game signups started by %s. Join all." % sender)
                        self.num_players = None
                        self.gameType = manual.Game_Manual
                
                self.bot.players = []
                self.bot.mod = sender

                        
        def cmd_join(self, text, sender, senderMode, action, private, respondee):
                """Used by a player to join the game"""
                if (self.bot.players == None): #There is no game active
                        self.bot.client.sayTo("%s, there is no game active." % sender, respondee)
                        return
                
                if (sender in self.bot.players): #A player tried to join twice.
                        self.bot.client.sayTo("%s, you can't join twice" % sender, respondee)
                        return
                        
                self.bot.players.append(sender)
                self.bot.client.announce(sender + " is now in the game.")
                                                        
                if (len(self.bot.players) == self.bot.num_players): #If there are enough players, start
                        self.bot.mod = None
                        self.bot.client.announce("Game has enough players, starting.")
                        self.bot.game = self.bot.gameType(self.bot.players, self.bot.client.announce, self.bot.client.sayTo, self.bot.commentary, self.bot.game_over)
                        
        def cmd_part(self, text, sender, senderMode, action, private, respondee):
                """Used by a player to leave the game"""
                if (self.bot.players == None): #Is there a game active?
                        self.bot.client.sayTo("%s, there is no game active." % sender, respondee)
                        return
                        
                if not(sender in self.bot.players):
                        self.bot.client.sayTo("%s, you're not in the game." % sender, respondee)
                        return
                        
                self.bot.players.remove(sender)
                self.bot.client.announce("%s has left the game." % sender)
        
        def cmd_end(self, text, sender, senderMode, action, private, respondee):
                """Used to end signups, either by the moderator or a channel operator"""
                if not(((sender == self.bot.mod) or (senderMode >= 2)) and self.bot.mod != None):
                        return
                
                self.bot.game_over()
                self.bot.client.announce("The game was snuffed out before it could even begin. :'-(")
                chan = open('channel', 'r')
                channel = chan.read()
                topicfile = open('topic', 'r')
                topic = topicfile.read()
                self.bot.client.topicset("%s" % topic)
        
        def cmd_roles(self, text, sender, senderMode, action, private, respondee):
                self.bot.rolenames = []
                roles = text.split(" ")[1:]

                for role in roles:
                        rolename = role.split(":", 1)[0]
                        if (len(role.split(":")) > 1):
                                displayname = role.split(":", 1)[1]
                        else:
                                displayname = rolename
                        self.bot.rolenames.append((rolename, displayname))
                
                self.bot.client.announce("Roles set")
        
        def cmd_start(self, text, sender, senderMode, action, private, respondee):
                if (self.bot.players == None): #If there is no game on, skip
                        return
                        
                if not((sender == self.bot.mod) and (self.bot.num_players == None)): #If the sender is not the mod, or the game is automatically started, skip
                        return
                
                roles = []
                if (self.bot.rolenames != None): #If there are rolenames set
                        if (len(self.bot.rolenames) == len(self.bot.players)): #If they are of the correct amount
                                roles = [] #assign them
                                for player in self.bot.players:
                                        roles.append(game.Manual)
                        else:
                                self.bot.client.sayTo("The amount of players differs from the amount of roles. The game can't start", respondee)
                                return
                else:
                        self.bot.rolenames = []
                        for player in self.bot.players:
                                self.bot.rolenames.append(("Voter", "Voter"))
                
                self.bot.game = manual.Game_Manual(self.bot.players, self.bot.rolenames, self.bot.client.announce, self.bot.client.sayTo, self.bot.commentary)
                self.bot.client.announce("Game started.")
                source = self.bot.game.roles
                numplayers = len(source)
                playerlist = "Players: " + ", ".join(source)
                self.bot.client.prepend("%s's game %s %s" % (sender, numplayers, playerlist))