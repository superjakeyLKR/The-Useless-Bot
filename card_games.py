from random import randint, choice

suits = ["Hearts", "Diamonds", "Clubs", "Spades"]

def draw_card():
	card = face_card_check(str(randint(2, 14)))
	return card

def face_card_check(card):
	if card == "11":
		card = "Jack"
	elif card == "12":
		card = "Queen"
	elif card == "13":
		card = "King"
	elif card == "14":
		card = "Ace"
	return card + " of " + choice(suits)

def make_hands():
	cards = [str(randint(2, 14)), str(randint(2, 14)), str(randint(2, 14)), str(randint(2, 14))]
	newCards = ["", "", "", ""]
	i = 0
	for card in cards:
		card = face_card_check(card)
		newCards[i] = card
		i += 1
		print(card)
	return newCards

def value_hand(cards):
	print(cards)
	cardValue, aceCount, i = 0, 0, 0
	while i < len(cards):
		if cards[i][0] != "J" and cards[i][0] != "Q" and cards[i][0] != "K" and cards[i][0] != "A":
			cardValue += int(cards[i][0])
		elif cards[i][0] != "A":
			cardValue += 10
		else:
			cardValue += 11
			aceCount += 1
		i += 1
	else:
		while aceCount > 0 and cardValue > 21:
			cardValue -= 10
			aceCount -= 1
	return cardValue

	