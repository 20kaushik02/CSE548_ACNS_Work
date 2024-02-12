
cse468encrypt.py is used for caesar and julia ciphers for Homeworks 1.2 and
1.3.


The rest are sample files to try out how the RSA and AES encryptions work for
Homework 1.4.  The recommended usage of this is to use your own loopback IP
(127.0.0.1) in two terminal windows (so you can see in I/O of the server and
client).

In addition, the serverPublicKey is the *actual* public key used in the lab, so
that's the one the attacker used in the actual attack.


File             | Description                                                |
-----------------+------------------------------------------------------------+
aes.py           | Very basic classes for interfacing with AES and RSA        |
rsa.py           | methods                                                    |
-----------------+------------------------------------------------------------+
key.pub | A sample public key                                                 |
-----------------+------------------------------------------------------------+
key              | A sample private key                                       |
-----------------+------------------------------------------------------------+
sample_client.py | A client that encrypts the AES key and the word "True" and |
                 | sends it to the server                                     |
-----------------+------------------------------------------------------------+
sample_server.py | A server that listens for messages from the client,        |
                 | decrypts the client's message, capitalizes the plaintext,  |
                 | and returns an encrypted version                           |
-----------------+------------------------------------------------------------+
serverPublicKey  | The public key used by the true server for the lab         |
-----------------+------------------------------------------------------------+
README.txt       | This README                                                |
-----------------+------------------------------------------------------------+


The python files should be run using python3, and you may need to install some
python packages depending on your environment, like:

pip3 install pycrypto

You can run the programs in the following way from the terminal:
$ python3 sample_server.py -p 10047 -kp key.pub -ks key
$ python3 sample_client.py -ip 127.0.0.1 -p 10047 -f key.pub

The first call stands up the server that listens on the specified port (10047
in this example). The -kp flag is the public key you'd like the server to use,
and -ks is the private key.

The second call kicks off a client on the loopback at the same port with -f
specifying the shared public key of the server.


