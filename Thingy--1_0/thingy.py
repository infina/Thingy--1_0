import game
import os
import sys
import traceback

help = [
"To start signups, use !signups",
"To join a game in signups use !join",
"To leave a game in signups, use !part",
"To start the game in Day 1 once signups are complete, use !start",
"To declare day after night, use !day",
"To manually make it night, use !night",
"To vote, use !vote",
"To unvote, use !unvote",
"To nolynch, use !nolynch",
"To declare a player dead, use !dead",
"To get a votecount, use !votecount",
"To get a list of active players, use !players"
]

class Thingy(object):
        def __init__(self, interface):
                self.interface = interface
                
                self.game = None
                self.players = None
                self.mod = None
                self.rolenames = None
                self.num_players = None
                
                self.getSetups()
                self.getPlugins()
        
        @property
        def client(self):
                return self.interface.client
        
        def event(self, event):
                for pluginFile in self.pluginList:
                        for plugin in self.pluginList[pluginFile]:
                                try:
                                        plugin.event(event)
                                except SystemExit:
                                        print "Terminating."
                                        sys.exit(0)
                                except:
                                        self.client.sayTo("%s, unhandled error. Dumping debugging information." % event.sender, event.respondee)
                                        print traceback.print_exc()


        def modCmd(self, sender, msg, private, mode):
                cmd = msg.split(" ", 1)[0]
                
                if (cmd == "!end"):
                        self.game_over()
                        self.client.announce("The game is over")
                else:
                        self.game.modCmd(msg)

        def commentary(self, msg):
                if (self.mod != None):
                        self.client.sayTo(msg, self.mod)
                
        def game_over(self):
                self.game = None
                self.mod = None
                self.players = None
                self.rolenames = None
                self.num_players = None
                
        def getPlugins(self):
                """Reads the plugin files from the given subfolder and then tries to reload each one. If it fails reloading it imports it.
                This is to double both as a reload function and as an initial import function. It also detects new plugin files on reload this way."""
                
                subfolder = "plugins"
                self.pluginPath = os.path.join(os.getcwd(), subfolder)
                self.pluginFiles = []
                self.pluginList = {}
                
                for file in os.listdir(self.pluginPath): #Get the modules stored in the plugin directory
                        if ((file[-3:] == '.py') and (file[:2] != '__')): #Check that it's a .py file but ignore the boilerplate file __
                                self.pluginFiles.append(file[:-3]) #Trim the .py
                                
                sys.path.append(self.pluginPath) #Add the plugin folder to the places Python searches for modules
                for file in self.pluginFiles: #Get the plugins in each module and import/reload the module.
                        try:
                                fileM = reload(sys.modules[file])
                                print 'Reloaded: ' + os.path.join(self.pluginPath, file)
                        except KeyError:
                                fileM = __import__(file)
                                print 'Imported: ' + os.path.join(self.pluginPath, file)
                        
                        self.pluginList[file] = []
                        for plugin in dir(fileM):
                                if (plugin[:2] != '__') and (plugin[:2] == 'Pg'): #Skipping module stuff and the Base plugin so that just the plugin classes are processed
                                        print '\tGetting ' + plugin
                                        self.pluginList[file].append(getattr(fileM, plugin)(self))
                print 'Done getting plugins.'
                
        def getSetups(self):
                """Reads the setups files from the given subfolder and then tries to reload each one. If it fails reloading it imports it.
                This is to double both as a reload function and as an initial import function. It also detects new setup files on reload this way."""
                
                subfolder = "setups"
                self.setupPath = os.path.join(os.getcwd(), subfolder)
                self.setupFiles = []
                
                for file in os.listdir(self.setupPath): #Get the modules stored in the plugin directory
                        if ((file[-3:] == '.py') and (file[:2] != '__')): #Check that it's a .py file but ignore the boilerplate file __
                                self.setupFiles.append(file[:-3]) #Trim the .py
                                
                sys.path.append(self.setupPath) #Add the setup folder to the places Python searches for modules
                for file in self.setupFiles: #Import/Reload each module.
                        try:
                                fileM = reload(sys.modules[file])
                                print 'Reloaded: ' + os.path.join(self.setupPath, file)
                        except KeyError:
                                fileM = __import__(file)
                                print 'Imported: ' + os.path.join(self.setupPath, file)
        
                print 'Done getting setups.'
