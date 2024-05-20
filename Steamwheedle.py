import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date, datetime
from calendar import timegm
import math

scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
#sheet = client.open_by_key('1l4u48cnXD3ORIDJiXebrhw7QVkhtie92oQ5niGmB0Nw') #Live
sheet = client.open_by_key('1PYRSgh3asyZpzTWA-6BbnwoaUCyttTZXMYgZc_KLXKY') #Local
#sheet = client.open_by_key('1zoz4k7uxlQkQ82WZEUcGBNQEEIS15KKgsy818rYKdac') #Dev
sheet = sheet.worksheet("Steamwheedle")

guilds = [203585612, 199066642, 467715881, 469001351, 439520221, 200915262, 439001941, 200912272, 200875392, 52083073, 437378721, 51433483, 437956461, 438015331, 439021421, 437262641, 439157421, 202782692, 466689451, 199002432, 468022961, 202672512, 466386371, 466184131, 467766291, 466295671, 466419191]

row = 4
for guildID in guilds:
    guild = requests.get(f"https://api.warcraftrumble.gg/guild/{str(guildID)}").json()
    totalSkulls = 0
    memberCount = 0
    for member in guild["data"]["members"]:
        memberCount += 1
        totalSkulls += int(member["skulls"])
    averageSkulls = math.floor(totalSkulls/memberCount)
    lastupdated = date.today().strftime("%d %B %Y")
    cell_list = sheet.range(f"E{str(row)}:I{str(row)}")
    for i, val in enumerate([str(averageSkulls), "", memberCount, "", lastupdated]):
        if val != "":
            cell_list[i].value = val
    sheet.update_cells(cell_list, value_input_option='USER_ENTERED')
    row +=1
