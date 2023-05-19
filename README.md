# Fish shop 

### Table of content:
1. [Description](#description)
2. [Objective of project](#objective-of-project)
3. [Installing](#installing)
4. [Enviroment](#enviroment)
5. [Usage](#usage)
6. [Examples](#examples)
7. [Deployment](#deployment-on-a-server)

### Description 

Telegram bot for Denis fish shop via [moltin](https://www.moltin.com/) service.  
The bot can be used to place orders in the fish shop.  

### Objective of project

The bot is written for educational purposes within online courses for web developers [dvmn.org](https://dvmn.org/).  

### Installing

1. Python3 must be installed. 
Use `pip` (or `pip3`) for install requirements:
```
pip install -r requirements.txt
```  
2. Redis must be installed.  
```
sudo apt-get update
sudo apt-get install redis
```  
3. You need register on [elasticpath](https://www.elasticpath.com/):  
3.1 Create shop
3.2 Create products
3.3 Create pricebooks
3.4 Create and publish catalogs

### Enviroment

You needs to create .env file for the enviroment variables in main folder.

- `TG_BOT_TOKEN` - needs register a bot in telegram via https://t.me/BotFather
- `TG_CHAT_ID` - yours chat_id / user_id, you can check it via @userinfobot: https://t.me/userinfobot
- `TG_BOT_LOGGER_TOKEN` - register an additional bot for sending logs
- `LOGS_FOLDER` - destination folder for logs
- `LOGS_MAX_SIZE` - bot logs file maximum size in bytes
- `LOGS_BACKUP_COUNT` - bot logs file backup count
- `REDIS_HOST` - host's ip address (e.g. 'localhost')
- `REDIS_PORT` - port (default 6379)
- `ELASTIC_CLIENT_ID` - Elastic Path Product Experience Manager client ID you can get at https://www.elasticpath.com/
- `ELASTIC_CLIENT_SECRET` - Elastic Path Product Experience Manager client secret you can get at https://www.elasticpath.com/

### Usage
Before start the script, needs activate your bot via `/start` command in chat.

From scripts folder:
```
python(or python3) main.py
```
Alternate arguments:
- **-h / --help** - display shortly description of script and arguments. 
- **-d / --dest_folder** - destination folder for bot logs (by default use enviroment variable 'LOGS_FOLDER').
- **-m / --max_bytes** - bot logs file maximum size in bytes (by default use enviroment variable 'LOGS_MAX_SIZE').
- **-bc / --backup_count** - logs file backup count (by default use enviroment variable 'LOGS_BACKUP_COUNT').

Running example with arguments:  
`python main.py -bc 3`

### Examples  
* **Example of a Telegram bot**
 
link: [https://t.me/dvmnQuizbotbot  ](https://t.me/FishkaDevShopbot)
![1111](https://github.com/SadRus/chat-bots-no4/assets/79669407/27c28e2a-8c0d-4ca8-a975-697d227aff87)


### Deployment on a server

1. Log in to a server via username, server IP and password:  
`ssh {username}@{server IP}`
2. Clone repository. Advise to put the code in the `/opt/{project}/` folder
3. Put into the folder file with virtual enviroments `.env`
4. Create a virtual enviroment, use python(or python3):  
`python -m venv venv`
5. Follow Installing section above
6. Create a file(unit) in the `/etc/systemd/system` called like name project, e.g. `chat_bots_no5.service`, use:  
`touch /etc/systemd/system/{project}.service`
7. Write the following config into it:  
    * Execstart - for start the sevice
    * Restart - auto-restart the service if it crashes
    * WantedBy - for start service within server
```
[Service]  
ExecStart=/opt/{project}/venv/bin/python3 /opt/{project}/{main.py}
Restart=always

[Install]
WantedBy=multi-user.target
```  
8. Include the unit in the autoload list  
`systemctl enable {project}`
9. Reload systemctl  
`systemctl daemon-reload`
10. Start the unit  
`systemctl start {project}`
11. Logs will writing by enviroment variable `LOGS_FOLDER` path (for server use `/var/log/` path)
12. You can check the process:  
`ps -aux | grep {project}`  
If the process is running it will show something like this, depends on your project name:  
![image](https://user-images.githubusercontent.com/79669407/228650981-e6f8016a-40e6-4c4f-88ef-a3df6969d2fc.png)
13. if the bot is running bot logger will send a message like this:  
![image](https://user-images.githubusercontent.com/79669407/228651407-0473a366-5cab-4ac8-a346-8e8435ce402d.png)


