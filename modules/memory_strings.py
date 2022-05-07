import subprocess
import shutil
import os
import time
def search_for(search,file):
	with open(file,'rb') as fileHandler:
		counter = 0
		while True:
			l = fileHandler.read(1)
			counter += 1
			if l.lower() == search[0].encode().lower():
				y = fileHandler.read(len(search)-1)
				counter += len(search)-1
				if y == search.encode()[1:]:
					print(f"[+] Offset : {hex(counter)}")
					fileHandler.seek(fileHandler.tell()-50)
					data = fileHandler.read(100)
					print(f"[+] Data : {l+y+data}")
					print("\n")
					fileHandler.seek(fileHandler.tell()-50)

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
			to_search = ""
			filetosearch = ""
			while to_search == "":
				to_search = input("[#] What do you want to search for? : ")
			while filetosearch != "hiberfil" and filetosearch != "pagefile":
				filetosearch = input("[#] 'hiberfil' or 'pagefile' search [hiberfil/pagefile]? : ")
				if filetosearch != "hiberfil" and filetosearch != "pagefile":
					print("[-] Invalid Option; the options are 'hiberfil' and 'pagefile'")
				elif filetosearch == "hiberfil":
					filetosearch = "hiberfil.sys"
					break
				elif filetosearch == 'pagefile':
					filetosearch = 'pagefile.sys'
					break
			search_for(to_search,f"tofu_tmp/windows_filesystem/{filetosearch}")
		except Exception as open_error:
			print(f"[-] Error {open_error}")
		time.sleep(2)	
		subprocess.check_call(["umount","tofu_tmp/windows_filesystem"])
