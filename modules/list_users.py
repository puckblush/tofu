import subprocess
import shutil
import os
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
				subprocess.check_call(["umount","tofu_tmp/windows_filesystem"])
			except:
				pass
		subprocess.check_call(["mount",drive_name,"tofu_tmp/windows_filesystem"])
		print("[+] Drive mounted to 'tofu_tmp/windows_filesystem'")
		try:
			users = os.listdir("tofu_tmp/windows_filesystem/Users/")
			for user in users:
				print(f"[+++] ------- - -// USER DISCOVERED : {user}")
		except Exception as open_error:
			print(f"[-] Error {open_error}")
		time.sleep(2)	
		subprocess.check_call(["umount","tofu_tmp/windows_filesystem"])
