"""This module contains the irc client class, which handles the entire IRC interface"""

#This module is very comment heavy. I blame it on the crypticness of the IRC protocol

from socket import socket #For connecting to the IRC server
import time
import events
import base64

#Configuration. Later this might be moved to a settings module
nick = 'Thingyv2test'
altnick = 'Thingy2_0'
passfile = open('password','rb')
passbin = passfile.read()
password = base64.standard_b64decode(passbin) #'oA,"2!'
owner = 'infina'
server = 'irc.foonetic.net'
port = 6667
chan = open('channel','r')
channel = chan.read()
dead_lounge = '#xkcdmafiadead'
verf = open('version','r')
VERSION = verf.read()
rawlog = True
modeValues = {'+': 1, '%': 2, '@': 3, '&':4, '~':5}


class IRC_Client:
        """IRC stuff. Initialization takes a Thingy object, which it calls with relevant events"""
        def __init__(self, interface):
                self.interface = interface
                self.socket = socket() #Socket class
                self.socket.connect((server, port)) #Connect
                self.running = True
                self.namesResult = [] #Used for buffering information returned from names request
                self.modes = {} #Dictionary for storing users and their modes
                self.nick = nick
                
                self.sends = [] #A list of sends, so that sending multiple lines individually are sent together in a batch later
                self.rawlog = open('rawlog.dat', 'w')
                self.channellog = open('Channel.log', 'a')
                self.querylog = open('Queries.log', 'a')

                print ("Connecting to the server...")
                #Next two lines are required by IRC protocol to be first thing sent
                self.send('NICK %s' % nick) #Choose nickname
                self.send('USER %s * * :A bot of %s.' % (owner, owner)) #choose user name.
           
        def __del__(self):
                self.rawlog.close()
        
        @property
        def bot(self):
                return self.interface.bot
        
        def send(self, msg):
                """For sending a message to the IRC server. Attaches \r\n and prints debugging info."""
                self.rawlog.write('=> %s\n' % msg.rstrip())
                self.socket.send(msg + '\r\n')
                
        def join(self, chan):
                """Join a channel"""
                self.send('JOIN ' + chan)
        
        def loop(self):
                """Main loop for handling input from the socket. Thread blocking."""
                readbuffer = ''
                while self.running:
                        readbuffer = readbuffer + self.socket.recv(1024) #Top up the buffer
                        temp = readbuffer.split("\n")
                        readbuffer = temp.pop( ) #The last line is possibly half read
                        timenow = time.gmtime()
                        currenttime = ('%s-%s-%s %s:%s:%s UTC' % (timenow[0], timenow[1], timenow[2], timenow[3], timenow[4], timenow[5]))

                        for rawl in temp:
                                rawl = rawl.rstrip() #Remove trailing \r\n
                                self.rawlog.write("<= %s\n" % rawl)
                                line = rawl.split(" ") #Split for easier parsing
                                
                                #Respond to pings
                                if line[0] == "PING": #IRC server pings in the format PING :<data>
                                        self.send("PONG " + line[1]) #Reply PONG :<data>
        
                                #Once connected, do stuff
                                elif line[1] == "001": #IRC server signals welcome message in format <server> 001 <nick> <msg> 
                                        self.send("MODE " + nick + " +B") #Mark ourselves as a bot
                                        self.send("PRIVMSG NICKSERV IDENTIFY " + password) #Identify with Nickserv
                                        print ("Connected to the server.")

                                elif line[1] == "433":
                                        self.send('NICK %s' % altnick) #Choose nickname
                                        self.send("MODE " + nick + " +B")
                                        self.send("PRIVMSG NICKSERV GHOST " + nick + " " + password)
                                

                                elif line[1] == "332": #on topic change
                                        topic = open('topic', 'w')
                                        msg = ' '.join(line[4:])[1:]
                                        topic.write(msg)
                                        topic.close()
                                
                                      
        
                                #We've received a notice from nickserv
                                elif (line[0].startswith(":NickServ") and line[1] == "NOTICE" and line[2] == nick):
                                        if (' '.join(line[3:]) == ":You are now identified for thingyv2test."): #We're logged in
                                                print ("Identified with NickServ, now joining main channel.")
                                                self.join(channel)
                                        
                                #We've received a message in a channel or pm. (PRIVMSG is for channels as well.)
                                elif line[1] == "PRIVMSG": #Messages are of the form nick!username@machine.domain.tld PRIVMSG <channel> :<msg>
                                        
                                        if line[2] == nick: #The message is sent via pm if <channel> is equal to nick
                                                private = True #It's a private message
                                        else:
                                                private = False #It was said in a channel
                                        
                                        sender = line[0].split("!")[0][1:] #Extract the sender's nick
                                        msg = ' '.join(line[3:])[1:] #Patch together the actual message from the list of words and chop off the leading ':'
                                        if ((sender in self.modes) and (sender != '|')):
                                                mode = self.modes[sender]
                                        elif (sender == "|"):
                                                mode = 4
                                        else:
                                                mode = 0
                                        
                                        event = events.Message()
                                        event.sender = sender
                                        event.senderMode = mode
                                        event.private = private
                                        event.channel = line[2]
                                        
                                        if ((msg.startswith("ACTION ")) and (msg[-1] == "")): #If the message is an emote
                                                event.action = True
                                                event.text = msg[8:][:-1] #Chop off the SOH's and the ACTION bit
                                                if private == False:
                                                        self.channellog.write('[%s] %s %s\n' % (currenttime, sender, event.text))
                                                else:
                                                        self.querylog.write('[%s] %s %s\n' % (currenttime, sender, event.text))
                                        else:
                                                event.action = False
                                                event.text = msg
                                                if private == False:
                                                        self.channellog.write('[%s] <%s> %s\n' % (currenttime, sender, msg))
                                                else:
                                                        self.querylog.write('[%s] <%s> %s\n' % (currenttime, sender, msg))
                                                
                                        if (msg.startswith("VERSION")):
                                                sender = line[0].split("!")[0][1:]
                                                self.send("NOTICE %s :VERSION %s " % (sender, VERSION))
                                                print ("%s CTCP Version'd" % (sender))
                                                return
                                        
                                        if (msg.startswith("!mode") and (len(line) >= 4)):
                                                sender = line[0].split("!")[0][1:]
                                                self.send("MODE %s %s" % (channel, line[4]))
                                                print ("%s set mode %s on %s" % (sender, line[4], channel))
                                                return
                                        
                                        if (msg.startswith("!umode") and (len(line) >= 5)):
                                                sender = line[0].split("!")[0][1:]
                                                self.send("MODE %s %s %s" % (channel, line[5], line[4]))
                                                print ("%s set umode %s on %s" % (sender, line[5], line[4]))
                                                return
                                        
                                        self.bot.event(event) #Pass the message along

                                elif (line[1] == "JOIN") and (line[0].split("!", 1)[0] != ':' + nick): #A user joined. Second bit is to check that it isn't the bot joining the channel (in which case, the server automatically sends a names list without a request)
                                        self.refreshMembers() #Refresh the memberlist
                                        user = line[0].split("!")[0][1:]
                                        print ("%s joined" % (user))
                                
                                elif line[1] == "PART": #A user parted.
                                        self.refreshMembers()
                                        user = line[0].split("!")[0][1:]
                                        print ("%s parted" % (user))
                                        
                                elif line[1] == "KICK": #A user was kicked
                                        self.refreshMembers()
                                        user = line[0].split("!")[0][1:]
                                        print ("%s was kicked" % (user))
                                        
                                elif line[1] == "QUIT": #A user quit
                                        self.refreshMembers()
                                        user = line[0].split("!")[0][1:]
                                        print ("%s quit" % (user))
                                        
                                elif line[1] == "NICK": #A user changed their nick
                                        self.refreshMembers()
                                        user = line[0].split("!")[0][1:]
                                        newnick = line[2].split(":")[1]
                                        self.send("PRIVMSG %s :!zuowotmzsq %s %s" % (nick, user, newnick))
                                        self.channellog.write('%s is now known as %s\n' % (user, newnick))
                                        print ("%s changed their nick to %s" % (user, newnick))
                                        
                                elif (line[1] == "MODE") and (line[2] == channel): #A user's mode was changed. line[2] must equal channel, otherwise thingy twigs on setting itself +B
                                        self.refreshMembers()
                                        #print "A user's mode was changed"
                                
                                elif line[1] == "353": #A partial or full list of names in the channel
                                        line[5] = line[5][1:] #Chopping off : in front of first name
                                        self.namesResult.extend(line[5:]) #Names start at the sixth word
                                        
                                elif line[1] == "366": #Indicates end of sending names
                                        self.modes = {}
                                        for name in self.namesResult:
                                                if name[0] in modeValues:
                                                        self.modes[name[1:]] = modeValues[name[0]] #get number for each mode
                                                else:
                                                        self.modes[name] = 0 #No mode
                                        self.namesResult = [] #Clear the buffer
                                       #print "Modes reloaded:"
                                        #for user in self.modes:
                                        #        print "%s: level %s." % (user, self.modes[user])
                        
                        for send in self.sends: #This keeps the sends non-threadblocking
                                self.send(send)
                        self.sends = []
                        
        
        def refreshMembers(self):
                """Requests a new memberlist from the server"""
                self.send("NAMES %s" % channel)
        
        def end(self):
                self.socket.close()

        def announce(self, msg, instant = False): #Announce something to every channel the bot is in
                self.sayTo(msg, channel, instant) #For now the bot is always in one channel, but later this may change. E.g. dead players lounge

        def sayTo(self, msg, target, instant=False): #Say something to a specific target
                if (not instant):
                        self.sends.append("PRIVMSG %s %s" % (target, msg))
                else:
                       self.send("PRIVMSG %s %s" % (target, msg))
                
        def respond(self, event, msg):
                if (event.channel == self.nick):
                        self.sayTo(msg, event.sender)
                else:
                        self.sayTo(msg, event.channel)

        def topicset(self, msg):
                self.send("PRIVMSG CHANSERV :TOPIC %s %s" % (channel, msg))

        def prepend(self, msg):
                self.send("PRIVMSG CHANSERV :TOPICPREPEND %s %s" % (channel, msg))

        def checktopic(self, channel):
                self.send("TOPIC %s" % channel)
            
        def action(self, msg):
                self.send("PRIVMSG %s :ACTION %s " % (channel, msg))



class TopicSet:
        '''To prepend topic for cureent game and living players'''



        