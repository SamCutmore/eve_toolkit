import requests
import csv

# Actually none of this is probably needed
import discord
intents = discord.Intents.default() 
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)

### CONFIG 
regions_to_watch = ["Placid", "Black Rise"]
ship_group_to_watch = 27

# https://zkillboard.com/group/4803/ serpentis officer cruiser
# https://zkillboard.com/group/4804/ serpentis officer frigate
# https://zkillboard.com/group/4795/ angel officer cruiser
# https://zkillboard.com/group/4796/ angel officer frigate
### CONFIG END


def get_type_ids(csv_file, market_group):
    type_ids = []

    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        for row in reader:
            # Assuming type_id is the first column (index 0) and group_id is the second column (index 1)
            if row[1] == market_group:
                type_ids.append(int(row[0]))

    return type_ids

def get_type_ids_with_names(csv_file, market_group):
    type_ids_with_names = {}

    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        for row in reader:
            # Assuming type_id is the first column (index 0) and group_id is the second column (index 1)
            if row[1] == market_group:
                type_id = int(row[0])
                name = row[2]  # Assuming name is the third column (index 2)
                type_ids_with_names[type_id] = name

    return type_ids_with_names

def get_region_and_system_name(solar_system_id):
    solarsystems_file_path = 'mapSolarSystems.csv'
    regions_file_path = 'mapRegions.csv'
    region_id = None
    solar_system_name = None

    with open(solarsystems_file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None) # Skip the header row
        for row in reader:
            # Assuming solar_system_id is the third column (index 2)
            if int(row[2]) == solar_system_id:
                region_id = int(row[0])  # Assuming region_id is the first column (index 0)
                solar_system_name = row[3]  # Assuming solar_system_name is the fourth column (index 3)
                break  # No need to continue searching after finding the match
    with open(regions_file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)

        for row in reader:
            if int(row[0]) == region_id:
                region_name = str(row[1]) 
                break  # No need to continue searching after finding the match

    return region_name, solar_system_name

def get_type_name(type_id):
    inv_types_file_path = "invTypes-nodescription.csv"
    type_name = None
    with open(inv_types_file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)

        for row in reader:
            if int(row[0]) == type_id:
                type_name = str(row[2]) 
                break
    return type_name

csv_file_path = 'invTypes-nodescription.csv'
market_group_id = str(ship_group_to_watch)

type_ids_with_names = get_type_ids_with_names(csv_file_path, market_group_id)
target_ship_type_ids = get_type_ids(csv_file_path, market_group_id)
print (f"Looking for {len(target_ship_type_ids)} ship types in {len(regions_to_watch)} regions")
# TODO implement region filter

import time

api_url = "https://redisq.zkillboard.com/listen.php?queueID=SET_YOUR_ID_here"
#target_ship_type_ids = [11393, 29988, 29984]

### trying to connect with webhook
discord_webhook_url = "https://discord.com/api/webhooks/PLACE_YOUR_KEY_HERE"
#payload = {
#    "content" : outbound_message,
#    "username" : "ZKill Spy"
#}
#payload["embeds"] = [
#    {
#        "description" : "text in embed",
#        "title" : "embed title"
#    }
#]
#send_to_webhook = requests.post(discord_webhook_url, json = payload)



def fetch_data():
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            #print("Received data:", data)
            #print("New killmail!")
            solar_system_id = data.get("package", {}).get("killmail", {}).get("solar_system_id")
            region_name, system_name = get_region_and_system_name(solar_system_id)
            killmail_id = solar_system_id = data.get("package", {}).get("killID")
            zkill_link = f"https://zkillboard.com/kill/{killmail_id}/"
            print(f"Kill in solar system: {system_name} in {region_name}. Kill ID {killmail_id}")
            # TODO Implement region filtering
            # TODO check if system is in jump range of Oulley or Aubenall


            # Check if the ship_type_id is in the list of target_ship_type_ids
            attackers = data['package']['killmail']['attackers']
            for attacker in attackers:
                #print("checking attacker")
                #solar_system_id = data['solar_system_id']
                ship_type_id = attacker.get('ship_type_id')
                if region_name in regions_to_watch:
                    print (f"yay! A kill in {region_name}")
                    if ship_type_id in target_ship_type_ids:
                        ship_name = type_ids_with_names[ship_type_id]
                        outbound_message = f"Someone used {ship_name} to kill som'n in {system_name} in {region_name}. Link: {zkill_link}"
                        print(outbound_message)


                        # Check if the ship_type_id is in the result
                        if ship_type_id in type_ids_with_names:
                            #print("Received data:", data)
                            print(f"Attempting to send a message")
                            payload = {
                                "content" : outbound_message,
                                "username" : "ZKill Spy"
                            }
                            send_to_webhook = requests.post(discord_webhook_url, json = payload)
                            try:
                                send_to_webhook.raise_for_status()
                            except requests.exceptions.HTTPError as err:
                                print(err)
                            else:
                                print("Payload delivered successfully, code {}.".format(send_to_webhook.status_code))
                        break

                # check if using officer weapon
                attacker_weapon_id = attacker.get('weapon_type_id')
                attacker_weapon_name = get_type_name(attacker_weapon_id)
                #if "'s Modified" in attacker_weapon_name:
                if "'s Modified" in attacker_weapon_name:
                    outbound_message = f"Someone used {attacker_weapon_name} to kill som'n in {system_name} in {region_name}. Link: {zkill_link}"
                    print(outbound_message)
                    print(f"Attempting to send a message")
                    payload = {
                        "content" : outbound_message,
                        "username" : "ZKill Spy"
                    }
                    send_to_webhook = requests.post(discord_webhook_url, json = payload)
                    try:
                        send_to_webhook.raise_for_status()
                    except requests.exceptions.HTTPError as err:
                        print(err)
                    else:
                        print("Payload delivered successfully, code {}.".format(send_to_webhook.status_code))
                
                # TODO check if using smartbomb
                # TODO look for gatecamps in jump range
                
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
        print("No new killmails in the last 10 seconds")



if __name__ == "__main__":
    try:
        while True:
            fetch_data()
            time.sleep(0.1)  # Wait for 0,1 seconds before the next request
    except KeyboardInterrupt:
        print("Script terminated by user.")


# Run the bot with your token
#client.run('discord_bot_token_here')