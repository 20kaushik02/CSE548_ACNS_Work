import math
import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


# Fermat's factorization
def fermat(n, start):
    count = 0

    # if primes are close, mean of primes is close to sqrt(n)
    a = math.isqrt(n) + 1
    b = math.isqrt((a * a) - n)

    # check b^2 = a^2 - n
    while (b * b) != ((a * a) - n):
        # print("[+] bit length of (a2 - n):", int(((a*a) -n)).bit_length())
        count += 1

        a += 1
        b = math.isqrt((a * a) - n)

        if count % 1e8 == 0:
            print("time elapsed:", time.perf_counter() - start, "seconds", flush=True)

    # calc the primes from their mean and distance
    p = a + b
    q = a - b
    return p, q, count


pub_key = RSA.import_key(open("key.pub", "r").read())

# testing
# computerphile example, intentionally weak, runs in 12 iterations
n = 5261933844650100908430030083398098838688018147149529533465444719385566864605781576487305356717074882505882701585297765789323726258356035692769897420620858774763694117634408028918270394852404169072671551096321238430993811080749636806153881798472848720411673994908247486124703888115308603904735959457057925225503197625820670522050494196703154086316062123787934777520599894745147260327060174336101658295022275013051816321617046927321006322752178354002696596328204277122466231388232487691224076847557856202947748540263791767128195927179588238799470987669558119422552470505956858217654904628177286026365989987106877656917
e = 65537

# example posted in canvas discussions
# seems to be safe from this method
# n = 125992118149870746006493654389175279527472408386640156684228205007899250636526783672946765874704581329243206029282525787037543662260258606135966229683550046557542867359322036785322426006162242420991369663470231974481363297634340923634481349310535206763098422642504687457452847274657348442529853593836012279453
# e = 65537

# example in citizenlab report
# n = 245406417573740884710047745869965023463
# e = 65537

pub_key = RSA.construct((n, e))

start = time.perf_counter()
d_p, d_q, iters = fermat(pub_key.n, start)
end = time.perf_counter()

print("found solution in {} seconds ({} iterations)".format(end - start, iters))
print("prime factors are:\n\np:", d_p, "\nq:", d_q)
print("\nn == p * q:", pub_key.n == d_p * d_q)

phi_n = (d_p - 1) * (d_q - 1)
d = pow(pub_key.e, -1, phi_n)

print("\nprivate key exponent d =", d)
priv_key = RSA.construct((pub_key.n, pub_key.e, d), consistency_check=True)

print("verifying...")
enc_key = PKCS1_OAEP.new(pub_key)
cipher_text = enc_key.encrypt("hello world".encode())

dec_key = PKCS1_OAEP.new(priv_key)
plain_text = dec_key.decrypt(cipher_text).decode()

if plain_text == "hello world":
    print("cracked! saving key...")
    with open("cracked.key", "w") as f:
        print(priv_key.export_key().decode(), file=f)
