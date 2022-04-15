import sys
import hashlib
import binascii
advanced_charset = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()-_=+[]{}|\\~`,<.>?/"
charset = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%&*-_=+?/"
def bruteforce(user_hash):
    for c1 in charset:
        if c1 == " ":
            c1 = ""
        print("[#] Char 10 Reached")
        for c2 in charset:
            if c2 == " ":
                c2 = ""
            print("[#] Char 9 Reached")
            for c3 in charset:
                if c3 == " ":
                    c3 = ""
                print("[#] Char 8 Reached")
                for c4 in charset:
                    if c4 == " ":
                        c4 = ""
                    print("[#] Char 7 Reached")
                    for c5 in charset:
                        if c5 == " ":
                            c5 = ""
                        print("[#] Char 6 Reached")
                        for c6 in charset:
                            print(c6)
                            if c6 == " ":
                                c6 = ""
                            print("[#] Char 5 Reached")
                            for c7 in charset:
                                if c7 == " ":
                                    c7 = ""
                                for c8 in charset:
                                    if c8 == " ":
                                        c8 = ""
                                    for c9 in charset:
                                        if c9 == " ":
                                            c9 = ""
                                        for c10 in charset:
                                            if c10 == " ":
                                                c10 = ""
                                            password_to_try = c1+c2+c3+c4+c5+c6+c7+c8+c9+c10
                                            hash_to_try = hashlib.new('md4', password_to_try.encode('utf-16le')).digest()
                                            hash_to_try = binascii.hexlify(hash_to_try)
                                            hash_to_try = hash_to_try.lower()
                                            #print(password_to_try)
                                            #print(password_to_try)
                                            if hash_to_try == user_hash.encode():
                                                print(f"[+] CRACKED! {user_hash}:{password_to_try}")
                                                return password_to_try
def do_wordlist(user_hash,wordlist):
    with open(wordlist,'r') as wordlist_fileHandler:
        line = "a"
        while line != "":
            try:
                line = wordlist_fileHandler.readline()
                line_clean = line.replace("\n","").replace("\r","")
                hash_to_try = hashlib.new('md4', line_clean.encode('utf-16le')).digest()
                hash_to_try = binascii.hexlify(hash_to_try)
                hash_to_try = hash_to_try.lower()
                if hash_to_try == user_hash.encode():
                    print(f"[+] CRACKED! {user_hash}:{line_clean}")
                    return line_clean
            except UnicodeDecodeError:
                #print("[?] Encountered Invalid Byte; Continuing")
                pass
        
    
try:
    hashes_file = sys.argv[1]
    wordlist = sys.argv[2]
except IndexError:
    print("[#] Usage : hash_crack.py HASHES_FILE WORDLIST")
    print("[#] For bruteforce mode, replace WORDLIST with 'BRUTEFORCE'")
    sys.exit(0)
hash_line = "a"
with open(hashes_file,'r') as hash_file_handler:
    while hash_line != "":
        hash_line = hash_file_handler.readline()
        if hash_line != "":
            hash_line = hash_line.replace("\n","").replace("\r","")
            username = hash_line.split(":")[0]
            user_hash = hash_line.split(":")[1]
            user_hash = user_hash.lower()
            if len(user_hash) == 32:
                print(f"[#] Cracking {hash_line}")
                if wordlist.lower() == "bruteforce":
                    print("[#] Running 10 Characters Of Incremental ASCII")
                    plaintext = bruteforce(user_hash)
                    print(f"[!!!] {username}:{plaintext}")
                else:
                    plaintext = do_wordlist(user_hash,wordlist)
                    print(f"[!!!] {username}:{plaintext}")
                    
            else:
                print(f"[-] Invalid Hash Length : {len(user_hash)}; Skipping")
            
        
        
