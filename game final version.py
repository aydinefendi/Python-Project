#ID: 5670726

import pygame
import sys
import os
from typing import List


pygame.init()
pygame.font.init()

# Window settings
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Create window
pygame.display.set_caption("War of Colours") # Set window title

# Set up a font to display scores and messages
score_font = pygame.font.SysFont("arial", 32) 
message_font = pygame.font.SysFont("arial", 28) 
played_card_font = pygame.font.SysFont("arial", 20)

# Game status
scores = {"player": 0, "computer": 0}
message = "Click a card to start the game"
played_card_message = ""
discard_pile = []

class Card:
    """ A class to represent a single card in the game.

    Attributes:
        colour (str): The colour of the card.
        number (int): The number of the card.
        special (bool): whether the card is special type (e.g., wild, watcher, etc.).
        name (str): the name of the card if applicable.
    """
    def __init__(self, colour: str, number: int, special: bool = False, name: str = ""):
        self.colour = colour
        self.number = number
        self.special = special
        self.name = name #To identify special cards

    def __str__(self):
        # If its a special card it returns its name, otherwise show colour and number
        return f"{self.colour} {self.number}" if not self.special else self.name
    
def calculate_points(player_card: Card, computer_card: Card,
                       previous_player_card: Card = None,
                       previous_computer_card: Card = None,
                       winner: str = "") -> int:

    """
    Calculates total points for the round including any applicable bonus.

    Parameters:
        player_card (Card): The card played by the player.
        computer_card (Card): The card played by the computer.
        previous_player_card (Card): Previous card played by the player.
        previous_computer_card (Card): Previous card played by the computer.
        winner (str): Either "player" or "computer".

    Returns:
        int: Total points for the round.
    """

    total_points = player_card.number + computer_card.number

    # Check for player's bonus
    if winner == "player" and previous_player_card:
        if player_card.colour == previous_player_card.colour and player_card.number == previous_player_card.number:
            total_points += 2

    #check for computer's bonus
    if winner == "computer" and previous_computer_card:
        if computer_card.colour == previous_computer_card.colour and computer_card.number == previous_computer_card.number:
            total_points += 2

    return total_points

def resolve_round(player_card: Card, computer_card: Card,
          scores: dict, discard_pile: list[Card],
          previous_player_card: Card = None,
          previous_computer_card: Card = None) -> tuple[dict, list[Card]]:
    """
    Compares the player's and computer's cards and updates the scores and discard pile accordingly.

    Parameters:
        player_card (Card): The card chosen by the player.
        computer_card (Card): The card chosen by the computer.
        scores (dict): Current scores of both players.
        discard_pile (list): the pile where the card played will be added.

    Returns:
        tuple: Updated scores and discard pile.
    """

# Input validation
    if not player_card or not computer_card:
        return scores, discard_pile, "Invalid card(s) — round skipped."

    if "player" not in scores or "computer" not in scores:
        return scores, discard_pile, "Invalid score dictionary — keys missing."
    
    # Show the cards played
    played_info = f"Player played: {player_card} | Computer played: {computer_card}"

    # Comparing numbers if colours match
    if player_card.colour == computer_card.colour:
        if player_card.number > computer_card.number:
            winner = "player"
        elif player_card.number < computer_card.number:
            winner = "computer"
        else:
            winner = "tie"

        if winner != "tie":
            points = calculate_points(player_card, computer_card, previous_player_card, previous_computer_card, winner) 
            scores[winner] += points
            round_message = f"{winner.capitalize()} wins the round and gets {points} points!"
        else:
            round_message = "It's a tie! No points awarded."
    else:  # If colours don't match
        round_message = "Colours don't match! No points awarded."

    discard_pile.append(player_card)
    discard_pile.append(computer_card)

    return scores, discard_pile, round_message, played_info



def refill_hands(player_hand: List[Card], computer_hand: List[Card],
                 draw_stack: List[Card], discard_pile: List[Card]) -> tuple[List[Card], List[Card], List[Card], List[Card]]:
    """
    Refills both player and computer hands with up to 5 cards each, dealt alternately.
    player always draws first when hands are empty and draw stack has cards.

    Parameters:
        player_hand (list of Card): Current hand of the player.
        computer_hand (list of Card): Current hand of the computer.
        draw_stack (list if Card): Cards remaining in the draw stack.
        discard_pile (list of Card): The discard pile to add any card if there is odd number of cards that is less than 10 in the draw stack.
    Returns:
        tuple: Updated draw_stack, computer_hand, player_hand and discard_pile.
    """
    # Refill when both players are out of cards
    if not player_hand and not computer_hand and draw_stack:
        cards_to_deal = min(10, len(draw_stack)) # max 5 per hand

        # If odd number of cards, move 1 to the discard pile
        if cards_to_deal % 2 != 0:
            discard_pile.append(draw_stack.pop()) # Remove a card from the end 
            cards_to_deal -= 1

        for i in range(cards_to_deal):
            if i % 2 == 0:
                player_hand.append(draw_stack.pop(0))  # player gets card at even indices
            else:
                computer_hand.append(draw_stack.pop(0)) # computer gets card at odd indices

        print(f"Hands refilled, player drew{len(player_hand)} cards, computer drew {len(computer_hand)} cards.")

    return player_hand, computer_hand, draw_stack, discard_pile

# Function to display the scores
def display_scores(screen, scores):
    player_score = score_font.render(f"Player Score: {scores['player']}", True, (255, 255, 255)) # Creates a text a white text surface
    computer_score = score_font.render(f"Computer Score: {scores['computer']}", True, (255, 255, 255)) # Creates a text a white text surface
    screen.blit(player_score, (50, 20)) # Draws the text surface on the screen
    screen.blit(computer_score, (700, 20)) # Draws the text surface on the screen

# Function to display the result message
def display_message(screen, message):
    message_surface = message_font.render(message, True, (255, 255, 255)) # Creates a text a white text surface
    screen.blit(message_surface, (SCREEN_WIDTH // 2 - message_surface.get_width() // 2, 70)) # Draws the text surface on the screen

# Function to display the played card information
def display_played_cards(screen, played_card_message):
    played_surface = played_card_font.render(played_card_message, True, (255, 255, 255)) # Creates a text a white text surface
    screen.blit(played_surface, (SCREEN_WIDTH // 2 - played_surface.get_width() // 2, 110)) # Draws the text surface on the screen

# Main game loop
running = True
while running:
    screen.fill((0, 100, 0))
    display_scores(screen, scores) # Display the scores
    display_message(screen, message) # Display the messages
    display_played_cards(screen, played_card_message) # Display played cards

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Here the mouse and clicks logic will be
        



    pygame.display.flip() # Update the screen
    
# to Exit the game 
pygame.quit()
sys.exit()

#ID: 5670726