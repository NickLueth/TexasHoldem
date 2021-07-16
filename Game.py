"""Texas Hold 'Em in Python

Author: Nicholas Lueth

Certification of Authenticity:
I certify that this is entirely my own work, except where I have given
fully-documented references to the work of others. I understand the definition
and consequences of plagiarism and acknowledge that the assessor of this
assignment may, for the purpose of assessing this assignment:
- Reproduce this assignment and provide a copy to another member of academic
- staff; and/or Communicate a copy of this assignment to a plagiarism checking
- service (which may then retain a copy of this assignment on its database for
- the purpose of future plagiarism checking)

Sources:
- https://github.com/monicanagent/cypherpoker.js (card png files)
- http://www.pngall.com/playing-cards-png/download/38939 (icon)
- https://www.wikihow.com/Program-a-Game-in-Python-with-Pygame (Research)
- https://www.youtube.com/watch?v=FfWpgLFMI7w&ab_channel=freeCodeCamp.org (Research)
- https://www.geeksforgeeks.org/how-to-create-buttons-in-a-game-using-pygame/ (Research)
"""
import random
import os
from time import sleep

values = [str(n) for n in range(2, 11)] + ["Jack", "Queen", "King", "Ace"]
suits = ["Spades", "Diamonds", "Clubs", "Hearts"]
base_path = os.path.dirname(__file__)
card_path = base_path + "\\images\\cards\\"

CANVAS_WIDTH = 1280
CANVAS_HEIGHT = 720
CARD_WIDTH = 112
CARD_HEIGHT = 156
resolution = (CANVAS_WIDTH, CANVAS_HEIGHT)
colors = {"white": (255, 255, 255), "black": (0, 0, 0), "red": (255, 0, 0), "green": (14, 160, 60)}
base_path = os.path.dirname(__file__)
image_path = base_path + "/images/"


class Deck:
    def __init__(self):
        """
        This method initializes the deck.
        """
        self.cards = self.generate_deck()

    def __str__(self):
        """
        This method creates a printable string for the object.
        :return: return_string (str) A printable string
        """
        return_string = "\n"
        for card in self.cards:
            return_string += str(card)
            return_string += "\n"
        return return_string

    def shuffle(self):
        """
        This method shuffles the deck.
        :return: a shuffled list of cards
        """
        return random.shuffle(self.cards)

    def remove_card(self, index):
        """
        This method removes a card from the deck.
        :param index: (int) The index of the card being removed
        """
        self.cards.remove(index)

    def find_card(self, value, suit):
        for card in self.cards:
            if card.value == value and card.suit == suit:
                return card
        return None

    @staticmethod
    def generate_deck():
        """
        This method creates a full deck of cards minus the jokers.
        :return: deck (list of Card Objects) A full deck of cards
        """
        deck = []
        for suit in suits:
            for value in values:
                if value.isnumeric():
                    img_str = card_path + value + suit[0] + ".png"
                else:
                    img_str = card_path + value[0] + suit[0] + ".png"
                deck.append(Card(value, suit, img_str, True))
        return deck


class Card:
    def __init__(self, value, suit, image, hidden):
        """
        This method initializes a card.
        :param value: (int) the card's rank
        :param suit: (string) the card's suit

        """
        self.value = value
        self.suit = suit
        self.image = image
        self.hidden = hidden

    def __str__(self):
        """
        This method creates a printable string for the object.
        :return: (str) A printable string
        """
        return f"{self.value} of {self.suit}"

    def flip(self):
        """
        This method flips a card
        """
        self.hidden = not self.hidden

    def scale_card(self, pygame):
        if self.hidden:
            return pygame.transform.smoothscale(pygame.image.load(image_path + "\\cards\\CB.png"), (112, 156))
        else:
            if self.value.isnumeric():
                img_str = "\\cards\\" + self.value + self.suit[0] + ".png"
            else:
                img_str = "\\cards\\" + self.value[0] + self.suit[0] + ".png"
            return pygame.transform.smoothscale(pygame.image.load(image_path + img_str), (112, 156))

    @staticmethod
    def simplify_cords(x, y):
        card_x = x - (CARD_WIDTH / 2)
        card_y = y - (CARD_HEIGHT / 2)
        return tuple((card_x, card_y))


