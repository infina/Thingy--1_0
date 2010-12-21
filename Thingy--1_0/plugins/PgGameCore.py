from plugin import PluginBase

class PgGameCore(PluginBase):
        def __init__(self, bot):
                PluginBase.__init__(self, bot)
                self.name = "PgSystem"
        
        def event(self, event):
                if (event.type == "message") and (self.bot.game != None): #Only applies when there's a game on
                        if (event.sender == self.bot.mod): #Handles mod commands for manual games
                                self.bot.modCmd(event.sender, event.text, event.private, event.senderMode)
                        
                        elif (event.sender in self.bot.game.roles): #handles player actions
                                if (event.text[0] == '!'): #Command char signifies an action                                        
                                        self.bot.game.action(event.sender, event.text[1:]) #Chop off command char
                                elif (event.action): #Emote also signifies action
                                        self.bot.game.action(event.sender, event.text) #No command character to chop off