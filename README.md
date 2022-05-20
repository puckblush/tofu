# tofu
A modular tool for hacking offline Windows filesystems and bypassing login screens. Can do hashdumps, OSK-Backdoors, user enumeration and more. <br> 
<img src="https://raw.githubusercontent.com/puckblush/tofu/main/tofu.png"></img>

<h1> How it works : </h1>
When a Windows machine is shut down, unless it has Bitlocker or another encryption service enabled, it's storage device contains everything stored on the device as if it was unlocked. This means that you can boot from an operating system on a bootable USB and access it's files - or even just connect the filesystem to another computer. <br>This tool helps for the part after booting from another OS (like linux) or connecting the filesystem to another computer; it has utilities that can dump NTLM password hashes, list users, install backdoors to spawn an elevated command prompt at the login screen and more. 

<h1>How to use the osk_backdoor : </h1>
1. Restart the Windows computer and as it's turning on, boot from a linux bootable USB (this process varies from computer to computer)<br>
2. Download tofu, set it up and run it<br>
3. Use the 'osk_backdoor.py' module after setting the options<br>
4. Restart the computer, this time booting into Windows<br>
5. In the accessibility settings (bottom right), select 'On Screen Keyboard'<br>
6. Wait/Press 'On Screen Keyboard' again until it works<br>
7. Success!<br>
<b>If you encountered an error along the lines of "CMD.exe does not exist at PATH", it could be an IO error; You can confirm this by trying to browse to the drive in the file explorer</b><br>

<h1>Modules : </h1>
Because tofu works on modules, it can be expanded for different purposes. See the 'modules' section for examples.<br>
Current Modules:<br>
1. <i>hashdump.py</i> - Dumps NTLM hashes from the target Windows filesystem<br>
2. <i>osk_backdoor.py</i> - Backdoor osk.exe to bypass the login; also includes an 'unbackdoor' module<br>
3. <i>list_users.py</i> - List the users with a profile on the Windows filesystem<br>
4. <i>chrome_history.py</i> - Dump chrome history of all users on the Windows filesystem<br>
5. <i>get_dpapi_masterkeys.py</i> - Dump DPAPI master keys from the Windows filesystem<br>
6. <i>enum_unattend.py</i> - Enumerate unattend files<br>
7. <i>memory_strings.py</i> - Search through the memory of the computer to find data<br>
8. <i>startup.py</i> - Inject a program into a user's startup directory<br>

<h1>Usage : </h1>
'list' : List all storage devices at /dev/ with a format of MSDOS, NTFS or -FVE-FS- (BITLOCKER) ; This will load the drive paths into memory<br>
'usedrive' : Set the drive to use; can use numbers assigned from the 'list' command<br>
'modules' : List modules ; This will load the module names into memory, so you need to run this command before selecting a module<br>
'use' : Use the selected module<br>

<h1>Setup : </h1>
 <b>(need to run as root because PyPyKatz' import path directory is dependent on the current user, and this needs to run as root)</b><br>
<i>sudo pip3 install -r requirements.txt<br>
sudo python3 tofu.py</i>
<h2> Built With : </h2>
<a href = "https://github.com/Legrandin/pycryptodome">PyCryptodome</a><br>
<a href="https://github.com/skelsec/pypykatz">PypyKatz</a><br>

<h3><b>Warning : If you're writing a module, make sure it won't do any damage before running it<br> </b></h3>

