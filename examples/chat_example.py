import client

import tkinter

c = client.Client()

window = tkinter.Tk()
window.title("Water Example Chatroom")

def connect():
    global c, hostEntry
    c.connect(hostEntry.get())

def post(dummy=None):
    global c, postEntry
    m = c.makeMessage({"chat":["message"]}, postEntry.get())
    c.sendMessage(m)
    postEntry.delete(0, tkinter.END)

connectBtn = tkinter.Button(window, text="Connect", command=connect)
postBtn = tkinter.Button(window, text="Post", command=post)

hostLabel = tkinter.Label(window, text="Server IP:")

hostEntry = tkinter.Entry(window)

postEntry = tkinter.Entry(window)

msgLabel = tkinter.Text(window, wrap=tkinter.WORD)

connectBtn.grid(row=0, column=2, sticky=tkinter.E+tkinter.N)
postBtn.grid(row=3, column=2, sticky=tkinter.E, rowspan=2)

hostLabel.grid(row=0, column=0, sticky=tkinter.W+tkinter.N)


hostEntry.grid(row=0, column=1, sticky=tkinter.W+tkinter.E+tkinter.N)

postEntry.bind("<Return>", post)
postEntry.grid(row=3, column=0, columnspan=2, sticky=tkinter.W+tkinter.E)

msgLabel.grid(row=2, column=0, columnspan=3, sticky=tkinter.W)

window.rowconfigure(0, weight=1)
window.columnconfigure(1, weight=1)

def prettyPrint(msgs):
    if not msgs:
        return
    for msg in msgs:
        if not msg:
            return

        if "chat" in msg.tags:
            return "<"+msg.sender[:8]+"> "+msg.content+"\n"
        elif "water" in msg.tags:
            if "client_joined" in msg.tags["water"]:
                return "Client "+msg.content[:8]+" joined\n"
            elif "client_left" in msg.tags["water"]:
                return "Client "+msg.content[:8]+" left\n"
        return ""

while True:
    window.update()
    
    try:
        newmsg = prettyPrint(c.getMessages())
        if newmsg:
            msgLabel.insert(tkinter.END, newmsg)
    except OSError:
        pass
    
    msgLabel.see(tkinter.END)
