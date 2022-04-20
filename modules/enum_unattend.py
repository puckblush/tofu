import subprocess
import shutil
import os
import time
from struct import unpack, pack
from collections import namedtuple
NK_ID = 0x6B6E
NK_ROOT = 0x2c
HASH_RECORD = namedtuple('HASH_RECORD', 'nk_offset keyname')
NK_HDR = namedtuple('NK_HDR', 'id type t1 t2 unk1 parent_off subkey_num unk2 lf_off unk3 value_cnt value_off sk_off classname_off unk41 unk42 unk43 unk44 unk5 name_len classname_len key_name')
LF_HDR = namedtuple('LF_HDR', 'id key_num hr')
VK_HDR = namedtuple('VK_HDR', 'id name_len data_len data_off data_type flag unk1 value_name')
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
        
        
        
def get_unattend_data(system_path):
	reg_hive = RegHive(system_path)
	openKey = reg_hive.regOpenKey(b"Setup")
	for keyToRead in reg_hive.regEnumKey(openKey):
		data = reg_hive.regQueryValue(openKey, keyToRead)
		print(f"[$] {keyToRead} : {data}")
	data = reg_hive.regQueryValue(openKey, b"UnattendFile")
	print(f"[***] Custom Unattend File : {data}")


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
				subprocess.check_call(["umount","tofu_tmp/windows_filesystem"])
			except:
				pass
		subprocess.check_call(["mount",drive_name,"tofu_tmp/windows_filesystem"])
		print("[+] Drive mounted to 'tofu_tmp/windows_filesystem'")
		try:
			shutil.copy("tofu_tmp/windows_filesystem/Windows/System32/config/SYSTEM","tofu_tmp/UNATTEND_SYSTEM")
			reg_unattend = get_unattend_data("tofu_tmp/UNATTEND_SYSTEM")
			if reg_unattend:
				print(f"[#] Custom unattend path at {reg_unattend}")
			else:
				print(f"[-] No custom unattend path")
			
			
			for filename in ["unattend.xml","autounattend.xml"]:
				for filePath in [f"tofu_tmp/windows_filesystem/Windows/System32/sysprep/{filename}", f"tofu_tmp/windows_filesystem/Windows/panther/{filename}",f"tofu_tmp/windows_filesystem/Windows/Panther/Unattend/{filename}",f"tofu_tmp/windows_filesystem/Windows/System32/{filename}",f"tofu_tmp/windows_filesystem/Windows/System32/panther/{filename}",f"tofu_tmp/windows_filesystem/Windows/System32/Panther/Unattend/{filename}"]:
					if os.path.exists(filePath):
						print(f"[+] '{filename}' found at '{filePath}'")
					else:
						print(f"[-] '{filename}' not found at '{filePath}'")
					
			os.remove("tofu_tmp/UNATTEND_SYSTEM")
		except Exception as open_error:
			print(f"[-] Error {open_error}")
		time.sleep(2)	
		subprocess.check_call(["umount","tofu_tmp/windows_filesystem"])
