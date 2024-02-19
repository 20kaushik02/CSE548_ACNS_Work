# mallory.py, a mitm attack to learn ratchet gossip about your CSE 539 instructor
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

flog = open("mallorylog.txt", "w")

myname = sys.argv[1]
theirname = sys.argv[2]

imfirst = myname > theirname
if imfirst:
    fn = "/tmp/" + myname + "-and-" + theirname + ".txt"
else:
    fn = "/tmp/" + theirname + "-and-" + myname + ".txt"
#if os.path.isfile(fn):
#    os.remove(fn)

def handler(signum, frame):
    print(Style.RESET_ALL + "Ctrl-c was pressed. Exiting...")
    exit(0)

                                                                         
                                                                          
signal.signal(signal.SIGINT, handler)

messagenumber = 6
leakerslatestratchet = 0
otherslatestratchet = 0
mylatestprivatekeyforleaker = 0
mylatestprivatekeyforother = 0

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

olderlatestratchet = 0
olderciphertext = ""
ciphertext = ""

while not os.path.isfile("/tmp/oops.txt"):
    if os.path.isfile(fn):
        fin = open(fn, "r")
        if fin:
            newotherslatestratchet = int(fin.readline())
            if otherslatestratchet != newotherslatestratchet:
                olderlatestratchet = otherslatestratchet
                otherslatestratchet = newotherslatestratchet
                flog.write("ratchet")
                flog.write("\n")
                flog.write(str(otherslatestratchet))
                flog.write("\n")
            newciphertext = fin.readline().rstrip('\n')
            if ciphertext != newciphertext:
                olderciphertext = ciphertext
                ciphertext = newciphertext
                flog.write("ciphertext")
                flog.write("\n")
                flog.write(ciphertext)
                flog.write("\n")
        fin.close()
    time.sleep(0.3)
oops = open("/tmp/oops.txt", "r")
mylatestprivatekeyforother = int(oops.readline().rstrip('\n'))
oops.close()
os.remove("/tmp/oops.txt")

fin = open(fn, "r")
leakerslatestratchet = int(fin.readline())
newerciphertext = fin.readline().rstrip('\n')
fin.close()

# We can decrypt one message already
s = pow(otherslatestratchet, mylatestprivatekeyforother, p) 
plaintext = otp(newerciphertext, "dec", s)
print("Eavesdropped " + theirname + ": " + plaintext)

flog.write("stolenkey")
flog.write("\n")
flog.write(str(mylatestprivatekeyforother))
flog.write("\n")


while True: 
    # Wait for the other to update the file
    while os.path.isfile(fn):
        time.sleep(0.001)
    while not os.path.isfile(fn):
        time.sleep(0.001)
    time.sleep(0.3)
    # Read the info and delete the file
    fin = open(fn, "r")
    theline = fin.readline()
    #print(theline)
    otherslatestratchet = int(theline)
    ciphertext = fin.readline().rstrip('\n')
    fin.close()
    os.remove(fn)
    # Do part of a key exchange with other, decrypt if possible
    s = pow(otherslatestratchet, mylatestprivatekeyforother, p) 
    plaintext = otp(ciphertext, "dec", s)
    flog.write("ciphertextforleaker")
    flog.write("\n")
    flog.write(ciphertext)
    flog.write("\n")
    print("Eavesdropped " + myname + ": " + plaintext)
    # Do a key exchange with leaker
    mylatestprivatekeyforleaker = secrets.randbelow(p)  
    mylatestprivatekeyforother = secrets.randbelow(p)  
    flog.write("keys")
    flog.write("\n")
    flog.write(str(mylatestprivatekeyforleaker))
    flog.write("\n")
    flog.write(str(mylatestprivatekeyforother))
    flog.write("\n")
    myratchetforleaker = pow(g, mylatestprivatekeyforleaker, p)
    s = pow(leakerslatestratchet, mylatestprivatekeyforleaker, p) 
    # Reencrypt and make file
    ciphertext = otp(plaintext, "enc", s)
    fout = open(fn, "w")
    flog.write("ratchetsleaker")
    flog.write("\n")
    flog.write(str(leakerslatestratchet))
    flog.write("\n")
    fout.write(str(myratchetforleaker))
    fout.write("\n")
    fout.write(ciphertext)
    fout.write("\n")
    fout.flush()
    fout.close()
    # Wait for the leaker to update the file
    while os.path.isfile(fn):
        time.sleep(0.001)
    while not os.path.isfile(fn):
        time.sleep(0.001)
    time.sleep(0.3)
    # Read the info and delete the file
    fin = open(fn, "r")
    theline = fin.readline()
    #print(theline)
    leakerslatestratchet = int(theline)
    ciphertext = fin.readline().rstrip('\n')
    fin.close()
    os.remove(fn)
    # Do a key exchange with other, decrypt if possible
    myratchetforother = pow(g, mylatestprivatekeyforother, p)
    s = pow(leakerslatestratchet, mylatestprivatekeyforleaker, p) 
    plaintext = otp(ciphertext, "dec", s)
    flog.write("ciphertextforother")
    flog.write("\n")
    flog.write(ciphertext)
    flog.write("\n")
    print("Eavesdropped " + theirname + ": " + plaintext)
    # Reencrypt and make file
    s = pow(otherslatestratchet, mylatestprivatekeyforother, p) 
    ciphertext = otp(plaintext, "enc", s)
    fout = open(fn, "w")
    flog.write("ratchetsother")
    flog.write("\n")
    flog.write(str(otherslatestratchet))
    flog.write("\n")
    fout.write(str(myratchetforother))
    fout.write("\n")
    fout.write(ciphertext)
    fout.write("\n")
    fout.flush()
    fout.close()
    messagenumber = messagenumber + 2
    if (False and messagenumber == 16):
        print("droppingtheball...")
        time.sleep(40)
     



