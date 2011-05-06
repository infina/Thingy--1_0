class Message():
        def __init__(self):
                self.type = "message"
                self.sender = None
                self.senderMode = None
                self.private = None
                self.action = None
                self.text = None
                self.channel = None

        @property
        def respondee(self):
                """Decorator makes event.respondee return to who the responding pm must be adressed"""
                if (self.private):
                        return self.sender
                else:
                        return self.channel