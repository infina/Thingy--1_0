from plugin import CommandsPlugin

class PgGameMisc(CommandsPlugin):
        def cmd_players(self, text, sender, senderMode, action, private, respondee):
                if (self.bot.game == None):
                        source = self.bot.players
                else:
                        source = self.bot.game.roles
                
                if (source == None):
                        self.bot.client.sayTo("%s, there is no game active" % sender, respondee)
                else:
                        self.bot.client.announce("Players: " + ", ".join(source))
        
        def cmd_votecount(self, text, sender, senderMode, action, private, respondee):
                if (self.bot.game != None):
                        self.bot.client.announce("Votes: " + self.bot.game.votecount())
                        
        def cmd_mod(self, text, sender, senderMode, action, private, respondee):
                if (senderMode >= 2) and (self.bot.game != None):
                        self.bot.modCmd(sender, text.split(" ", 1)[1], private, senderMode)

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
                