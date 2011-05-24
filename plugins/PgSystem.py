from plugin import PluginBase
import sys

class PgSystem(PluginBase):
        def __init__(self, bot):
                PluginBase.__init__(self, bot)
                self.name = "PgSystem"
        
        def event(self, event):
                if (event.type == "message"):                
                        if (event.senderMode >= 3):                        
                                if (event.text == "!reload_plugins"):
                                                        self.bot.getPlugins()
                                                        self.bot.client.respond(event, "Plugins reloaded.")
                                
                                elif (event.text == "!reload_thingy"):
                                        self.interface.reloadThingy()
                                        self.bot.client.announce("Reloaded.")
                                        
                                elif (event.text == "!reload_client"):
                                        self.bot.client.announce("Reconnecting...", True)
                                        self.bot.interface.reloadClient()
                                        
                                elif (event.text == "!restart"):
                                        self.bot.client.announce("Restarting.", True)
                                        self.bot.interface.reset()
                                
                                elif (event.text == "!quit"):
                                        self.bot.client.announce("Quitting. Bye all.", True)
                                        sys.exit(0)
