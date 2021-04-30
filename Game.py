""" This is a Texas Hold 'Em Game for my final project.

Author: Nicholas Lueth
Class: CSI-260-01
Assignment: Final Project
Due Date: April 30th, 2021 @11:00 AM

Certification of Authenticity:
I certify that this is entirely my own work, except where I have given
fully-documented references to the work of others. I understand the definition
and consequences of plagiarism and acknowledge that the assessor of this
assignment may, for the purpose of assessing this assignment:
- Reproduce this assignment and provide a copy to another member of academic
- staff; and/or Communicate a copy of this assignment to a plagiarism checking
- service (which may then retain a copy of this assignment on its database for
- the purpose of future plagiarism checking)
"""
# Imports
import random
import os
# Global variables
ranks = [str(n) for n in range(2, 11)] + ["Jack", "Queen", "King", "Ace"]
suits = ["Spades", "Diamonds", "Clubs", "Hearts"]
base_path = os.path.dirname(__file__)
card_path = base_path + "\\images\\cards\\"


class Deck:
    def __init__(self):
        """
        This method initializes the Deck object.
        """
        self.deck = self.generate_deck()

    def __str__(self):
        """
        This method allows the object to be referenced as a string.
        :return: (str) formatted string
        """
        return_string = ""
        for card in self.deck:
            return_string += str(card)
            return_string += "\n"
        return return_string

    def shuffle(self):
        """
        This method shuffles the deck.
        :return: (list of Card objects) shuffled list of cards
        """
        return random.shuffle(self.deck)

    def remove_card(self, index):
        """
        This method removes a card from the deck.
        :param index: (int) index of the card to be removed
        """
        self.deck.remove(index)

    def find_card(self, rank, suit):
        """
        This method finds a card.
        :param rank: (str) rank of the card to find
        :param suit: (str) suit of the card to find
        :return: Either (Card object) or (None)
        """
        for card in self.deck:
            if card.rank == rank and card.suit == suit:
                return card
        return None

    @staticmethod
    def generate_deck():
        """
        This method generates a deck.
        :return: (list of Card objects) the new deck
        """
        deck = []
        for suit in suits:
            for rank in ranks:
                if rank.isnumeric():
                    img_str = card_path + rank + suit[0] + ".png"
                else:
                    img_str = card_path + rank[0] + suit[0] + ".png"
                deck.append(Card(rank, suit, img_str, True))
        return deck


class Card:
    def __init__(self, rank, suit, image, hidden):
        """
        This method initializes the Card object.
        :param rank: (str) rank of the card
        :param suit: (str) suit of the card
        :param image: (image render) the image
        :param hidden: (bool) whether the card should be visible or not
        """
        self.rank = rank
        self.suit = suit
        self.image = image
        self.hidden = hidden

    def __str__(self):
        """
        This method allows the object to be referenced as a string.
        :return: (str) formatted string
        """
        return f"{self.rank} of {self.suit}"

    def flip(self):
        """
        This method flips a card.
        """
        self.hidden = not self.hidden


