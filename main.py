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

Sources:
- https://github.com/monicanagent/cypherpoker.js (card png files)
- http://www.pngall.com/playing-cards-png/download/38939 (icon)
- https://www.wikihow.com/Program-a-Game-in-Python-with-Pygame (Research)
- https://www.youtube.com/watch?v=FfWpgLFMI7w&ab_channel=freeCodeCamp.org (Research)
- https://www.geeksforgeeks.org/how-to-create-buttons-in-a-game-using-pygame/ (Research)
- https://piratesonline.fandom.com/wiki/Poker (Reference)
"""
# Imports
from Game import Player, Robot, Hand, Deck, Pot, CommunityCards
import pygame
import os
from random import randint
from time import sleep
from pygame.locals import *
# Initializations and global variables
pygame.init()
pygame.font.init()
font_pot = pygame.font.SysFont('Comic Sans MS', 30)
font_text = pygame.font.SysFont('Comic Sans MS', 20)
CANVAS_WIDTH = 1280
CANVAS_HEIGHT = 720
CARD_WIDTH = 112
CARD_HEIGHT = 156
resolution = (CANVAS_WIDTH, CANVAS_HEIGHT)
colors = {"white": (255, 255, 255), "black": (0, 0, 0), "red": (255, 0, 0), "green": (14, 160, 60)}
# File locating
base_path = os.path.dirname(__file__)
image_path = base_path + "/images/"
# Window setup
pygame.display.set_caption("Texas Hold 'Em")
icon = pygame.image.load(image_path + '/other/icon.png')
pygame.display.set_icon(icon)


def get_hand(deck):
    """
    This function gets a players hand from the deck.
    :param deck: (list of Card objects) the deck
    :return: hand (Hand object) The player's hand
    """
    # Pull cards from deck
    hand = Hand(tuple(deck[x] for x in range(2)))
    # Remove the pulled cards
    for x in range(1, -1, -1):
        deck.remove(deck[x])
    return hand


def get_community_cards(deck):
    """
    This function gets the community cards from the deck.
    :param deck: (list of Card objects) the deck
    :return: community_cards (CommunityCards object) the session's community cards
    """
    # Pull cards from deck
    community_cards = CommunityCards(tuple(deck[x] for x in range(5)))
    # Remove the pulled cards
    for x in range(4, -1, -1):
        deck.remove(deck[x])
    return community_cards


def configure_players(deck):
    """
    This function configures the players and bots.
    :param deck: (Deck object) the deck
    :return: (list of Player objects) The players
    """
    # List of possible bot names
    robot_names = ["Eric (BOT)", "Jordan (BOT)", "Sam (BOT)", "Craig (BOT)", "Ryan (BOT)",
                   "Adam (BOT)", "Nate (BOT)", "Conor (BOT)", "Nina (BOT)", "Hayley (BOT)", "Shelsea (BOT)",
                   "Ben (BOT)", "Josh (BOT)", "Jimmy (BOT)", "Sarah Pettitt (BOT)"]
    # List of the randomly picked bot names
    picked_names = ["Sarah Pettitt (BOT)"]
    # Pick names until every player has a name
    while len(picked_names) < 3:
        i = randint(0, len(robot_names)-1)
        if robot_names[i] not in picked_names:
            picked_names.append(robot_names[i])
    # Starting cash all players start with
    starting_cash = 5000.00
    # Creating the Player and Robot objects
    player = Player("You", starting_cash, get_hand(deck.deck))
    bot1 = Robot(picked_names[0], starting_cash, get_hand(deck.deck))
    bot2 = Robot(picked_names[1], starting_cash, get_hand(deck.deck))
    bot3 = Robot(picked_names[2], starting_cash, get_hand(deck.deck))
    return [player, bot1, bot2, bot3]


def scale_card(card):
    """
    This function scales cards down because the original images are a little bit too big.
    :param card: (Card object) the card
    :return: (pygame transform) the transform of the image
    """
    # If the card is meant to be hidden, scale the card back
    if card.hidden:
        return pygame.transform.smoothscale(pygame.image.load(image_path + "\\cards\\CB.png"), (112, 156))
    # If the card is NOT meant to be hidden, scale the card itself
    else:
        # If the value of the card is numeric, use the value to make the image path
        if card.rank.isnumeric():
            img_str = "\\cards\\" + card.rank + card.suit[0] + ".png"
        # If the value of the card is NOT numeric, use the value to make the image path
        else:
            img_str = "\\cards\\" + card.rank[0] + card.suit[0] + ".png"
        return pygame.transform.smoothscale(pygame.image.load(image_path + img_str), (112, 156))


def simplify_cords(x, y):
    """
    This function simplifies the coordinates of a card by translating the 0,0 position to the center of the image.
    :param x: (int) desired x position of the card
    :param y: (int) desired y position of the card
    :return: (tuple)
    """
    # Remove half of the width and height to get the center
    card_x = x - (CARD_WIDTH/2)
    card_y = y - (CARD_HEIGHT/2)
    return tuple((card_x, card_y))


def show_hands(players):
    """
    This function flips the hands of all of the bots.
    :param players: (list of Player objects)
    """
    for player in range(1, len(players)):
        for card in players[player].hand.cards:
            card.flip()


def show_community_cards(community, num):
    """
    This function flips a specific number of community cards.
    :param community: (CommunityCards object) the community cards
    :param num: (int) the number to flip
    """
    for i in range(num):
        community.cards[i].hidden = False


def set_role(players, sessions, pot):
    """
    This function sets the roles for the session.
    :param players: (list of Player objects) the players
    :param sessions: (int) the number of sessions that have been played
    :param pot: (Pot object) the pot
    """
    # Configure and load the icon images
    bb_icon = pygame.image.load(base_path + "/images/other/BBIcon.png")
    bb_icon = pygame.transform.smoothscale(bb_icon, (75, 75))
    sb_icon = pygame.image.load(base_path + "/images/other/SBIcon.png")
    sb_icon = pygame.transform.smoothscale(sb_icon, (75, 75))
    d_icon = pygame.image.load(base_path + "/images/other/DealerIcon.png")
    d_icon = pygame.transform.smoothscale(d_icon, (75, 75))
    # Set the dealer
    players[sessions % 4].set_dealer()
    players[sessions % 4].icon = d_icon
    # Set the small blind
    players[(sessions + 1) % 4].set_small_blind()
    players[(sessions + 1) % 4].icon = sb_icon
    players[(sessions + 1) % 4].money -= 500
    pot.add(500)
    # set the big Blind
    players[(sessions + 2) % 4].set_big_blind()
    players[(sessions + 2) % 4].icon = bb_icon
    players[(sessions + 2) % 4].money -= 1000
    pot.add(1000)


def load_items(window, players, community_cards, pot):
    """
    This function assigns and configures almost all images and text, and returns the buttons.
    :param window: (pygame window object) the window
    :param players: (list of Player objects) the players
    :param community_cards: (CommunityCards object) the community cards
    :param pot: (Pot object) the pot
    :return: (dict) a dictionary containing the image render, x position, and y position for every button
    """
    # Player cards
    pc1 = scale_card(players[0].hand.cards[0])
    pc2 = scale_card(players[0].hand.cards[1])
    if not players[0].folded:
        window.blit(pc1, simplify_cords((CANVAS_WIDTH / 2) - 70, CANVAS_HEIGHT - (CARD_HEIGHT / 2)))
        window.blit(pc2, simplify_cords((CANVAS_WIDTH / 2) + 70, CANVAS_HEIGHT - (CARD_HEIGHT / 2)))
    # Player Profile
    profile_background = pygame.image.load(base_path + "/images/other/Profile.png")
    pp_x = CANVAS_WIDTH - profile_background.get_width()
    pp_y = CANVAS_HEIGHT - profile_background.get_height()
    window.blit(profile_background, (pp_x, pp_y))

    # Bot 1 cards
    b1c1 = scale_card(players[1].hand.cards[0])
    b1c2 = scale_card(players[1].hand.cards[1])
    b1c1 = pygame.transform.rotate(b1c1, -90)
    b1c2 = pygame.transform.rotate(b1c2, -90)
    if not players[1].folded:
        window.blit(b1c1, simplify_cords(CARD_WIDTH / 2, (CANVAS_HEIGHT / 2) - 70))
        window.blit(b1c2, simplify_cords(CARD_WIDTH / 2, (CANVAS_HEIGHT / 2) + 70))
    # Bot 1 Profile
    b1p_x = 0
    b1p_y = CANVAS_HEIGHT - profile_background.get_height()
    window.blit(profile_background, (b1p_x, b1p_y))

    # Bot 2 cards
    b2c1 = scale_card(players[2].hand.cards[0])
    b2c2 = scale_card(players[2].hand.cards[1])
    b2c1 = pygame.transform.rotate(b2c1, 180)
    b2c2 = pygame.transform.rotate(b2c2, 180)
    if not players[2].folded:
        window.blit(b2c1, simplify_cords((CANVAS_WIDTH / 2) - 70, CARD_HEIGHT / 2))
        window.blit(b2c2, simplify_cords((CANVAS_WIDTH / 2) + 70, CARD_HEIGHT / 2))
    # Bot  2 Profile
    b2p_x = 0
    b2p_y = 0
    window.blit(profile_background, (b2p_x, b2p_y))

    # Bot 3 cards
    b3c1 = scale_card(players[3].hand.cards[0])
    b3c2 = scale_card(players[3].hand.cards[1])
    b3c1 = pygame.transform.rotate(b3c1, 90)
    b3c2 = pygame.transform.rotate(b3c2, 90)
    if not players[3].folded:
        window.blit(b3c1, simplify_cords((CARD_WIDTH / 2) + CANVAS_WIDTH - CARD_HEIGHT, (CANVAS_HEIGHT / 2) - 70))
        window.blit(b3c2, simplify_cords((CARD_WIDTH / 2) + CANVAS_WIDTH - CARD_HEIGHT, (CANVAS_HEIGHT / 2) + 70))
    # Bot 3 Profile
    b3p_x = CANVAS_WIDTH-profile_background.get_width()
    b3p_y = 0
    window.blit(profile_background, (b3p_x, b3p_y))

    # Community cards
    cc1 = scale_card(community_cards.cards[0])
    cc2 = scale_card(community_cards.cards[1])
    cc3 = scale_card(community_cards.cards[2])
    cc4 = scale_card(community_cards.cards[3])
    cc5 = scale_card(community_cards.cards[4])
    window.blit(cc1, simplify_cords((CANVAS_WIDTH / 2) - 250, CANVAS_HEIGHT / 2))
    window.blit(cc2, simplify_cords((CANVAS_WIDTH / 2) - 125, CANVAS_HEIGHT / 2))
    window.blit(cc3, simplify_cords((CANVAS_WIDTH / 2), CANVAS_HEIGHT / 2))
    window.blit(cc4, simplify_cords((CANVAS_WIDTH / 2) + 125, CANVAS_HEIGHT / 2))
    window.blit(cc5, simplify_cords((CANVAS_WIDTH / 2) + 250, CANVAS_HEIGHT / 2))

    # Pot
    pot_text = font_pot.render(f"{pot}", True, colors["black"])
    window.blit(pot_text, ((CANVAS_WIDTH / 2) - (pot_text.get_width() / 2), (CANVAS_HEIGHT / 2) - 160))

    # Go through every player and render the icon if they serve a role during the session
    for player in players:
        player_name = font_text.render(player.name, True, colors["black"])
        player_money = font_text.render(str(player.get_money()), True, colors["black"])
        # If player 1 has a role
        if player.ID == 1:
            if player.icon:
                window.blit(player.icon, (CANVAS_WIDTH-(player.icon.get_width()+5),
                                          CANVAS_HEIGHT-(player.icon.get_height()+5)))
            window.blit(player_name, (CANVAS_WIDTH-220, CANVAS_HEIGHT-150))
            window.blit(player_money, (CANVAS_WIDTH-220, CANVAS_HEIGHT-130))
        # If player 2 has a role
        elif player.ID == 2:
            if player.icon:
                window.blit(player.icon, (5, CANVAS_HEIGHT-(player.icon.get_height()+5)))
            window.blit(player_name, (12, CANVAS_HEIGHT-150))
            window.blit(player_money, (12, CANVAS_HEIGHT-130))
        # If player 3 has a role
        elif player.ID == 3:
            if player.icon:
                window.blit(player.icon, (5, 5))
            window.blit(player_name, (12, 100))
            window.blit(player_money, (12, 120))
        # If player 1 has a role
        elif player.ID == 4:
            if player.icon:
                window.blit(player.icon, (CANVAS_WIDTH-(player.icon.get_width() + 5), 5))
            window.blit(player_name, (CANVAS_WIDTH-220, 100))
            window.blit(player_money, (CANVAS_WIDTH-220, 120))
    # Configure the call button
    call_button = pygame.image.load(base_path + "/images/buttons/CallButton.png")
    call_x = CANVAS_WIDTH/2-call_button.get_width()-175
    call_y = CANVAS_HEIGHT-call_button.get_height()*2+5
    window.blit(call_button, (call_x, call_y))
    # Configure the fold button
    fold_button = pygame.image.load(base_path + "/images/buttons/FoldButton.png")
    fold_x = CANVAS_WIDTH/2+call_button.get_width()+30
    fold_y = CANVAS_HEIGHT-call_button.get_height()
    window.blit(fold_button, (fold_x, fold_y))
    # Configure the raise button
    raise_button = pygame.image.load(base_path + "/images/buttons/RaiseButton.png")
    raise_x = CANVAS_WIDTH/2-call_button.get_width()-175
    raise_y = CANVAS_HEIGHT-call_button.get_height()
    window.blit(raise_button, (raise_x, raise_y))

    return {"call": [call_button, call_x, call_y], "fold": [fold_button, fold_x, fold_y],
            "raise": [raise_button, raise_x, raise_y], "pp": [profile_background, pp_x, pp_y],
            "b1p": [profile_background, b1p_x, b1p_y], "b2p": [profile_background, b2p_x, b2p_y], "b3p":
                [profile_background, b3p_x, b3p_y]}


def main():
    """
    This is the main function that handles the game loop and game events.
    """
    session = 1
    # Set up the display window
    window = pygame.display.set_mode(resolution)
    # Replay loop
    while True:
        # Create the pot and deck
        pot = Pot(0)
        game_deck = Deck()
        # Shuffle the deck
        game_deck.shuffle()
        # A value to signify when a session is ending
        end = False
        # A value to represent what stage of the session the game is in
        rounds = 1
        # A value to keep track of consecutive raises and allowing for easier calculation
        raises_in_a_row = 0
        # This value will hold the last move made by a player or bot
        last_move = ""
        # If it is the first session the do the initial configurations for the players and community cards
        if session == 1:
            configure_players(game_deck)
            players = Player.get_players().copy()
            set_role(players, session, pot)
            community_cards = get_community_cards(game_deck.deck)
        # Otherwise, do a reset so we can hop right into another session
        else:
            # For every player reset their variables and reset the community cards
            for player in players:
                player.reset()
                player.hand = get_hand(game_deck.deck)
                community_cards = get_community_cards(game_deck.deck)
            for cards in community_cards.cards:
                cards.hidden = True
            set_role(players, session, pot)
        players[0].hand.cards[0].flip()
        players[0].hand.cards[1].flip()
        # The primary game loop
        while not end:
            # Update the window
            pygame.display.update()
            # This loop goes through every player's turn
            for player in players:
                # If the session has ended, break out of the game loop so the values can reset
                if end:
                    break
                # If every player folds, then quit the game
                if players[0].folded and players[1].folded and players[2].folded and players[3].folded:
                    pygame.quit()
                    exit(0)
                # If a player has folded, skip their turn
                if player.folded:
                    continue
                # If everyone has checked, then move on to the next round
                if players[0].checked and players[1].checked and players[2].checked and players[3].checked:
                    rounds += 1
                    # Unfold the the folded players for the next round
                    for p in players:
                        if not p.folded:
                            p.checked = False
                # If it is the second round, then show 3 community cards
                if rounds == 2:
                    show_community_cards(community_cards, 3)
                # If it is the second round, then show 4 community cards
                elif rounds == 3:
                    show_community_cards(community_cards, 4)
                # If it is the second round, then show all of the community cards
                elif rounds == 4:
                    show_community_cards(community_cards, 5)
                    show_hands(players)
                    end = True
                # Fill the background with the color green and put the other images and text on top
                window.fill(colors['green'])
                buttons = load_items(window, players, community_cards, pot)
                # If the session is not headed towards an ended state, then show who just played
                if not end:
                    if player.name == "You":
                        who_turn = font_pot.render(f"It is: your turn", True, colors["black"])
                    else:
                        who_turn = font_pot.render(f"It is: {player.name}'s turn", True, colors["black"])
                # Otherwise, ask who won
                else:
                    who_turn = font_pot.render(f"Who won?", True, colors["black"])
                # Display what the last move was and who's turn is it
                last_move_r = font_pot.render(last_move, True, colors["black"])
                window.blit(who_turn, (CANVAS_WIDTH / 2 - who_turn.get_width() / 2, CANVAS_HEIGHT / 2 - who_turn.
                                       get_height() + 160))
                window.blit(last_move_r, (CANVAS_WIDTH/2-last_move_r.get_width()/2, CANVAS_HEIGHT/2-last_move_r.
                                          get_height()+120))
                # A variable to test whether the player clicked a button
                no_button_clicked = True
                # While a button hasn't been clicked
                while no_button_clicked:
                    # If the player who's turn it is, is a bot
                    if player.bot and not end:
                        # Wait 2 - 3 seconds in between bot decisions to allow the user to read what they do
                        sleep(randint(2, 3))
                        # Select a random number between 0 and 100 to make decisions
                        bots_choice = randint(0, 100)
                        # If between 0 and 80, check/call
                        if 0 <= bots_choice < 80:
                            player.call(pot)
                            no_button_clicked = False
                            # Reset raises in a row
                            raises_in_a_row = 0
                            last_move = f"{player.name} checked."
                            # Identify that the player is ready for the next round
                            player.checked = True
                        # If between 80 and 95, raise
                        elif player.bot and 80 <= bots_choice < 95:
                            # Increment raises in a row
                            raises_in_a_row += 1
                            player.raise_pot(pot, 50 * raises_in_a_row)
                            no_button_clicked = False
                            last_move = f"{player.name} increased the pot by $50."
                            # Identify that the player is not ready for the next round
                            player.checked = False
                        # If between 95 and 100, fold
                        elif 95 <= bots_choice <= 100:
                            player.fold()
                            no_button_clicked = False
                            # Reset raises in a row
                            raises_in_a_row = 0
                            last_move = f"{player.name} folded"
                            # Identify that the player is ready for the next round
                            player.checked = True
                    # Loop to wait for mouse events
                    for event in pygame.event.get():
                        # If they click the quit button, then quit
                        if event.type == QUIT:
                            pygame.quit()
                            exit(0)
                        # If the player clicks on their turn
                        if event.type == pygame.MOUSEBUTTONDOWN and not player.bot and not end:
                            # Register the clicks in a mouse presses variable
                            mouse_presses = pygame.mouse.get_pressed(3)
                            # If the player clicks the call button
                            if mouse_presses[0] and buttons["call"][1] < pygame.mouse.get_pos()[0] < buttons["call"][1]\
                                    + buttons["call"][0].get_width() and buttons["call"][2] < pygame.mouse.get_pos()[1]\
                                    < buttons["call"][2] + buttons["call"][0].get_height():
                                player.call(pot)
                                no_button_clicked = False
                                # Reset raises in a row
                                raises_in_a_row = 0
                                last_move = f"{player.name} checked."
                            # If the player clicks the raise button
                            elif mouse_presses[0] and buttons["raise"][1] < pygame.mouse.get_pos()[0] < \
                                    buttons["raise"][1] + buttons["raise"][0].get_width() and buttons["raise"][2] < \
                                    pygame.mouse.get_pos()[1] < buttons["raise"][2] + buttons["raise"][0].get_height():
                                # Increment raises in a row
                                raises_in_a_row += 1
                                player.raise_pot(pot, 50 * raises_in_a_row)
                                no_button_clicked = False
                                last_move = f"{player.name} increased the pot by $50."
                            # If the player clicks the call button
                            elif mouse_presses[0] and buttons["fold"][1] < pygame.mouse.get_pos()[0] < \
                                    buttons["fold"][1] + buttons["fold"][0].get_width() and buttons["fold"][2] < \
                                    pygame.mouse.get_pos()[1] < buttons["fold"][2] + buttons["fold"][0].get_height():
                                player.fold()
                                no_button_clicked = False
                                # Reset raises in a row
                                raises_in_a_row = 0
                                last_move = f"{player.name} folded"
                        # If approaching the end of a session, click on the player profiles to choose the winner
                        elif event.type == pygame.MOUSEBUTTONDOWN and end:
                            # Register the clicks in a mouse presses variable
                            mouse_presses = pygame.mouse.get_pressed(3)
                            # If the player clicks the player 1 button
                            if mouse_presses[0] and buttons["pp"][1] < pygame.mouse.get_pos()[0] < buttons["pp"][1] + \
                                    buttons["pp"][0].get_width() and buttons["pp"][2] < pygame.mouse.get_pos()[1] < \
                                    buttons["pp"][2] + buttons["pp"][0].get_height():
                                # Give the player the value of the pot
                                players[0].money += pot.value
                                no_button_clicked = False
                                # Move on to the next session
                                session += 1
                            # If the player clicks the player 2 button
                            elif mouse_presses[0] and buttons["b1p"][1] < pygame.mouse.get_pos()[0] < buttons["b1p"][1]\
                                    + buttons["b1p"][0].get_width() and buttons["b1p"][2] < pygame.mouse.get_pos()[1] <\
                                    buttons["b1p"][2] + buttons["b1p"][0].get_height():
                                # Give the player the value of the pot
                                players[1].money += pot.value
                                no_button_clicked = False
                                # Move on to the next session
                                session += 1
                            # If the player clicks the player 3 button
                            elif mouse_presses[0] and buttons["b2p"][1] < pygame.mouse.get_pos()[0] < buttons["b2p"][1]\
                                    + buttons["b2p"][0].get_width() and buttons["b2p"][2] < pygame.mouse.get_pos()[1] <\
                                    buttons["b2p"][2] + buttons["b2p"][0].get_height():
                                # Give the player the value of the pot
                                players[2].money += pot.value
                                no_button_clicked = False
                                # Move on to the next session
                                session += 1
                            # If the player clicks the player 4 button
                            elif mouse_presses[0] and buttons["b3p"][1] < pygame.mouse.get_pos()[0] < buttons["b3p"][1]\
                                    + buttons["b3p"][0].get_width() and buttons["b3p"][2] < pygame.mouse.get_pos()[1] <\
                                    buttons["b3p"][2] + buttons["b3p"][0].get_height():
                                # Give the player the value of the pot
                                players[3].money += pot.value
                                no_button_clicked = False
                                # Move on to the next session
                                session += 1
                    # Update the display
                    pygame.display.update()


# Main
if __name__ == '__main__':
    main()
