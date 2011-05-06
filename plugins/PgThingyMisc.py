from plugin import CommandsPlugin
from irc_client import modeValues
import cPickle as pickle
import os

class PgThingyMassPing(CommandsPlugin):
        def __init__(self, bot):
                CommandsPlugin.__init__(self, bot)
                self.inputData()
                
        def cmd_noping(self, text, sender, senderMode, action, private, respondee):
                if (sender in self.optout):                        
                        self.bot.client.sayTo("%s, you have already opted-out." % sender, respondee)
                        return
                
                self.optout.append(sender) #Add opt-outer to list
                self.outputData() #Output list to file
                self.bot.client.sayTo("%s, You have opted-out from being mass pinged." % sender, respondee)
                
        def cmd_doping(self, text, sender, senderMode, action, private, respondee):
                try:
                        self.optout.remove(sender) #Add opt-outer to list
                        self.outputData() #Output list to file
                        self.bot.client.sayTo("%s, You will now be mass pinged." % sender, respondee)
                except ValueError:
                        self.bot.client.sayTo("%s, you have not opted-out." % sender, respondee)
                
        def cmd_massping(self, text, sender, senderMode, action, private, respondee):
                names = []
                for name in self.bot.client.modes:
                        if ((name != self.bot.client.nick) and (name != sender) and not(name in self.optout)): #Don't ping the mass pinger or Thingy's nick
                                names.append(name)
                self.bot.client.announce("! ".join(names) + "!")
                self.bot.client.announce("Game time!")               

        def cmd_uberping(self, text, sender, senderMode, action, private, respondee):
                if (senderMode >= 2):
                    names = []
                    for name in self.bot.client.modes:
                        if ((name != self.bot.client.nick) and (name != sender)): #Don't ping the mass pinger or Thingy's nick
                                names.append(name)
                    self.bot.client.announce("! ".join(names) + "!")
                    self.bot.client.announce("Game time!")
                    return
                
        def outputData(self):
                dataFile = file(os.path.join('data', 'noping.pkl'), 'wb')
                pickle.dump(self.optout, dataFile, False)

        def inputData(self):
                try:
                        dataFile = file(os.path.join('data', 'noping.pkl'), 'rb')
                        self.optout = pickle.load(dataFile)
                except IOError:
                        self.optout = []

                        
