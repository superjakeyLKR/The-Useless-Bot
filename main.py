import os
import random
import requests
import json
import discord
from replit import db
from keep_alive import keep_alive
import card_games

client = discord.Client()

greetings = ["Hello!", "Hi!", "Good morning/afternoon!", "What's up?"]

ownerOnly = "Sorry, but you can't do that unless you're ˢᵘᵖᵉʳʲᵃᵏᵉʸ#5268"

def get_quote():
	response = requests.get("https://zenquotes.io/api/random")
	jsonData = json.loads(response.text)	  
	quote = jsonData[0]["q"] + " -" + jsonData[0]["a"]
	return(quote)

def add_a_message(message):
	if "useraddedmessages" in db.keys():
		messages = db["useraddedmessages"]
		messages.append(message)
		db["useraddedmessages"] = messages
	else:
		db["useraddedmessages"] = [message]

def delete_message(index):
	messages = db["useraddedmessages"]
	if len(messages) > index:
		del messages[index]
		db["useraddedmessages"] = messages

def delete_all_messages():
	if "useraddedmessages" in db.keys():
		del db["useraddedmessages"]

@client.event
async def on_ready():
	print("{0.user} is now online.".format(client))


@client.event
async def on_message(message):
	if message.author == client.user:
		return
		
	msg = message.content

	if msg.startswith("_hello"):
		await message.channel.send(random.choice(greetings))

	elif msg.startswith("_quote"):
		await message.channel.send(get_quote())

	elif msg.startswith("_usermessage") or msg.startswith("_um"):
		if "useraddedmessages" in db.keys():
			await message.channel.send(random.choice(db["useraddedmessages"]))
		else:
			await message.channel.send("There are no user added messages")	

	elif msg.startswith("_newmessage"):
		temp = msg.split("_newmessage ", 1)[1]
		temp += " (by " + str(message.author) + ")"
		add_a_message(temp)
		await message.channel.send("Added new message: " + temp)
	
	elif msg.startswith("_nm"):
		temp = msg.split("_nm ", 1)[1]
		temp += " (by " + str(message.author) + ")"
		add_a_message(temp)
		await message.channel.send("Added new message: " + temp)
	
	elif msg.startswith("_myname"):
		print(str(message.author))
		await message.channel.send("Your name is " + str(message.author))

	elif msg.startswith("_deleteusermessage"):
		if str(message.author == "ˢᵘᵖᵉʳʲᵃᵏᵉʸ#5268"):
			msgs = []
			if "useraddedmessages" in db.keys():
				index = int(msg.split("_deleteusermessage", 1)[1])
				delete_message(index)
				msgs = db["useraddedmessages"]
				await message.channel.send("Message {} successfully deleted. Remaning messages: {}".format(index, msgs))
			else:
				await message.channel.send("That message doesn't exist.")
		else:
			await message.channel.send(ownerOnly)

	elif msg.startswith("_dum"):
		if str(message.author == "ˢᵘᵖᵉʳʲᵃᵏᵉʸ#5268"):
			msgs = []
			if "useraddedmessages" in db.keys():
				index = int(msg.split("_dum", 1)[1])
				delete_message(index)
				await message.channel.send("Message {} successfully deleted. Remaning messages: {}".format(index, msgs))
			else:
				await message.channel.send("That message doesn't exist.")
		else:
			await message.channel.send(ownerOnly)
		
	elif msg.startswith("_deleteallmessages") or msg.startswith("_dam"):
		if str(message.author == "ˢᵘᵖᵉʳʲᵃᵏᵉʸ#5268"):
			await message.channel.send("Are you sure you want to delete all user messages? Type \"_cda\" if yes, and \"_dda\" if not. (Without \")")
		else:
			await message.channel.send(ownerOnly)

	elif msg.startswith("_cda"):
		if not str(message.author == "ˢᵘᵖᵉʳʲᵃᵏᵉʸ#5268"):
			await message.channel.send(ownerOnly)
		else:
			delete_all_messages()
			await message.channel.send("Successfully deleted all user messages.")

	elif msg.startswith("_dda"):
		if not str(message.author == "ˢᵘᵖᵉʳʲᵃᵏᵉʸ#5268"):
			await message.channel.send(ownerOnly)
		else:
			await message.channel.send("Cancelling delete all request.")
			
	elif msg.startswith("_blackjack"):
		if not str(message.author) + "playingblackjack" in db.keys():
			await message.channel.send("Starting new game of blackjack...")
			cards = card_games.make_hands()
			playerCards = [cards[0], cards[1]]
			value = card_games.value_hand(playerCards)
			await message.channel.send("You have a {} and a {}, and the dealer has a {} and a face-down card. Your hand value is {}, and you are not bust.".format(cards[0], cards[1], cards[2], value))
			db[str(message.author) + "playingblackjack"] = cards
			await message.channel.send("You can either draw a card (_bj draw), stick (_bj stick), or fold (_bj fold or _bj end).")
		else:
			await message.channel.send("You are already in a blackjack game!")
		
	elif msg.startswith("_bj draw"):
		if str(message.author) + "playingblackjack" in db.keys():
			newCard = card_games.draw_card()
			playerCards = [db[str(message.author) + "playingblackjack"][0], db[str(message.author) + "playingblackjack"][1], newCard] 
			i = 0
			text = "You have a "
			while i + 2 < len(playerCards):
				text += playerCards[i] + ", a "
				i += 1
			else:
				text += playerCards[i] + " and a " + playerCards[i + 1] + "."
			await message.channel.send(text)
		else:
			await message.channel.send("You aren't playing blackjack!")

	elif msg.startswith("_bj end") or msg.startswith("_bj fold"):
		if str(message.author) + "playingblackjack" in db.keys():
			del db[str(message.author) + "playingblackjack"]
			await message.channel.send("Successfully ended blackjack game.")
		else:
			await message.channel.send("You have to start a blackjack game to end it, stupid.")
	elif msg.startswith("_help") or msg.startswith("_?"):
		await message.channel.send("""```List of commands (prefix is \"_\"):
•	help/?: Brings up this menu.
•	hello: Greets you.
•	quote: Gives you a random quote.
•	usermessage/um: Shows you a random user-made message.
•	newmessage/nm: Allows you to add your own message (Don't put anything that violates the rules.)
•	myname: Tells you your name.```""")

keep_alive()
client.run(os.environ["TOKEN"])