class Player:
    _id = 1
    _all_players = []
    _call_to = 100

    def __init__(self, name, money, hand):
        """
        This method initializes a player.
        :param name: (str) The name of the player
        :param money: (float) The amount of money the player has
        :param hand: (list of card objects) Cards in the player's hand
        """
        self.name = name
        self.money = money
        self.hand = hand
        self.big_blind = False
        self.small_blind = False
        self.dealer = False
        self.icon = None
        self.ID = Player._id
        self.in_pot = 0
        self.folded = False
        self.checked = False
        self.bot = False
        # Hands (Used for implementing the auto win function)
        self.has_rf = False
        self.has_sf = False
        self.has_4oak = False
        self.has_fh = False
        self.has_f = False
        self.has_s = False
        self.has_3oak = False
        self.has_2p = False
        self.has_1p = False
        self.high_card = None
        Player._id += 1
        Player._all_players.append(self)

    def __str__(self):
        """
        This method creates a printable string for the object.
        :return: (str) A printable string
        """
        return f"""Name: {self.name}
        Money: {self.money}
        Hand: {self.hand}
        BB: {self.big_blind}
        SB: {self.small_blind}
        Dealer: {self.dealer}"""

    def get_money(self):
        return f"Pot: ${self.money:,.2f}"

    def show_hands(self):
        for card in self.hand.cards:
            card.flip()

    def call(self, pot):
        """
        This method makes a call for the player's turn.
        """
        amount = Player._call_to - self.in_pot
        self.checked = True
        if self.money - amount < 0:
            self.money = 0
            self.in_pot += self.money
            Pot.add(pot, self.money)
        else:
            self.money -= amount
            self.in_pot += amount
            if amount < 0:
                amount = 0
            Pot.add(pot, amount)

    def fold(self):
        """
        This method makes the player fold their hand.
        """
        self.folded = True
        self.checked = True

    def raise_pot(self, pot, amount):
        """
        This method has the player offer to raise the pot.
        :param pot: (Pot object) The pot
        :param amount: (float) The amount of money they would like to rise the pot by
        """
        self.call(pot)
        Player._call_to += amount
        Pot.add(pot, amount)
        self.money -= amount
        self.in_pot += amount

    def set_dealer(self):
        self.dealer = True
        self.big_blind = False
        self.small_blind = False

    def set_small_blind(self):
        self.dealer = False
        self.big_blind = False
        self.small_blind = True
        self.in_pot += 50

    def set_big_blind(self):
        self.dealer = False
        self.big_blind = True
        self.small_blind = False
        self.in_pot += 100

    def reset(self):
        self.icon = None
        self.in_pot = 0
        self.folded = False
        self.checked = False
        Player._call_to = 100

    def get_hand(self, deck):
        self.hand = Hand(tuple(deck[x] for x in range(2)))
        for x in range(1, -1, -1):
            deck.remove(deck[x])

    @staticmethod
    def get_players():
        return Player._all_players


class Pot:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"Pot: ${self.value:,.2f}"

    def add(self, amount):
        self.value += amount

    def reset(self):
        self.value = 0.0


class Robot(Player):
    def __init__(self, name, money, hand):
        """
        This method initializes a robot.
        :param name: (str) The name of the robot
        :param money: (float) The amount of money the robot has
        :param hand: (list of card objects) Cards in the robot's hand
        """
        super().__init__(name, money, hand)
        self.bot = True


class Hand:
    def __init__(self, cards):
        """
        This method initializes a robot.
        :param cards: (list of Card objects) The cards in the player's hand
        """
        self.cards = cards

    def __str__(self):
        """
        This method creates a printable string for the object.
        :return: (str) A printable string
        """
        return f"{self.cards[0]} and {self.cards[1]}"


class CommunityCards:
    def __init__(self, cards):
        self.cards = cards

    def __str__(self):
        """
        This method creates a printable string for the object.
        :return: (str) A printable string
        """
        return f"""
{self.cards[0]}
{self.cards[1]}
{self.cards[2]}
{self.cards[3]}
{self.cards[4]}
"""

    def show_community_cards(self, num):
        for i in range(num):
            self.cards[i].hidden = False


