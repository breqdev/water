import json

class Message():
    def __init__(self):
        pass

    def withParams(self, sender, tags, content):
        self.sender = sender
        self.tags = tags
        self.content = content
        return self

    def fromJSON(self, jsonstr):
        try:
            struct = json.loads(jsonstr.strip("\x00"))
            self.sender = struct["sender"]
            self.tags = struct["tags"]
            self.content = struct["content"]
            return True
        except:
            return False

    def dumps(self):
        return json.dumps({"sender":self.sender,
                           "tags":self.tags,
                           "content":self.content})+"\x00"
    
