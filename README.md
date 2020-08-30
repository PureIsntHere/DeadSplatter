# DeadSplatter
Dedicated Server manager for Dead Matter Servers.

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

[![DeepSource](https://static.deepsource.io/deepsource-badge-light-mini.svg)](https://deepsource.io/gh/PurityWasHere/Dead-Matter-Server-Installer/?ref=repository-badge)

DeadSplatter is a Server Manager for Optimizing, Updating, And keeping Dead Matter servers healthy and online.


DeadSplatter is CONSTANTLY Checking your server's health.

It can monitor your Server's ram usage and your system usage.

If your server's health is declining because of memory leaks it will be automatically restarted.

If your server goes down for any reason DeadSplatter will bring it back ASAP.

DeadSplatter also keeps your systems ram clean by clearing it on a timer. By doing this your server health and uptime is increased.


**Features**

1) Fully customizable server path and ram cutoffs.

2) LightWeight and performance friendly (lightest weight manager that monitors memory usage)

3) Monitors server memory use and system memory use

4) Updater for server using SteamCMD (Backs up all config files.)

5) Automated Server Backups

6) Install a fresh server

7) Support for automatic logging in with SteamCMD. If a username and password are supplied in config the script will automatically login

8) Simple functionality. DeadSplatter can install, update, and manage servers with a single command.  

**How To Use**

1) Download Source

2) Install python and requirements if not already installed

3) Customize config.json to your needs.

Example: "max_ram":50 <- Max amount of ram the server can use before it is restarted. 

Example2: "max_system_ram":50 <- Max amount of ram load the entire system can be under until it is restarted. (Used in fallback mode if the script can't get proper permissions)

4) Run Main.py through cmd using python Main.py

*To Disable / Enable Features check Config.json*

**To Do List**

1)I̶n̶t̶e̶g̶r̶a̶t̶e̶ ̶S̶t̶e̶a̶m̶C̶M̶D̶

2)I̶n̶t̶e̶g̶r̶a̶t̶e̶ ̶U̶p̶d̶a̶t̶i̶n̶g̶ ̶S̶e̶r̶v̶e̶r̶s̶

3)I̶n̶t̶e̶g̶r̶a̶t̶e̶ ̶I̶n̶s̶t̶a̶l̶l̶i̶n̶g̶ ̶S̶e̶r̶v̶e̶r̶s̶

4)Maintain Performance

**Known Issues**
1) Certain Windows Server Builds have weird permissions that cause the script to run in failsafe mode 24/7
Possible fix for some users is to run through elevated Powershell.
If Powershell workaround doesn't work you'll have to use fallback mode. There's not much i can do about Windows servers weird ass permissions 