class Game:
    def __init__(self, window, deck, pot, pygame, fonts):
        # game = sessions
        self.sessions = 1
        self.fonts = fonts
        self.rounds = 1
        self.ending = False
        self.last_move = ""
        self.deck = deck
        self.deck.shuffle()
        self.pot = pot
        self.window = window
        self.players = self.get_players()
        self.community_cards = self.get_community_cards()
        self.raises_in_a_row = 0
        self.pygame = pygame
        self.buttons = self.load_items(pygame)

    def __str__(self):
        return f"""GAME OBJECT:
        Sessions: {self.sessions}
        Fonts: {self.fonts}
        Rounds: {self.rounds}
        Ending: {self.ending}
        Last move: {self.last_move}
        Deck: {self.deck}
        Pot: {self.pot}
        Players: {self.players}
        Community Cards: {self.community_cards}
        Raises in a row: {self.raises_in_a_row}
        """

    def get_players(self):
        robot_names = ["Eric (BOT)", "Jordan (BOT)", "Sam (BOT)", "Craig (BOT)", "Ryan (BOT)",
                       "Adam (BOT)", "Nate (BOT)", "Conor (BOT)", "Nina (BOT)", "Hayley (BOT)", "Shelsea (BOT)",
                       "Ben (BOT)", "Josh (BOT)", "Jimmy (BOT)"]
        picked_names = []
        while len(picked_names) < 3:
            i = random.randint(0, len(robot_names) - 1)
            if robot_names[i] not in picked_names:
                picked_names.append(robot_names[i])
        starting_cash = 5000.00
        player = Player("You", starting_cash, [])
        bot1 = Robot(picked_names[0], starting_cash, [])
        bot2 = Robot(picked_names[1], starting_cash, [])
        bot3 = Robot(picked_names[2], starting_cash, [])
        player.get_hand(self.deck.cards)
        bot1.get_hand(self.deck.cards)
        bot2.get_hand(self.deck.cards)
        bot3.get_hand(self.deck.cards)
        return [player, bot1, bot2, bot3]

    def get_community_cards(self):
        cards = tuple(self.deck.cards[x] for x in range(5))
        for x in range(4, -1, -1):
            self.deck.cards.remove(self.deck.cards[x])
        community = CommunityCards(cards)
        return community

    def load_items(self, pygame):
        pc1 = self.players[0].hand.cards[0].scale_card(pygame)
        pc2 = self.players[0].hand.cards[1].scale_card(pygame)
        if not self.players[0].folded:
            self.window.blit(pc1, Card.simplify_cords((CANVAS_WIDTH / 2) - 70, CANVAS_HEIGHT - (CARD_HEIGHT / 2)))
            self.window.blit(pc2, Card.simplify_cords((CANVAS_WIDTH / 2) + 70, CANVAS_HEIGHT - (CARD_HEIGHT / 2)))
        # Player Profile
        profile_background = pygame.image.load(base_path + "/images/other/Profile.png")
        pp_x = CANVAS_WIDTH - profile_background.get_width()
        pp_y = CANVAS_HEIGHT - profile_background.get_height()
        self.window.blit(profile_background, (pp_x, pp_y))

        # Bot 1 cards
        b1c1 = self.players[1].hand.cards[0].scale_card(pygame)
        b1c2 = self.players[1].hand.cards[1].scale_card(pygame)
        b1c1 = pygame.transform.rotate(b1c1, -90)
        b1c2 = pygame.transform.rotate(b1c2, -90)
        if not self.players[1].folded:
            self.window.blit(b1c1, Card.simplify_cords(CARD_WIDTH / 2, (CANVAS_HEIGHT / 2) - 70))
            self.window.blit(b1c2, Card.simplify_cords(CARD_WIDTH / 2, (CANVAS_HEIGHT / 2) + 70))
        # Bot 1 Profile
        b1p_x = 0
        b1p_y = CANVAS_HEIGHT - profile_background.get_height()
        self.window.blit(profile_background, (b1p_x, b1p_y))

        # Bot 2 cards
        b2c1 = self.players[2].hand.cards[0].scale_card(pygame)
        b2c2 = self.players[2].hand.cards[1].scale_card(pygame)
        b2c1 = pygame.transform.rotate(b2c1, 180)
        b2c2 = pygame.transform.rotate(b2c2, 180)
        if not self.players[2].folded:
            self.window.blit(b2c1, Card.simplify_cords((CANVAS_WIDTH / 2) - 70, CARD_HEIGHT / 2))
            self.window.blit(b2c2, Card.simplify_cords((CANVAS_WIDTH / 2) + 70, CARD_HEIGHT / 2))
        # Bot  2 Profile
        b2p_x = 0
        b2p_y = 0
        self.window.blit(profile_background, (b2p_x, b2p_y))

        # Bot 3 cards
        b3c1 = self.players[3].hand.cards[0].scale_card(pygame)
        b3c2 = self.players[3].hand.cards[1].scale_card(pygame)
        b3c1 = pygame.transform.rotate(b3c1, 90)
        b3c2 = pygame.transform.rotate(b3c2, 90)
        if not self.players[3].folded:
            self.window.blit(b3c1, Card.simplify_cords((CARD_WIDTH / 2) + CANVAS_WIDTH - CARD_HEIGHT, (CANVAS_HEIGHT / 2) - 70))
            self.window.blit(b3c2, Card.simplify_cords((CARD_WIDTH / 2) + CANVAS_WIDTH - CARD_HEIGHT, (CANVAS_HEIGHT / 2) + 70))
        # Bot 3 Profile
        b3p_x = CANVAS_WIDTH - profile_background.get_width()
        b3p_y = 0
        self.window.blit(profile_background, (b3p_x, b3p_y))

        # Community cards
        cc1 = self.community_cards.cards[0].scale_card(pygame)
        cc2 = self.community_cards.cards[1].scale_card(pygame)
        cc3 = self.community_cards.cards[2].scale_card(pygame)
        cc4 = self.community_cards.cards[3].scale_card(pygame)
        cc5 = self.community_cards.cards[4].scale_card(pygame)
        self.window.blit(cc1, Card.simplify_cords((CANVAS_WIDTH / 2) - 250, CANVAS_HEIGHT / 2))
        self.window.blit(cc2, Card.simplify_cords((CANVAS_WIDTH / 2) - 125, CANVAS_HEIGHT / 2))
        self.window.blit(cc3, Card.simplify_cords((CANVAS_WIDTH / 2), CANVAS_HEIGHT / 2))
        self.window.blit(cc4, Card.simplify_cords((CANVAS_WIDTH / 2) + 125, CANVAS_HEIGHT / 2))
        self.window.blit(cc5, Card.simplify_cords((CANVAS_WIDTH / 2) + 250, CANVAS_HEIGHT / 2))
        # Pot
        pot_text = self.fonts[1].render(f"{self.pot}", True, colors["black"])
        self.window.blit(pot_text, ((CANVAS_WIDTH / 2) - (pot_text.get_width() / 2), (CANVAS_HEIGHT / 2) - 160))
        # Icons
        for player in self.players:
            player_name = self.fonts[0].render(player.name, True, colors["black"])
            player_money = self.fonts[0].render(str(player.get_money()), True, colors["black"])
            if player.ID == 1:
                if player.icon:
                    self.window.blit(player.icon, (CANVAS_WIDTH - (player.icon.get_width() + 5), CANVAS_HEIGHT - (player.icon.get_height() + 5)))
                self.window.blit(player_name, (CANVAS_WIDTH - 220, CANVAS_HEIGHT - 150))
                self.window.blit(player_money, (CANVAS_WIDTH - 220, CANVAS_HEIGHT - 130))
            elif player.ID == 2:
                if player.icon:
                    self.window.blit(player.icon, (5, CANVAS_HEIGHT - (player.icon.get_height() + 5)))
                self.window.blit(player_name, (12, CANVAS_HEIGHT - 150))
                self.window.blit(player_money, (12, CANVAS_HEIGHT - 130))
            elif player.ID == 3:
                if player.icon:
                    self.window.blit(player.icon, (5, 5))
                self.window.blit(player_name, (12, 100))
                self.window.blit(player_money, (12, 120))
            elif player.ID == 4:
                if player.icon:
                    self.window.blit(player.icon, (CANVAS_WIDTH - (player.icon.get_width() + 5), 5))
                self.window.blit(player_name, (CANVAS_WIDTH - 220, 100))
                self.window.blit(player_money, (CANVAS_WIDTH - 220, 120))

        call_button = pygame.image.load(base_path + "/images/buttons/CallButton.png")
        call_x = CANVAS_WIDTH / 2 - call_button.get_width() - 175
        call_y = CANVAS_HEIGHT - call_button.get_height() * 2 + 5
        self.window.blit(call_button, (call_x, call_y))

        fold_button = pygame.image.load(base_path + "/images/buttons/FoldButton.png")
        fold_x = CANVAS_WIDTH / 2 + call_button.get_width() + 30
        fold_y = CANVAS_HEIGHT - call_button.get_height()
        self.window.blit(fold_button, (fold_x, fold_y))

        raise_button = pygame.image.load(base_path + "/images/buttons/RaiseButton.png")
        raise_x = CANVAS_WIDTH / 2 - call_button.get_width() - 175
        raise_y = CANVAS_HEIGHT - call_button.get_height()
        self.window.blit(raise_button, (raise_x, raise_y))

        return {"call": [call_button, call_x, call_y], "fold": [fold_button, fold_x, fold_y],
                "raise": [raise_button, raise_x, raise_y], "pp": [profile_background, pp_x, pp_y],
                "b1p": [profile_background, b1p_x, b1p_y], "b2p": [profile_background, b2p_x, b2p_y], "b3p":
                    [profile_background, b3p_x, b3p_y]}

    def restart_game(self):
        self.deck.cards = Deck.generate_deck()
        self.deck.shuffle()
        self.get_community_cards()
        self.pot.reset()
        self.ending = False
        self.rounds = 1
        self.raises_in_a_row = 1
        for player in self.players:
            player.icon = None
            player.big_blind = False
            player.small_blind = False
            player.dealer = False
            player.in_pot = 0
            player.folded = False
            player.checked = False
            player.get_hand(self.deck.cards)
        for card in self.community_cards.cards:
            card.hidden = True

    def take_turns(self):
        for player in self.players:
            if self.ending:
                break
            if self.players[0].folded and self.players[1].folded and self.players[2].folded and self.players[3].folded:
                quit(0)
            if player.folded:
                continue
            if self.players[0].checked and self.players[1].checked and self.players[2].checked and self.players[3].checked:
                self.rounds += 1
                for p in self.players:
                    if not p.folded:
                        p.checked = False
            if self.rounds == 2:
                self.community_cards.show_community_cards(3)
            elif self.rounds == 3:
                self.community_cards.show_community_cards(4)
            elif self.rounds == 4:
                self.community_cards.show_community_cards(5)
                for i in range(1, len(Player.get_players())):
                    self.players[i].show_hands()
                self.ending = True
            self.window.fill(colors['green'])
            self.load_items(self.pygame)
            if not self.ending:
                if player.name == "You":
                    who_turn = self.fonts[1].render(f"It is: your turn", True, colors["black"])
                else:
                    who_turn = self.fonts[1].render(f"It is: {player.name}'s turn", True, colors["black"])
            else:
                who_turn = self.fonts[1].render(f"Who won?", True, colors["black"])
            last_move_r = self.fonts[1].render(self.last_move, True, colors["black"])
            self.window.blit(who_turn, (CANVAS_WIDTH / 2 - who_turn.get_width() / 2, CANVAS_HEIGHT / 2 - who_turn.get_height() + 160))
            self.window.blit(last_move_r, (CANVAS_WIDTH / 2 - last_move_r.get_width() / 2, CANVAS_HEIGHT / 2 - last_move_r.get_height() + 120))
            no_button_clicked = True
            while no_button_clicked:
                if player.bot and not self.ending:
                    self.pygame.display.update()
                    sleep(random.randint(5, 7))
                    bots_choice = random.randint(0, 100)
                    if 0 <= bots_choice < 80:
                        player.call(self.pot)
                        no_button_clicked = False
                        self.raises_in_a_row = 0
                        self.last_move = f"{player.name} checked."
                    elif player.bot and 80 <= bots_choice < 95:
                        self.raises_in_a_row += 1
                        player.raise_pot(self.pot, 50 * self.raises_in_a_row)
                        no_button_clicked = False
                        self.last_move = f"{player.name} increased the pot by $50."
                    elif 95 <= bots_choice <= 100:
                        player.fold()
                        no_button_clicked = False
                        self.raises_in_a_row = 0
                        self.last_move = f"{player.name} folded"

                for event in self.pygame.event.get():
                    if event.type == self.pygame.QUIT:
                        self.pygame.quit()
                        exit(0)
                    if event.type == self.pygame.MOUSEBUTTONDOWN and not player.bot and not self.ending:
                        mouse_presses = self.pygame.mouse.get_pressed(3)
                        if mouse_presses[0] and self.buttons["call"][1] < self.pygame.mouse.get_pos()[0] < self.buttons["call"][1] + \
                                self.buttons["call"][0].get_width() and self.buttons["call"][2] < self.pygame.mouse.get_pos()[1] < \
                                self.buttons["call"][2] + self.buttons["call"][0].get_height():
                            player.call(self.pot)
                            no_button_clicked = False
                            self.raises_in_a_row = 0
                            self.last_move = f"{player.name} checked."
                            player.checked = True
                        elif mouse_presses[0] and self.buttons["raise"][1] < self.pygame.mouse.get_pos()[0] < self.buttons["raise"][
                            1] + self.buttons["raise"][0].get_width() and self.buttons["raise"][2] < self.pygame.mouse.get_pos()[1] < \
                                self.buttons["raise"][2] + self.buttons["raise"][0].get_height():
                            self.raises_in_a_row += 1
                            player.raise_pot(self.pot, 50 * self.raises_in_a_row)
                            no_button_clicked = False
                            self.last_move = f"{player.name} increased the pot by $50."
                            player.checked = False
                        elif mouse_presses[0] and self.buttons["fold"][1] < self.pygame.mouse.get_pos()[0] < self.buttons["fold"][1] + \
                                self.buttons["fold"][0].get_width() and self.buttons["fold"][2] < self.pygame.mouse.get_pos()[1] < \
                                self.buttons["fold"][2] + self.buttons["fold"][0].get_height():
                            player.fold()
                            no_button_clicked = False
                            self.raises_in_a_row = 0
                            self.last_move = f"{player.name} folded"
                            player.checked = True
                    elif event.type == self.pygame.MOUSEBUTTONDOWN and self.ending:
                        mouse_presses = self.pygame.mouse.get_pressed(3)
                        if mouse_presses[0] and self.buttons["pp"][1] < self.pygame.mouse.get_pos()[0] < self.buttons["pp"][1] + \
                                self.buttons["pp"][0].get_width() and self.buttons["pp"][2] < self.pygame.mouse.get_pos()[1] < \
                                self.buttons["pp"][2] + self.buttons["pp"][0].get_height():
                            self.players[0].money += self.pot.value
                            no_button_clicked = False
                            self.sessions += 1
                            self.ending = True
                        elif mouse_presses[0] and self.buttons["b1p"][1] < self.pygame.mouse.get_pos()[0] < self.buttons["b1p"][1] + \
                                self.buttons["b1p"][0].get_width() and self.buttons["b1p"][2] < self.pygame.mouse.get_pos()[1] < \
                                self.buttons["b1p"][2] + self.buttons["b1p"][0].get_height():
                            self.players[1].money += self.pot.value
                            no_button_clicked = False
                            self.sessions += 1
                            self.ending = True
                        elif mouse_presses[0] and self.buttons["b2p"][1] < self.pygame.mouse.get_pos()[0] < self.buttons["b2p"][1] + \
                                self.buttons["b2p"][0].get_width() and self.buttons["b2p"][2] < self.pygame.mouse.get_pos()[1] < \
                                self.buttons["b2p"][2] + self.buttons["b2p"][0].get_height():
                            self.players[2].money += self.pot.value
                            no_button_clicked = False
                            self.sessions += 1
                            self.ending = True
                        elif mouse_presses[0] and self.buttons["b3p"][1] < self.pygame.mouse.get_pos()[0] < \
                                self.buttons["b3p"][1] + self.buttons["b3p"][0].get_width() and self.buttons["b3p"][2] \
                                < self.pygame.mouse.get_pos()[1] < self.buttons["b3p"][2] + self.buttons["b3p"][0].\
                                get_height():
                            self.players[3].money += self.pot.value
                            no_button_clicked = False
                            self.sessions += 1
                            self.ending = True
                self.pygame.display.update()
