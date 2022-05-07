import glob
import importlib
import subprocess

class tofu:
	drive_option_data = {}
	drive_path = None
	drive_format = None
	module_list = []
	def check_valid_ms(path):
		filesystem_data = {}
		try:
			with open(path,'rb') as fileHandler:
				try:
					header = fileHandler.read(11)[3:11]
					if header.startswith(b"NTFS"):
						return "NTFS"
					elif header.startswith(b"MSDOS"):
						return "MSDOS"
					elif header.startswith(b"-FVE-FS-"):
						return "BITLOCKER ENCRYPTED DRIVE"
					else:
				 		return False
				except PermissionError:
					print("[-] Insufficient Permissions; Are you running as root?")
					return False
		except FileNotFoundError:
			print("[-] File not found")
			return False
	def list_all_ms_drives():
		mounted_drives = glob.glob("/dev/nvme*") + glob.glob("/dev/sd*") + glob.glob("/dev/hd*") + glob.glob("/dev/xvd*") + glob.glob("/dev/mmc*")
		filesystem_data = {}
		try:
			for m in mounted_drives:
				with open(m,'rb') as fileHandler:
					try:
						header = fileHandler.read(11)[3:11]
						if header.startswith(b"NTFS"):
							filesystem_data[m] = "NTFS"
						elif header.startswith(b"MSDOS"):
							filesystem_data[m] = "MSDOS"
						elif header.startswith(b"-FVE-FS-"):
							filesystem_data[m] = "BITLOCKER ENCRYPTED DRIVE"
					except:
						pass
		except PermissionError:
			print("[-] Insufficient Permissions; Are you running as root?")
			exit()
		return filesystem_data
	def print_all_ms_drives():
		print("[#] Listing all devices using a Microsoft file system\n")
		filedata = tofu.list_all_ms_drives()
		drive_counter = 0
		for file_system in filedata:
			drive_counter += 1
			tofu.drive_option_data[str(drive_counter)] = file_system
			print(f"Drive : {drive_counter} \n Drive Location : {file_system} \n Drive Format : {filedata[file_system]} \n ======================================")

	def banner():
		print('''
[ 		tofu  	   ]
[	   by puckblush    ]
[		           ]
		''')
	def help():
		print(f'''
		DRIVE  : {tofu.drive_path}
		FORMAT : {tofu.drive_format}
		
		[help] - Print this help message
		[exit] - Exit
		[list] - List all Microsoft drives at '/dev'
		[usedrive] - Set drive to use

		[modules] - Reload & List modules
		[use] - Use module
		''')
	def list_modules():
		modules = glob.glob("./modules/*.py")
		return modules
	def check_valid_module(module):
		if module in tofu.module_list or module+".py" in tofu.module_list:
			return True
		else:
			return False
	def load_module(module_name):
		module_name = module_name.replace(".py","")
		print(f"[...] Loading {module_name}")
		current_module = importlib.import_module("modules."+module_name)
		try:
			current_module.__main__(tofu.drive_path,tofu.drive_format)
				
		except Exception as module_error:
			print(f"Module Failed : {module_error}")
	def __main__():
		tofu.banner()
		tofu.help()
		while True:
			option = input("Option >> ")
			option = option.lower()
			if option == 'help':
				tofu.help()
			elif option == 'exit':
				exit()
			elif option == 'list':
				tofu.print_all_ms_drives()
			elif option.startswith("usedrive ") or option == "usedrive":
				if option == "usedrive":
					drive_to_use = input("[full path to drive/alias from 'list'] >>")
					
				else:
					drive_to_use = option[9:]
				drive_to_use = drive_to_use.strip()
				
				check_for_file = True
				
				try:
					drive_to_use = tofu.drive_option_data[drive_to_use]
					check_for_file = False
				except:
					pass
					
				if check_for_file:
					drive_type = tofu.check_valid_ms(drive_to_use)	
					if drive_type:
							print("[+] Valid MS Drive")
							print(f"[+] Drive Format : {drive_type}")
							tofu.drive_path = drive_to_use
							tofu.drive_format = drive_type
					else:
							print("[-] Invalid MS Drive")
				else:
					drive_type = tofu.check_valid_ms(drive_to_use)
					if drive_type:
						print("[+] Valid MS Drive")
						print(f"[+] Drive Format : {drive_type}")
						tofu.drive_path = drive_to_use
						tofu.drive_format = drive_type
					else:
						print("[?] Something went wrong with getting the drive format; try re-listing the drives")
			
			elif option == "modules":
				print("==============================================================\n")
				module_list = tofu.list_modules()
				clean_module_list = []
				for module in module_list:
					clean_module = module.split("/")[len(module.split("/"))-1]
					clean_module_list.append(clean_module)
					print(f"--/ MODULE : {clean_module}")
				tofu.module_list = clean_module_list
				print("\n==============================================================")
			elif option == "use" or option.startswith("use "):
				if option == "use":
					module_to_use = input("[module to use] >> ")
				else:
					module_to_use = option[4:]
				module_to_use = module_to_use.strip()
				if tofu.check_valid_module(module_to_use):
					print("[+] Valid module")
					tofu.load_module(module_to_use)
				else:
					print("[-] Invalid module name, try running 'modules' again")
				
				
			elif option == "":
				pass
			else:
				print("[-] Invalid option")
				tofu.help()
						
			
		
if __name__ == '__main__':
		tofu.__main__()
