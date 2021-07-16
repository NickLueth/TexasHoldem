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

from Game import Player, Robot, Deck, Pot, Game
import pygame
import os
from random import randint

# Face up cards are 744 by 1052 pixels
# Face down card is 500 by 700 pixels
# Face up = 372, 526
# Face Down = 115, 161

pygame.init()
pygame.font.init()
font_pot = pygame.font.SysFont('Comic Sans MS', 30)
font_text = pygame.font.SysFont('Comic Sans MS', 20)
fonts = [font_text, font_pot]
CANVAS_WIDTH = 1280
CANVAS_HEIGHT = 720
CARD_WIDTH = 112
CARD_HEIGHT = 156
resolution = (CANVAS_WIDTH, CANVAS_HEIGHT)
colors = {"white": (255, 255, 255), "black": (0, 0, 0), "red": (255, 0, 0), "green": (14, 160, 60)}

base_path = os.path.dirname(__file__)
image_path = base_path + "/images/"
pygame.display.set_caption("Texas Hold 'Em")
icon = pygame.image.load(image_path + '/other/icon.png')
pygame.display.set_icon(icon)


def set_roles(players, rounds, pot):
    bb_icon = pygame.image.load(base_path + "/images/other/BBIcon.png")
    bb_icon = pygame.transform.smoothscale(bb_icon, (75, 75))
    sb_icon = pygame.image.load(base_path + "/images/other/SBIcon.png")
    sb_icon = pygame.transform.smoothscale(sb_icon, (75, 75))
    d_icon = pygame.image.load(base_path + "/images/other/DealerIcon.png")
    d_icon = pygame.transform.smoothscale(d_icon, (75, 75))

    # Dealer
    players[rounds % 4].set_dealer()
    players[rounds % 4].icon = d_icon
    # Small blind
    players[(rounds + 1) % 4].set_small_blind()
    players[(rounds + 1) % 4].icon = sb_icon
    players[(rounds + 1) % 4].money -= 50
    pot.add(50)
    # Big Blind
    players[(rounds + 2) % 4].set_big_blind()
    players[(rounds + 2) % 4].icon = bb_icon
    players[(rounds + 2) % 4].money -= 100
    pot.add(100)


def configure_players(game):
    robot_names = ["Eric (BOT)", "Jordan (BOT)", "Sam (BOT)", "Craig (BOT)", "Ryan (BOT)",
                   "Adam (BOT)", "Nate (BOT)", "Conor (BOT)", "Nina (BOT)", "Hayley (BOT)", "Shelsea (BOT)",
                   "Ben (BOT)", "Josh (BOT)", "Jimmy (BOT)"]
    picked_names = []
    while len(picked_names) < 3:
        i = randint(0, len(robot_names) - 1)
        if robot_names[i] not in picked_names:
            picked_names.append(robot_names[i])
    starting_cash = 5000.00
    player = Player("You", starting_cash, [])
    bot1 = Robot(picked_names[0], starting_cash, [])
    bot2 = Robot(picked_names[1], starting_cash, [])
    bot3 = Robot(picked_names[2], starting_cash, [])
    player.get_hand(game.deck.cards)
    bot1.get_hand(game.deck.cards)
    bot2.get_hand(game.deck.cards)
    bot3.get_hand(game.deck.cards)
    return [player, bot1, bot2, bot3]


def main():
    """
    This is the main function that handles the game loop.
    """
    deck = Deck()
    game = Game(pygame.display.set_mode(resolution), deck, Pot(0), pygame, fonts)
    while True:
        if game.ending:
            game.restart_game()
            set_roles(game.players, game.sessions, game.pot)
        if game.sessions == 1:
            set_roles(game.players, game.sessions, game.pot)
            for card in game.players[0].hand.cards:
                card.flip()
            while not game.ending:
                pygame.display.update()
                game.take_turns()
        else:
            for card in game.players[0].hand.cards:
                card.flip()
            while not game.ending:
                pygame.display.update()
                game.take_turns()


if __name__ == '__main__':
    main()
