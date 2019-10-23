
#
## receiveblinksLAM  (modified by me)  for physical layer (with network layer sanity test)
#
## I added a prompt for samples per second -- I also modified the melville quote generator have a prompt for samples per second
#  so you can try at faster pulse rates.   Also added a character per seocnd maeaursment.
#
# 
#
# BTW - The Melville quotes were being sent correctly -- there was a timing problem in the receiveblinks function
#

#
## The receiveblinksLAM_threaded module has a start at using threads -- I rewrote that one aa a class to make it clearer
#


from  SetPin import SetPin
import Morse as M
import time

address = 'CC'

def p(X,*T,**D):
    "print to use for looking at intermediate results in comprehensions"
    print(X,*T,**D)
    return X

fromMorse = {(1,1):'.',
        (1,3):'-',
        (0,1):'*',
        (0,2):'_',
        (0,4):'|',
        (0,8):'END'}

def translate(data):
    print("translate ({})".format(data))
    #dat = data[1:len(data)]
    string = ''
    for d in data:
        print(d,end=":")
        if d in fromMorse:
            string += fromMorse[d]
            print(string)
        else: print("{} not in reverse morse table".format(d))
    ditdahs = string.replace('*', '').strip("END")
    print(ditdahs)
    ddwords = ditdahs.split("|")
    print(ddwords)
    words = []
    for ddword in ddwords:
        words.append("".join([p(M.from_morse(p(ddletter))) for ddletter in ddword.split("_") if ddletter]))
    print(words) 
    message = " ".join(words)
    print(message)
    return message

def getdiff(time_stamp):
    return time.time() - time_stamp

def receiveblinks(RXpin)->tuple:
    print("receiveblinks")
    print("dits per second: {}".format(speed))
    print("samples per dit: {}".format(samplesperdit))
    tuples = []
    time_stamp = time.time()
    last_state = 0
    print("start skip zeros",last_state,getdiff(time_stamp))
    while True:
        last_reading = RXpin.read_pin()
        #print(last_reading,last_state)
        if last_reading != last_state:
            #print ("end skip zeros",getdiff(time_stamp))
            time_stamp = time.time()
            last_state = 1
            break
        time.sleep(1/(samplesperdit*speed))
    print("enter main while loop",last_state)
    while getdiff(time_stamp) <= 5:
        time.sleep(1/(samplesperdit*speed))
        last_reading = RXpin.read_pin()
        if last_reading != last_state:
            tuples.append([last_state, getdiff(time_stamp)])
            last_state = last_reading
            time_stamp = time.time()
            
    return tuples

def cleandata(data):
    print("cleandata({})".format(data))
    for dat in range(len(data)):
        data[dat][1] = round(speed*data[dat][1])
    print("cleandata return {}".format(data))
    return data

def interpretdata(data):
    print("interpretdata({})".format(data))
    if data[:len(address)] == address:
        return data[len(address):]
    else:
        return 

def checksum(data):
    s = 0
    message = data[len(address)+1:]
    print(message)
    for c in message:
        s += ord(c)
    if s%19 == ord(data[len(address)])-64:
        return data
    else:
        return None

def printMessage(message):
    if message != None:
        print('Message from ' + message[:len(address)])
        print(message[len(address)+1:])
    else:
        print('There was a communication error')

def RXblink():
        messagenumber = 1
        with SetPin(16,"GPIO_23",direction="RX") as RXpin:
            while True:
                tuples = receiveblinks(RXpin)
                QT.put(tuples,timeout=60)
                print("""
Message number {} enqueued,
tuples = {}
time = {}
""".format(messagenumber, len(tuples),time.asctime()))
                # put will time out when queue is empty for a minute
                # so don't dawdle.
def RXprint():
    messagenumber = 1
    while True:
     

        messagenumber +=1
        
        
        tuples = QT.get(timeout=120)
        print ("""
message number {} dequeued,
tuples = {},
time = {}
""".format(
            messagenumber, len(tuples), time.asctime()))
        # times out in two minutes
        data = cleandata(tuples)
        print("RXprint loop, data={}".format(data))
        for dat in range(len(data)):
            data[dat] = tuple(data[dat])
        for n,i in enumerate(data):
            if(i == (0,3)):
                data[n] = (0,1)
                data.insert(n+1,(0,2))
            elif(i == (0,7)):
                data[n] = (0,1)
                data.insert(n+1,(0,2))
                data.insert(n+2,(0,4))
        print("main loop after enumerate: {}".format(data))
        message = translate(data)
        interpreted = interpretdata(message) # proof of concept for network layer
        message = checksum(interpreted)# have to handle media access control -- much harder
        printMessage(message)

            
if __name__ == "__main__":
    
    import threading
    import queue

    
    speed = int(input("Dit times per second:"))
    print("speed = {} Dit times per second".format(speed))
    samplesperdit = int(input("Samples per dit :"))
    print("speed = {} Dit times per second".format(speed))
    QT=queue.Queue() # no queue maxsize - we have lots of memory in the pi
    thread_RXb = threading.Thread(target=RXblink,name="RXblink")
    thread_RXp = threading.Thread(target=RXprint,name="RXprint")
    print("Starting RXprint thread")
    thread_RXp.start()
    time.sleep(1)
    print("Starting RXblink thread")
    thread_RXb.start()
    time.sleep(1)
    while True:
        print("*",end="")
        time.sleep(60)