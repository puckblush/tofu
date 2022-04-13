# tofu
A quick, easy and modular tool for hacking offline Windows drives and bypassing login screens. Can do hashdumps, OSK-Backdoors, user enumeration and more.<br> 
<img src="https://raw.githubusercontent.com/stoatsec/tofu/main/tofu.png"></img>

<h2> How it works : </h2>
When a Windows machine is shut down, unless it has Bitlocker or another encryption service enabled, it's hard drive contains everything stored on the device as if it was unlocked. This means that you can boot from an operating system from a bootable USB and access it's files - or even just connect the hard drive to another computer. This tool helps for the part after booting from another OS (like linux); it has utilities that can dump NTLM password hashes, list users and install backdoors to spawn an elevated command prompt at the login screen. 

<h2>How to use the osk_backdoor : </h2>
1. Restart the Windows computer and as it's turning on, boot from a linux bootable USB (this process varies from computer to computer)<br>
2. Download tofu and run it<br>
3. Use the 'osk_backdoor.py' module after setting the options<br>
4. Restart the computer, this time booting into Windows<br>
5. In the accessibility settings (bottom right), select 'On Screen Keyboard'<br>
6. Wait/Press 'On Screen Keyboard' again<br>
7. Success!<br>

<h2>Modules : </h2>
Because tofu works on modules, it can be constantly expanded for different purposes. See the 'modules' section for examples.<br>
Current Modules:<br>
1. <i>hashdump.py</i> - Dumps NTLM hashes from the target hard drive<br>
2. <i>osk_backdoor.py</i> - Backdoor osk.exe to bypass the login; also includes an 'unbackdoor' module<br>
3. <i>list_users.py</i> - List the users with a profile on the hard drive<br>

<h2>Usage : </h2>
'list' : List all hard drives at /dev/ with a format of MSDOS, NTFS or -FVE-FS- (BITLOCKER) ; This will load the drive paths into memory<br>
'usedrive' : Set the drive to use; can use numbers assigned from the 'list' command<br>
'modules' : List modules ; This will load the module names into memory, so you need to run this command before selecting a module<br>
'use' : Use the selected module<br>

<h2>Setup : </h2><i>
pip3 install -r requirements.txt<br>
sudo python3 tofu.py</i>

<h3><b>Warning : If you're writing a module, make sure it won't do any damage before running it<br> </b></h3>