class Player:
    # Starting ID
    _id = 1
    # A list containing all of the players
    _all_players = []
    # The initial call value
    _call_to = 1000

    def __init__(self, name, money, hand):
        """
        This method initializes the Player object.
        :param name: (str) name of the player
        :param money: (float) amount of starting money
        :param hand: (Hand object) player's hand
        """
        self.name = name
        self.money = money
        self.hand = hand
        # For roles
        self.big_blind = False
        self.small_blind = False
        self.dealer = False
        self.icon = None
        # Sub variables
        self.ID = Player._id
        self.in_pot = 0
        self.bot = False
        # Situational variables
        self.folded = False
        self.checked = False
        Player._id += 1
        Player._all_players.append(self)

    def __str__(self):
        """
        This method allows the object to be referenced as a string.
        :return: (str) formatted string
        """
        return f"""Name: {self.name}
        Bot: {self.bot}
        Money: {self.money}
        Hand: {self.hand}
        BB: {self.big_blind}
        SB: {self.small_blind}
        Dealer: {self.dealer}
        ID: {self.ID}
        Amount in pot: {self.in_pot}
        """

    def get_money(self):
        """
        This method returns a players total money.
        :return: (str) money
        """
        return f"Pot: ${self.money:,.2f}"

    def call(self, pot):
        """
        This method makes a call for a player's turn.
        :param pot: (Pot object) the pot
        """
        # Amount due
        amount = Player._call_to - self.in_pot
        # Ready for next
        self.checked = True
        # The player can't go in debt
        if self.money - amount < 0:
            # Set the player's money to 0 instead
            self.money = 0
            # Put their money in the pot
            self.in_pot += self.money
            Pot.add(pot, self.money)
        # If the player isn't going to go in debt then remove the amount due from the player's money
        else:
            self.money -= amount
            # Add the amount due to the pot
            self.in_pot += amount
            if amount < 0:
                amount = 0
            Pot.add(pot, amount)

    def fold(self):
        """
        This method makes a player fold for their turn.
        """
        self.folded = True
        self.checked = True

    def raise_pot(self, pot, amount):
        """
        This method makes a player raise the pot for their turn.
        :param pot: (Pot object) the pot
        :param amount: (int) The amount to raise the pot by
        """
        # Players who raise also call the last raise
        self.call(pot)
        Player._call_to += amount
        Pot.add(pot, amount)
        self.money -= amount
        self.in_pot += amount

    def set_dealer(self):
        """
        This method sets a player as a dealer.
        """
        self.dealer = True
        self.big_blind = False
        self.small_blind = False

    def set_small_blind(self):
        """
        This method sets a player as the small blind for $500.
        """
        self.dealer = False
        self.big_blind = False
        self.small_blind = True
        self.in_pot += 500

    def set_big_blind(self):
        """
        This method sets a player as the small blind for $1000.
        """
        self.dealer = False
        self.big_blind = True
        self.small_blind = False
        self.in_pot += 1000

    def reset(self):
        """
        This method resets the player.
        """
        self.icon = None
        self.in_pot = 0
        self.folded = False
        self.checked = False
        Player._call_to = 1000

    @staticmethod
    def get_players():
        """
        This method returns all of the players.
        :return: Player._all_players (list of Player objects) the players
        """
        return Player._all_players


class Pot:
    def __init__(self, value):
        """
        This method initializes the Pot object.
        :param value: (float) money in the pot
        """
        self.value = value

    def __str__(self):
        """
        This method allows the object to be referenced as a string.
        :return: (str) formatted string
        """
        return f"Pot: ${self.value:,.2f}"

    def add(self, amount):
        """
        This method adds money to the pot.
        :param amount: (float) The amount being added to the pot
        """
        self.value += amount

    def reset(self):
        """
        This method resets the pot back to 0.0.
        """
        self.value = 0.0


class Robot(Player):
    def __init__(self, name, money, hand):
        """
        This method initializes a Robot object.
        :param name: (str) name of the player
        :param money: (float) amount of starting money
        :param hand: (Hand object) player's hand
        """
        super().__init__(name, money, hand)
        self.bot = True


class Hand:
    """
    This method initializes a Hand object.
    """
    def __init__(self, cards):
        self.cards = cards

    def __str__(self):
        """
        This method allows the object to be referenced as a string.
        :return: (str) formatted string
        """
        return f"{self.cards[0]} and {self.cards[1]}"


class CommunityCards:
    def __init__(self, cards):
        """
        This method initializes a CommunityCards object.
        """
        self.cards = cards

    def __str__(self):
        """
        This method allows the object to be referenced as a string.
        :return: (str) formatted string
        """
        return f"{self.cards[0]}\n{self.cards[1]}\n{self.cards[2]}\n{self.cards[3]}\n{self.cards[4]}"
