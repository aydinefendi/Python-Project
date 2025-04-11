#ID: 5670726
 
import pygame
import sys
import os
from card import Card
from game_logic import resolve_round, refill_hands
from scoring import calculate_points

# Initialize pygame
pygame.init()
pygame.font.init()

# Window settings
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Create window
pygame.display.set_caption("War of Colours") # Set window title

# Set up a font to display scores, messages and played info
score_font = pygame.font.SysFont("arial", 32) 
message_font = pygame.font.SysFont("arial", 28) 
played_card_font = pygame.font.SysFont("arial", 20)

# Game status
scores = {"player": 0, "computer": 0}
message = "Click a card to start the game"
played_card_message = ""
discard_pile = []

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

         # Example trigger - will be changed with real logic
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player_card = Card("Red", 7)
            computer_card = Card("Red", 3)
            scores, discard_pile, round_message, played_info = resolve_round(
                player_card, computer_card, scores, discard_pile)
            
            message = round_message
            played_card_message = played_info

    
    pygame.display.flip() # Update the screen
    
# to Exit the game 
pygame.quit()
sys.exit()

#ID: 5670726