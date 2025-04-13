import pygame
import os
import random
import sys
import time

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
PURPLE = (128, 0, 128)

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

# Game state
SELECTING_CARD = 0
WAITING_FOR_COMPUTER = 1
SHOWING_RESULT = 2
GAME_OVER = 3
game_state = SELECTING_CARD

# Played cards
player_played_card = None
computer_played_card = None

# Result message
result_message = ""

# Card class
class Card:
    def __init__(self, color, number, card_type="regular"):
        ''' Initializes the card with the given color, number, and card type '''
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

#ID: 5671165
def shuffle(array: list) -> list:
    """Shuffles the cards inside the deck in place using the Fisher-Yates algorithm.
    
    Args:
        array (list): The list of unshuffled deck of cards.
        
    Returns:
        list: The shuffled deck of cards as a list.
    """
    for i in range(len(array) - 1, 0, -1):
        j = random.randint(0, i)
        # Swap the card at index i with a random card at index j
        array[i], array[j] = array[j], array[i]
    return array
#ID: 5671165

# Initialize the deck
def initialize_deck():
    ''' Initializes the deck of cards '''
    deck = []
    colors = ["Red", "Blue", "Green", "Yellow"]
    
    # Add regular cards (1-10 in each color) in deck list
    for color in colors:
        for number in range(1, 11):
            deck.append(Card(color, number))
    
    # Add special cards
    deck.append(Card("", 0, "wild"))
    deck.append(Card("", 0, "watcher"))
    deck.append(Card("", 0, "colorstorm"))
    deck.append(Card("", 0, "ascendancy"))

    shuffle(deck)

    return deck

# Deal cards
def deal_cards():
    ''' Deals the cards to the player and computer '''
    global player_hand, computer_hand, draw_stack, discard_pile, player_score, computer_score
    
    # Reset scores when starting a new game
    player_score = 0
    computer_score = 0
    
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

