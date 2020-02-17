import curses
import time

import client

class Player:
    def __init__(self, uuid):
        self.uuid = uuid
        self.x = 0
        self.y = 0

    def moveTo(self, x, y):
        self.x, self.y = x,y

    def draw(self, stdscr):
        stdscr.addstr(self.y, self.x, str(self.uuid)[0])


def main(stdscr):

    curses.noecho()
    curses.cbreak()
    stdscr.nodelay(True)

    stdscr.keypad(True)
    curses.curs_set(False)

    cl = client.Client()
    cl.connect("localhost")

    player = Player(cl.uuid)
    players = {str(cl.uuid):player}
    
    while True:
        c = stdscr.getch()
        if c == ord('q'):
            cl.close()
            break
        if c == curses.KEY_UP:
            player.moveTo(player.x, max(player.y-1, 0))
        if c == curses.KEY_DOWN:
            player.moveTo(player.x, min(player.y+1, 23))
        if c == curses.KEY_LEFT:
            player.moveTo(max(player.x-1, 0), player.y)
        if c == curses.KEY_RIGHT:
            player.moveTo(min(player.x+1, 79), player.y)

        posMsg = cl.makeMessage({"world":["position"]},
                                {"x":player.x, "y":player.y})

        cl.sendMessage(posMsg)

        msgs = cl.getMessages()
        if not msgs:
            continue
        for msg in msgs:
            if "world" in msg.tags:
                if "position" in msg.tags["world"]:
                    if msg.sender == str(cl.uuid):
                        continue
                    if msg.sender not in players:
                        players[msg.sender] = Player(msg.sender)
                    players[msg.sender].moveTo(
                            msg.content["x"], msg.content["y"])
            elif "water" in msg.tags:
                if "client_left" in msg.tags["water"]:
                    if msg.content in players:
                        del players[msg.content]

        stdscr.clear()
        for p in players.values():
            p.draw(stdscr)
        time.sleep(0.1)

curses.wrapper(main)
