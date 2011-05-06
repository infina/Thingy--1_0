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