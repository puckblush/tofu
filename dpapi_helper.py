import importlib
import os
import sys
print("[#] dpapi_helper.py : Loading modules")
from pypykatz.dpapi.dpapi import DPAPI
import glob
import json
import sqlite3
import base64

def decrypt_chrome_experimental(winpath,users,registry_sam,registry_system):
	# THIS DOES NOT WORK YET; DO NOT IMPLEMENT THIS PLEASE
	# this works by dumping the hashes from the registry and using extracted SIDs from the '%AppData%/Microsoft/Protect' to make prekeys
	# using the prekeys, it tries to decrypt the masterkey file using the specific user's hash
	# this method is faster than cycling through every prekey with every masterkey file, which takes forever and a day
	bootkey = get_bootkey(registry_system)
	print(f"[#] Bootkey : {bootkey}")
	registry_hive = RegHive(registry_sam)
	sam_key = get_hbootkey(registry_hive,bootkey)
	hashes = get_hashes(registry_hive,sam_key)
	
	
	for user in users:
		user_hash = hashes[user]
		print("[HASH PAIR] {user}:{user_hash}")
		dpapi_object = DPAPI()
		#prekeys = dpapi_object.get_prekeys_form_registry_files(f"{winpath}/Windows/System32/config/SYSTEM", f"{winpath}/Windows/System32/config/SECURITY", f"{winpath}/Windows/System32/config/SAM")
		#dpapi_object.get_prekeys_from_password()
		masterkey_files = f"{winpath}/Users/User/AppData/Roaming/Microsoft/Protect/"
		prekeys = []
		for sid in os.listdir(masterkey_files):
			l = dpapi_object.get_prekeys_from_password(sid,user_hash)
			print(l)
			prekeys.append(l)
		prekey_list = []
		for prekey in prekeys:
			for prekey2 in prekey:
				prekey_list.append(prekey2.hex())
		prekeys = prekey_list
		masterkey_array_length = 0
		old_masterkey_array_length = 0
		
		for masterkey_file in glob.glob(f"{masterkey_files}/*/*"):
			print(f"[#] Trying {masterkey_file}")
			for prekey in prekeys:
				masterkey_array_length = len(dpapi_object.masterkeys)
				if prekey is not None:
					print(f"[#] Trying Prekey Candidate {prekey}")
					dpapi_object.load_prekeys(prekey)

					dpapi_object.decrypt_masterkey_file(masterkey_file)
					if masterkey_array_length > old_masterkey_array_length:
						old_masterkey_array_length = masterkey_array_length
						print(f"[+++] Retrieved masterkey")

		if dpapi_object.masterkeys:
			for masterkey in masterkeys:
				print(f"-- MASTERKEY / {masterkey}") 
			print("[#] We have masterkeys. Now, lets' try them on Chrome")
			
def get_masterkeys(winpath,registry_sam,registry_system,registry_security):
	
	# this works by dumping all potential prekey candidates from the registry, and then cycling through the masterkey files to get a masterkey
	# this method takes a ridiculous amount of time because DPAPI takes a while to decrypt the masterkey 
	dpapi_object = DPAPI()
	prekeys = dpapi_object.get_prekeys_form_registry_files(registry_system, registry_security, registry_sam)
	prekey_list = []
	for prekey in prekeys:
                for prekey2 in prekey:
                        prekey_list.append(prekey2.hex())
        prekeys = prekey_list
	#dpapi_object.get_prekeys_from_password()
	for user in os.listdir(f"{winpath}/Users/")
                try:
                masterkey_files = f"{winpath}/Users/{user}/AppData/Roaming/Microsoft/Protect/"
                masterkey_array_length = 0
                old_masterkey_array_length = 0
                        
                for masterkey_file in glob.glob(f"{masterkey_files}/*/*"):
                        print(f"[#] Trying {masterkey_file}")
                        for prekey in prekeys:
                                masterkey_array_length = len(dpapi_object.masterkeys)
                                if prekey is not None:
                                        print(f"[#] Trying Prekey Candidate {prekey}")
                                        try:
                                                dpapi_object.load_prekeys(prekey)
                                                
                                                dpapi_object.decrypt_masterkey_file(masterkey_file)
                                                if masterkey_array_length > old_masterkey_array_length:
                                                        old_masterkey_array_length = masterkey_array_length
                                                        print(f"[+++] Retrieved masterkey")
                                        except OverflowError:
                                                print("[#] Got something that wasn't a masterkey file; ignoring")
                                                
                return dpapi_object.masterkeys
try:
	winpath = sys.argv[1]
except IndexError:
	print("[#] Usage : dpapi_helper.py PATH_TO_MOUNTED_WINDOWS_DRIVE")
	print("[#] Example : dpapi_helper.py /media/ubuntu/Windows")
	sys.exit(0)
masterkeys = get_masterkeys(winpath, f"{winpath}/Windows/System32/config/SAM", f"{winpath}/Windows/System32/config/SYSTEM",f"{winpath}/Windows/System32/config/SECURITY")
for masterkey in masterkeys:
	print(f"-- MASTERKEY / {masterkey}")
