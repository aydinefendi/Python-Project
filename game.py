import pygame
import os
import random
import sys

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
CARD_WIDTH = 120
CARD_HEIGHT = 180
CARD_SPACING = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 168, 82)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Setting up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Card Game")

# Game variables
player_hand = []
computer_hand = []
draw_stack = []
discard_pile = []
player_score = 0
computer_score = 0

# Card class
class Card:
    def __init__(self, color, number, card_type="regular"):
        self.color = color
        self.number = number
        self.card_type = card_type  #regular, wild, watcher, colorstorm, ascendancy
        self.selected = False
        
        # Load the image
        if card_type == "wild":
            self.image = pygame.image.load(os.path.join("CARDS", "WILD.png"))
        elif card_type == "watcher":
            self.image = pygame.image.load(os.path.join("CARDS", "WATCHER.png"))
        elif card_type == "colorstorm":
            self.image = pygame.image.load(os.path.join("CARDS", "COLORSTORM.png"))
        elif card_type == "ascendancy":
            self.image = pygame.image.load(os.path.join("CARDS", "ASCENDANCY.png"))
        else:
            self.image = pygame.image.load(os.path.join("CARDS", f"{color[0]}{number}.png"))
        
        # Resize image
        self.image = pygame.transform.scale(self.image, (CARD_WIDTH, CARD_HEIGHT))
        self.back_image = pygame.image.load(os.path.join("CARDS", "BACK.png"))
        self.back_image = pygame.transform.scale(self.back_image, (CARD_WIDTH, CARD_HEIGHT))
        
        
        self.rect = self.image.get_rect()
    
    # draw() method to draw the card
    def draw(self, x, y, face_up=True):
        ''' Draws the card at the specified position '''
        self.rect.x = x
        self.rect.y = y
        
        #Draw highlight if card is selected
        if self.selected:
            pygame.draw.rect(screen, BLUE, (x - 5, y - 5, CARD_WIDTH + 10, CARD_HEIGHT + 10), 3)
        
        #Draw the card image
        if face_up:
            screen.blit(self.image, (x, y))
        else:
            screen.blit(self.back_image, (x, y))
    
    def __str__(self):
        if self.card_type == "regular":
            return f"{self.color} {self.number}"
        else:
            return self.card_type.capitalize()

# Initialize the deck
def initialize_deck():
    ''' Initializes the deck of cards '''
    deck = []
    colors = ["Red", "Blue", "Green", "Yellow"]
    
    # Add regular cards (1-10 in each color)
    for color in colors:
        for number in range(1, 11):
            deck.append(Card(color, number))
    
    # Add special cards
    deck.append(Card("", 0, "wild"))
    deck.append(Card("", 0, "watcher"))
    deck.append(Card("", 0, "colorstorm"))
    deck.append(Card("", 0, "ascendancy"))
    
    # Shuffle the deck
    random.shuffle(deck)
    
    return deck

# Deal cards
def deal_cards():
    ''' Deals the cards to the player and computer '''
    global player_hand, computer_hand, draw_stack, discard_pile
    
    draw_stack = initialize_deck()
    player_hand = [draw_stack.pop() for _ in range(5)]
    computer_hand = [draw_stack.pop() for _ in range(5)]
    discard_pile = []

# Draw player's hand
def draw_player_hand():
    ''' Draws the player's hand '''
    # Calculate the total width of all cards with spacing
    total_width = len(player_hand) * CARD_WIDTH + (len(player_hand) - 1) * CARD_SPACING
    
    # Calculate the starting x position to center the cards
    start_x = (SCREEN_WIDTH - total_width) // 2
    
    # Draw each card
    for i, card in enumerate(player_hand):
        x = start_x + i * (CARD_WIDTH + CARD_SPACING)
        y = SCREEN_HEIGHT - CARD_HEIGHT - 50
        card.draw(x, y, face_up=True)

# Draw the game board
def draw_game_board():
    ''' Draws the game board '''
    # Fill the background
    screen.fill(GREEN)
    
    # Draw player's hand
    draw_player_hand()
    
    # Draw help text
    font = pygame.font.SysFont(None, 36)
    instruction_text = font.render("Click on a card to select it", True, WHITE)
    screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, 50))
    
    # Draw scores
    score_text = font.render(f"Player: {player_score}  Computer: {computer_score}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 10))
    
    pygame.display.flip()

# Check for card selection
def handle_card_selection(pos):
    ''' Handles the card selection '''
    for card in player_hand:
        if card.rect.collidepoint(pos):
            # Deselect all cards
            for c in player_hand:
                c.selected = False
            # Select this card
            card.selected = True
            return card
    return None

# Main function
def main():
    ''' Main function to run the game '''
    global player_score, computer_score
    
    #Initialize the game
    deal_cards()
    selected_card = None
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            #andle mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected_card = handle_card_selection(event.pos)
        
        # Draw everything
        draw_game_board()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