# Draw played cards
def draw_played_cards():
    ''' Draws the played cards in the center of the screen '''
    if player_played_card:
        # Player's played card (left side)
        player_x = SCREEN_WIDTH // 2 - CARD_WIDTH - 30
        player_y = SCREEN_HEIGHT // 2 - CARD_HEIGHT // 2
        player_played_card.draw(player_x, player_y, face_up=True)
        
        # Display "Player's Card" text
        font = pygame.font.SysFont(None, 30)
        text = font.render("Player's Card", True, WHITE)
        screen.blit(text, (player_x + CARD_WIDTH // 2 - text.get_width() // 2, player_y - 30))
    
    if computer_played_card:
        # Computer's played card (right side)
        computer_x = SCREEN_WIDTH // 2 + 30
        computer_y = SCREEN_HEIGHT // 2 - CARD_HEIGHT // 2
        computer_played_card.draw(computer_x, computer_y, face_up=True)
        
        # Display "Computer's Card" text
        font = pygame.font.SysFont(None, 30)
        text = font.render("Computer's Card", True, WHITE)
        screen.blit(text, (computer_x + CARD_WIDTH // 2 - text.get_width() // 2, computer_y - 30))
    
    # Draw result message if in SHOWING_RESULT state
    if game_state == SHOWING_RESULT and result_message:
        font = pygame.font.SysFont(None, 36)
        text = font.render(result_message, True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))

# Computer plays a card
def computer_play_card():
    ''' Computer selects a card to play '''
    #computer just plays a random card
    if computer_hand:
        return computer_hand.pop(random.randint(0, len(computer_hand) - 1))
    return None

# Check if the game is over
def check_game_over():
    ''' Checks if the game is over '''
    
    if len(draw_stack) == 0 and (len(player_hand) == 0 or len(computer_hand) == 0):
        return True
    
    if len(player_hand) == 0 and len(computer_hand) == 0:
        return True
        
    if len(player_hand) < 4 or len(computer_hand) < 4:
        return True
        
    return False

# Draw the winner display
def draw_winner_display():
    ''' Display the winner of the game '''
    # Create a semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    # Draw game over message
    font_large = pygame.font.SysFont(None, 72)
    game_over_text = font_large.render("GAME OVER", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 4))
    
    # Draw final scores
    font = pygame.font.SysFont(None, 48)
    scores_text = font.render(f"Final Score - Player: {player_score}  Computer: {computer_score}", True, WHITE)
    screen.blit(scores_text, (SCREEN_WIDTH // 2 - scores_text.get_width() // 2, SCREEN_HEIGHT // 4 + 100))
    
    # Determine and display the winner
    winner_text = ""
    if player_score > computer_score:
        winner_text = "Player Wins!"
        text_color = BLUE
    elif computer_score > player_score:
        winner_text = "Computer Wins!"
        text_color = RED
    else:
        winner_text = "It's a Tie!"
        text_color = YELLOW
    
    winner_display = font_large.render(winner_text, True, text_color)
    screen.blit(winner_display, (SCREEN_WIDTH // 2 - winner_display.get_width() // 2, SCREEN_HEIGHT // 4 + 200))
    
    # Draw play again button
    button_width = 200
    button_height = 60
    button_x = SCREEN_WIDTH // 2 - button_width // 2
    button_y = SCREEN_HEIGHT // 4 + 300
    
    pygame.draw.rect(screen, GREEN, (button_x, button_y, button_width, button_height))
    
    button_text = font.render("Play Again", True, WHITE)
    screen.blit(button_text, (button_x + button_width // 2 - button_text.get_width() // 2, 
                           button_y + button_height // 2 - button_text.get_height() // 2))
    
    return pygame.Rect(button_x, button_y, button_width, button_height)

# Evaluate the round
def evaluate_round():
    ''' Evaluates the round and updates scores '''
    global player_score, computer_score, result_message, discard_pile, game_state
    
    if not player_played_card or not computer_played_card:
        return
    
    # Handle special cards first
    if player_played_card.card_type != "regular" or computer_played_card.card_type != "regular":
        # For now, just put them in discard pile
        discard_pile.extend([player_played_card, computer_played_card])
        result_message = "Special card played. No points awarded."
        return
    
    # Check if cards are the same color
    if player_played_card.color == computer_played_card.color:
        # Same color - higher number wins
        total_points = player_played_card.number + computer_played_card.number
        
        if player_played_card.number > computer_played_card.number:
            player_score += total_points
            result_message = f"Player wins {total_points} points!"
        elif computer_played_card.number > player_played_card.number:
            computer_score += total_points
            result_message = f"Computer wins {total_points} points!"
        else:
            # Tie means no points (shouldn't happen with unique cards)
            result_message = "Tie! No points awarded."
    else:
        # Different colors means no points
        result_message = "Different colors! No points awarded."
    
    # Move cards to discard pile
    discard_pile.extend([player_played_card, computer_played_card])
    
    # Draw new cards if there are cards in the draw stack
    if len(draw_stack) > 0 and len(player_hand) < 5:
        player_hand.append(draw_stack.pop())
    
    if len(draw_stack) > 0 and len(computer_hand) < 5:
        computer_hand.append(draw_stack.pop())
    
    # Check if the game is over
    if check_game_over():
        game_state = GAME_OVER

# Play button
def draw_play_button():
    ''' Draws the play button if a card is selected '''
    
    # Check if any card is selected
    any_selected = any(card.selected for card in player_hand)
    
    if any_selected and game_state == SELECTING_CARD:
        button_width = 200
        button_height = 50
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        button_y = SCREEN_HEIGHT // 2 + 100
        
        # Draw the button
        pygame.draw.rect(screen, RED, (button_x, button_y, button_width, button_height))
        
        # Draw text
        font = pygame.font.SysFont(None, 36)
        text = font.render("Play Card", True, WHITE)
        screen.blit(text, (button_x + button_width // 2 - text.get_width() // 2, 
                           button_y + button_height // 2 - text.get_height() // 2))
        
        return pygame.Rect(button_x, button_y, button_width, button_height)
    
    return None

# Process selected card
def play_selected_card():
    ''' Plays the selected card '''
    global player_hand, player_played_card, game_state
    
    for i, card in enumerate(player_hand):
        if card.selected:
            player_played_card = player_hand.pop(i)
            game_state = WAITING_FOR_COMPUTER
            return True
    
    return False

# Draw wait message
def draw_wait_message():
    ''' Draws a message indicating waiting for the computer '''
    if game_state == WAITING_FOR_COMPUTER:
        font = pygame.font.SysFont(None, 36)
        text = font.render("Computer is thinking...", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + 150))

# Draw the game board
def draw_game_board():
    ''' Draws the game board '''
    #Background
    screen.fill(GREEN)
    
    # Draw relevant elements based on game state
    if game_state != GAME_OVER:
        # Draw player's hand
        draw_player_hand()
        
        # Draw played cards
        draw_played_cards()
        
        # Draw button
        play_button = draw_play_button()
        
        # Draw wait message if needed
        draw_wait_message()
        
        # Draw game state specific instructions
        font = pygame.font.SysFont(None, 36)
        if game_state == SELECTING_CARD:
            instruction_text = font.render("Select a card and click 'Play Card'", True, WHITE)
        elif game_state == WAITING_FOR_COMPUTER:
            instruction_text = font.render("Waiting for computer to play...", True, WHITE)
        elif game_state == SHOWING_RESULT:
            instruction_text = font.render("Click anywhere to continue", True, WHITE)
        else:
            instruction_text = font.render("", True, WHITE)
        
        screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, 50))
        
        # Draw scores
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Player: {player_score}  Computer: {computer_score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 10))
        
        play_again_button = None
    else:
        # Game is over - show winner
        play_button = None
        play_again_button = draw_winner_display()
    
    pygame.display.flip()
    
    if game_state == GAME_OVER:
        return None, play_again_button
    else:
        return play_button, None

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
    global player_score, computer_score, game_state, player_played_card, computer_played_card, result_message
    
    # Initialize the game
    deal_cards()
    selected_card = None
    play_button_rect = None
    play_again_button_rect = None
    computer_play_time = 0
    running = True
    
    while running:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if game_state == SELECTING_CARD:
                # Handle mouse clicks for card selection and play button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if play button was clicked
                    if play_button_rect and play_button_rect.collidepoint(event.pos):
                        if play_selected_card():
                            # Set the time when computer will play
                            computer_play_time = current_time + 2000  # 2 seconds delay
                    else:
                        # Check for card selection
                        selected_card = handle_card_selection(event.pos)
            
            elif game_state == SHOWING_RESULT:
                # Progress to next round when user clicks
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game_state = SELECTING_CARD
                    player_played_card = None
                    computer_played_card = None
                    result_message = ""
            
            elif game_state == GAME_OVER:
                # Handle play again button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_again_button_rect and play_again_button_rect.collidepoint(event.pos):
                        # Reset the game
                        deal_cards()
                        selected_card = None
                        play_button_rect = None
                        play_again_button_rect = None
                        computer_play_time = 0
                        player_played_card = None
                        computer_played_card = None
                        result_message = ""
                        game_state = SELECTING_CARD
        
        # Handle computer's turn
        if game_state == WAITING_FOR_COMPUTER and current_time >= computer_play_time:
            computer_played_card = computer_play_card()
            evaluate_round()  
            if game_state != GAME_OVER:  
                game_state = SHOWING_RESULT
        
        # Draw everything
        play_button_rect, play_again_button_rect = draw_game_board()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()