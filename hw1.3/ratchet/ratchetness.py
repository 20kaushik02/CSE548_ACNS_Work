# ratchetness.py, a simplified form of OTR for spreading ratchet gossip about your CSE 539 instructor
# jedimaestro@asu.edu

import secrets
import sys
import os.path
import time
import os
import re
from colorama import Fore, Back, Style
import signal

g = 10697987386528634556132351984988679277669693771233806587823166397646257882356751154924044166012048802718827287365490918762116743604708315476073224232944329

p = 21395974773057269112264703969977358555339387542467613175646332795292515764713502309848088332024097605437654574730981837524233487209416630952146448465888659

if (len(sys.argv) < 3) or sys.argv[1] == sys.argv[2]:
    print("No!  RTFSC!")
    exit(0)

myname = sys.argv[1]
theirname = sys.argv[2]

imfirst = myname > theirname
if imfirst:
    fn = "/tmp/" + myname + "-and-" + theirname + ".txt"
else:
    fn = "/tmp/" + theirname + "-and-" + myname + ".txt"
if imfirst:
    if os.path.isfile(fn):
        os.remove(fn)
elif False:
    while os.path.isfile(fn):
        time.sleep(1)

def handler(signum, frame):
    print(Style.RESET_ALL + "Ctrl-c was pressed. Exiting...")
    if os.path.isfile(fn):
        os.remove(fn)
    exit(0)

                                                                         
                                                                          
signal.signal(signal.SIGINT, handler)

messagenumber = 0
theirlatestratchet = 0
mylatestprivatekey = 0

def otp(plainorcipher, encordec, key):
# plainorcipher is the text for plaintext or ciphertext
# encordec is "enc" to encrypt or "dec" to decrypt
# key is a large integer with hopefully enough key material
    if encordec == "enc":
        sign = 1
    elif encordec == "dec":
        sign = -1
    else:
        return "Bad use of bad API"
    keystream = []
    ki = key
    while ki > 0:
        keystream.append(ki % 26)
        ki = int(ki / 26)
    whattoreturn = ""
    for i in range(len(plainorcipher)):
        letter = ord(plainorcipher[i]) - ord('A')
        c = (letter + keystream[i]*sign) % 26
        c = c + ord('A')
        whattoreturn = whattoreturn + str(chr(c))
    return whattoreturn


while True:
    if (imfirst and messagenumber % 2 == 0) or ((not imfirst) and messagenumber % 2 == 1):
        mylatestprivatekey = secrets.randbelow(p) 
        myratchet = pow(g, mylatestprivatekey, p)
        s = pow(theirlatestratchet, mylatestprivatekey, p) 
        print(Fore.GREEN + "Sending... " + str(messagenumber))
        if messagenumber != 0:
            print(Fore.GREEN + "Please type something juicy... ")
            ratchetgossip = sys.stdin.readline().rstrip('\n')
            if len(ratchetgossip) == 0:
                exit(0)
            plaintext = re.sub(r'[^A-Z]', '', ratchetgossip.upper())
            ciphertext = otp(plaintext, "enc", s)

        fout = open(fn, "w")
        fout.write(str(myratchet))
        fout.write("\n")
        if messagenumber != 0:
            fout.write(ciphertext)
            fout.write("\n")
        fout.flush()
        fout.close()
        messagenumber = messagenumber + 1
        while os.path.isfile(fn):
            time.sleep(0.1)
    else:
        print(Fore.RED + "Receiving... " + str(messagenumber))
        while not os.path.isfile(fn):
            time.sleep(1)
        time.sleep(1)
        fin = open(fn, "r")
        theirlatestratchet = int(fin.readline())
        s = pow(theirlatestratchet, mylatestprivatekey, p) 
        if messagenumber != 0:
            ciphertext = fin.readline().rstrip('\n')
            print("Received: " + otp(ciphertext, "dec", s))
        fin.close()
        os.remove(fn)
        messagenumber = messagenumber + 1
        time.sleep(2)





