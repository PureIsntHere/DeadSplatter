Pures Server Manager v0.5

Simple Python Script to monitor memory leaks / crashes for DeadMatter Servers.

Requirements:
Python 3.8
psutil (pip install psutil)

How To Use:

1) Once you have python installed go into the config.json thats included.

2) Change values to whats needed for your server. IE: Max ram usage before server restart (For memory leaks) Make sure to set max_ram and max_system_ram

max_ram is what you want the max server usage to be before the server restarts. if for whatever reason the script cant detect the server's memory usage it will fallback and use max_system_ram.

3) Start the script. The script will automatically start your sever if you have the path added in your config.json

4) If you close the script it will also close the server it is currently managing if that server is in the booting stages. Once the server boots it will not be a child process anymore.



note: your directory needs to be double slashed. so in config.json when you set the path it should look like E:\\SteamLibrary\\steamapps\\common\\Dead_Matter_Dedicated_Server\\ for example.

note: Max Ram value is the maximum amount of ram that the server itself can use before it restarts.

note: RamCleaner.bat is a file that will clear up ram every 60 seconds. It does not clean the servers Ram specifically. 

note: High Priority module will attempt to set your server to high priority. It is set to true by default. If you dont want this set it to false in the config.json.