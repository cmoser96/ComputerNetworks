#
## Lab 2.2 - Physical Layer  - Send Tuples as blinks
#
from MorseTX import MorseTX
from SetPin import SetPin
import random
import mobydickquotes
import string
import unicodedata
import time
from receiveblinksLAM_threading_classes import physical


class BlinkTX(SetPin):
    def __init__(self, address, headerpin,BCM,direction="TX",dit_time=.03):
        self.address = address
        p = physical(self.address)
        if direction != "TX":
            raise ValueError("direction must be 'TX'")
        super().__init__(headerpin,BCM,direction="TX")
        self.dit_time = dit_time
    def __call__(self,tups):
        check = p.checkBefore(self.dit_time)
        if check:
            for state,duration in tups:
                self.blinkTX(state,duration)
    def blinkTX(self,state,duration):
        self.turn_high() if state else self.turn_low()
        time.sleep(self.dit_time*duration)      

def blink():
    quotes = mobydickquotes.quotes

    def getquote():
        q = quotes[random.randint(0,len(quotes)-1)]
        print(q)
        return q.upper().replace('\n', ' ')

    def checksum(msg):
        s = 0
        for c in msg:
            s += ord(c)
        return chr(s%26+65) + msg

    while True:
        x=input("dit_times per second:")
        to = input("To address:").upper()
        print(x)
        if not all([d in string.digits for d in x]):
            print ("enter an integer")
            continue
        dit_time=int(x)
        break
    
    with BlinkTX(15,'CC',"GPIO_22",direction="TX",dit_time=1/dit_time) as blink:
        while True:
            msg = input("""\
ENTER

  A MESSAGE TO SEND
  TO SEND A MESSAGE

  the 'enter" key
  TO SEND A RANDOM MELVILLE QUOTE
  
  QUIT
  TO QUIT

:"""
)
            if not msg:
                blink(MorseTX(to + address + checksum(getquote())))
            elif msg.upper() == "QUIT":
                break
            else:
                blink(MorseTX(to + address + checksum(msg.upper())))

if __name__ == "__main__":
    blink()