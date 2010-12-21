class PluginBase(object):
        def __init__(self, bot):
                self.bot = bot #Link back to Thingy
                self.name = None #Plugin's name
        
        def event(self, event):
                pass
        
class CommandsPlugin(PluginBase):
        """A plugin that has every command as a function. !start calls the function cmd_start and so on. No more giant elifs for commands"""
        def __init__(self, bot, cmdChar = '!'):
                PluginBase.__init__(self, bot)
                self.cmdChar = cmdChar
        
        def event(self, event):
                if (event.type != "message"): #A kick or somesuch isn't a command
                        return
                
                if (event.text[0] != self.cmdChar): #Only interested in words that start with the command characer
                        return
                
                cmd = event.text.split(" ")[0][1:] #First word, without the command character
                funcName = "cmd_" + cmd #Function name is like this: cmd_<command name>
                
                if hasattr(self, funcName): #Check if there's a function with the name cmd_<command word> in the class
                        getattr(self, funcName)(event.text, event.sender, event.senderMode, event.action, event.private, event.respondee)