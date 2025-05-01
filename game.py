import pygame
import os
import random
import sys
import time
from collections import defaultdict

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
pygame.display.set_caption("War of Colors")

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

#ID: 5670726
score_font = pygame.font.SysFont(None, 36)
message_font = pygame.font.SysFont(None, 36)
played_card_font = pygame.font.SysFont(None, 30)
message = ""
played_card_message = ""
#ID: 5670726

# Played cards
player_played_card = None
computer_played_card = None

#ID: 5670726
previous_player_card = None
previous_computer_card = None
result_message = ""
#ID: 5670726

# Card class
class Card:
    def __init__(self, color, number, card_type="regular"):
        ''' Initializes the card with the given color, number, and card type '''
        self.color = color
        self.number = number
        self.card_type = card_type  #regular, wild, watcher, colorstorm, ascendancy, add two points
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
        elif card_type == "twopoints":
            self.image = pygame.image.load(os.path.join("CARDS", "TWOPOINTS.png"))
        elif card_type == "twopoints2":
            self.image = pygame.image.load(os.path.join("CARDS", "TWOPOINTS2.png"))
        else:
            self.image = pygame.image.load(os.path.join("CARDS", f"{color[0]}{number}.png"))
        
        # Resize image
        self.image = pygame.transform.scale(self.image, (CARD_WIDTH, CARD_HEIGHT))
        self.back_image = pygame.image.load(os.path.join("CARDS", "BACK.png"))
        self.back_image = pygame.transform.scale(self.back_image, (CARD_WIDTH, CARD_HEIGHT))
        
        self.rect = self.image.get_rect()
    #ID: 5672969
    # draw() method to draw the card
    def draw(self, x, y, face_up=True):
        """Draws the card at the specified position.
        
        Args:
            x: The x-coordinate where the card should be drawn.
            y: The y-coordinate where the card should be drawn.
            face_up: Whether the card should be drawn face up or face down.
            
        Returns:
            None
        """
        self.rect.x = x
        self.rect.y = y
        
        #Draw highlight if card is selected
        if self.selected:
            pygame.draw.rect(screen, BLUE, (x - 5, y - 5, CARD_WIDTH + 10, CARD_HEIGHT + 10), 3)
        
        #Draw the card image
        if face_up:
            screen.blit(self.image, (x, y))
        else:
            pygame.draw.rect(screen, BLACK, (x - 2, y - 2, CARD_WIDTH + 4, CARD_HEIGHT + 4), border_radius=12)
            screen.blit(self.back_image, (x, y))
    
    def __str__(self):
        if self.card_type == "regular":
            return f"{self.color} {self.number}"
        else:
            return self.card_type.capitalize()
    #ID: 5672969

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
    deck.append(Card("", 0, "twopoints"))
    deck.append(Card("", 0, "twopoints"))
    
    shuffle(deck)

    return deck

#ID: 5671165

#Adds a card to the discard pile
def discard_card(card: Card) -> None:
    """Adds a Card instance to the discard pile.

    Args:
        card (Card): The card instance to be added to the discard pile.

    Returns:
        None
    """
    global discard_pile

    discard_pile.append(card)
#ID: 5671165

#ID: 5671165
#Give the player one card
def player_draw_card() -> None:
    """Draws one card from the draw stack and assigns it to the player.

    This function takes the top card from the draw stack and appends it to
    the player's hand.

    Returns:
        None
    """
    player_hand.append(draw_stack.pop())
#ID: 5671165

#ID: 5671165
#Give the computer one card
def computer_draw_card() -> None:
    """Draws one card from the draw stack and assigns it to the computer.

    This function takes the top card from the draw stack and appends it to
    the computer's hand.

    Returns:
        None
    """
    computer_hand.append(draw_stack.pop())
#ID: 5671165

#ID: 5672969
# Deal cards
def deal_cards():
    """Deals the cards to the player and computer.
    
    This function initializes the game by dealing cards to both the player
    and computer, resetting scores, and preparing the draw stack and discard pile.
    
    Returns:
        None
    """
    global player_hand, computer_hand, draw_stack, player_score, computer_score, discard_pile
    
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
#ID: 5672969

#ID: 5672969
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
#ID: 5672969

#ID: 5672969
# Computer plays a card
def computer_play_card():
    """Computer selects a card to play.
    
    This function randomly selects a card from the computer's hand to play.
    
    Returns:
        Card or None: The selected card if the computer has cards, None otherwise.
    """
    #computer just plays a random card
    if computer_hand:
        return computer_hand.pop(random.randint(0, len(computer_hand) - 1))
    return None
#ID: 5672969

#ID: 5672969
# Check if the game is over
def check_game_over():
    """Checks if the game is over.
    
    The game is considered over only when:
    - The draw stack is empty AND
    - Both players have no cards left to play
    
    Returns:
        bool: True if the game is over, False otherwise.
    """
    if len(draw_stack) == 0 and len(player_hand) == 0 and len(computer_hand) == 0:
        return True
        
    return False
#ID: 5672969

#ID: 5672969
# Draw the winner display
def draw_winner_display():
    """Displays the winner of the game.
    
    This function creates a game over screen showing the final scores,
    the winner, and a play again button.
    
    Returns:
        The rectangle representing the play again button.
    """
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
#ID: 5672969

#ID: 5670726
# Calculates points
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
        if player_card.number == previous_player_card.number:
            total_points += 2

    #check for computer's bonus
    if winner == "computer" and previous_computer_card:
        if computer_card.number == previous_computer_card.number:
            total_points += 2

    return total_points
#ID: 5670726

#ID: 5670726
# Evaluate the round
def resolve_round():
    """
    Handles a single round of the game:
      Compares player and computer cards.
      Applies scoring and bonus logic.
      Updates the discard pile, game state, and tracks previously played cards.

    Returns:
        tuple:
             discard_pile (list[Card]): The updated discard pile.
             result_message (str): A message summarizing the round result.
             played_info (str): Detailed info about which cards were played.
    """
    global player_played_card, computer_played_card
    global player_score, computer_score, discard_pile, draw_stack
    global player_hand, computer_hand, game_state, result_message
    global previous_player_card, previous_computer_card
    
    if not player_played_card or not computer_played_card:
        return discard_pile, result_message, "No cards played."
    
    # Show the cards played
    played_info = f"Player played: {player_played_card} | Computer played: {computer_played_card}"

    # Handling colorstorm card and/or two points card combinations or with regular cards
    colorstorm_played = player_played_card.card_type == "colorstorm" or computer_played_card.card_type == "colorstorm"
    twopoints_player = player_played_card.card_type == "twopoints"
    twopoints_computer = computer_played_card.card_type == "twopoints"

    if colorstorm_played or twopoints_player or twopoints_computer:
        discard_card(player_played_card)
        discard_card(computer_played_card)

        # Applying two points card
        if twopoints_player:
            player_score += 2
        if twopoints_computer:
            computer_score += 2

        # Handling colorstorm
        if colorstorm_played and len(draw_stack) >= 3:
            # Group cards by color
            grouped = defaultdict(list)
            for card in draw_stack:
                grouped[card.color].append(card) 

            # Sort each color group numbers in ascending order
            for colour_group in grouped.values():
                colour_group.sort(key=lambda c: c.number)

            # shuffle color groups randomly
            color_order = list(grouped.keys())
            shuffle(color_order)

            # Rebuild the draw stack
            draw_stack = []
            for color in color_order:
                draw_stack.extend(grouped[color])

        if draw_stack and len(player_hand) < 5:
            player_draw_card()
        if draw_stack and len(computer_hand) < 5:
            computer_draw_card()

        # Result messages
        if twopoints_player and twopoints_computer:
            result_message =  "Both players used Two points card! Each gets 2 points."
        elif twopoints_player and colorstorm_played:
            result_message = "Player used Two points card and Colorstorm played! draw stack is reordered"
        elif twopoints_computer and colorstorm_played:
            result_message = "Computer used Two points card and Colorstorm played! draw stack is reordered"
        elif twopoints_player:
            result_message = "Player used two points card and gets 2 points."
        elif twopoints_computer:
            result_message = "computer used two points card and gets 2 points."
        elif colorstorm_played and len(draw_stack) < 3:
            result_message = "Colorstorm played! There is no enough cards in the draw stack to reorder"
        elif colorstorm_played:
            result_message = "Colorstorm played! Draw stack reordered by color. No points awarded this round"

        return discard_pile, result_message, played_info

    # Comparing numbers if colors match
    if player_played_card.color == computer_played_card.color:
        if player_played_card.number > computer_played_card.number:
            winner = "player"
        elif player_played_card.number < computer_played_card.number:
            winner = "computer"
        else:
            winner = "tie"

        if winner != "tie":
            points = calculate_points(player_played_card, computer_played_card, 
                                      previous_player_card, previous_computer_card, winner=winner)
            if winner == "player":
                player_score += points
            else:
                computer_score += points
            round_message = f"{winner.capitalize()} wins the round and gets {points} points!"
        else:
            round_message = "It's a tie! No points awarded."
    else:
        round_message = "Colours don't match! No points awarded."

    result_message = round_message

    # Move played cards to discard pile
    discard_card(player_played_card)
    discard_card(computer_played_card)

    # Draw new cards 
    if draw_stack and len(player_hand) < 5:
        player_draw_card()
    if draw_stack and len(computer_hand) < 5:
        computer_draw_card()

    
    if len(draw_stack) == 0 and len(player_hand) == 0 and len(computer_hand) == 0:
        game_state = GAME_OVER

    previous_player_card = player_played_card
    previous_computer_card = computer_played_card

    return discard_pile, result_message, played_info
#ID: 5670726

#ID: 5672969
# Play button
def draw_play_button():
    """Draws the play button if a card is selected.
    
    This function draws a play button on the screen when a card is selected
    and the game is in the SELECTING_CARD state.
    
    Returns:
        pygame.Rect or None: The rectangle representing the play button if drawn,
                            None if no button is drawn.
    """
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
#ID: 5672969

#ID: 5672969
# Process selected card
def play_selected_card():
    """Plays the selected card.
    
    This function removes the selected card from the player's hand and
    sets it as the player's played card for the current round.
    
    Returns:
        bool: True if a card was played, False otherwise.
    """
    global player_hand, player_played_card, game_state
    
    for i, card in enumerate(player_hand):
        if card.selected:
            player_played_card = player_hand.pop(i)
            game_state = WAITING_FOR_COMPUTER
            card.selected = False
            return True
    
    return False
#ID: 5672969

#ID: 5672969
# Draw wait message
def draw_wait_message():
    """Draws a message indicating waiting for the computer.
    
    This function displays a "Computer is thinking..." message when
    the game is in the WAITING_FOR_COMPUTER state.
    
    Returns:
        None
    """
    if game_state == WAITING_FOR_COMPUTER:
        font = pygame.font.SysFont(None, 36)
        text = font.render("Computer is thinking...", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
#ID: 5672969
 
#ID: 5670726
# Draw the score and round messages
def draw_scores_and_messages():
    p_score = score_font.render(f"Player: {player_score}", True, WHITE)
    c_score = score_font.render(f"Computer: {computer_score}", True, WHITE)
    msg = message_font.render(message, True, WHITE)
    played = played_card_font.render(played_card_message, True, WHITE)

    screen.blit(p_score, (50, 20))
    screen.blit(c_score, (SCREEN_WIDTH - 250, 20))
    screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 70))
    screen.blit(played, (SCREEN_WIDTH // 2 - played.get_width() // 2, 10))
#ID: 5670726

# Draw the draw_stack
def draw_draw_stack() -> None:
    """Draws the draw stack on the screen with small positional adjustment between each card.
    
    This function adds the label "Draw stack" and draws each card in the draw stack
    with small positional adjustment to simulate the stack shape.
    All cards are drawn face down.
    
    Returns:
        None
    """
    base_x = 15
    base_y = (SCREEN_HEIGHT // 2) - (CARD_HEIGHT // 2)
    # Adjustment to show the stack effect
    adjustment = 2.3
    
    #Draw the 'Draw stack' text
    font = pygame.font.SysFont(None, 36)
    draw_stack_text = font.render("Draw stack", True, WHITE)
    text_x = base_x + 10
    text_y = base_y - CARD_HEIGHT // 2 - 40
    screen.blit(draw_stack_text, (text_x, text_y))

    #Draw each card in the draw stack faced down
    for i, card in enumerate(draw_stack):
        x = base_x + (i * adjustment)
        y = base_y - (i * adjustment)
        card.draw(x, y, face_up=False)
#ID: 5671165

#ID: 5671165
# Draw discard pile
def draw_discard_pile() -> None:
    """Draws the discard pile on the screen with small positional adjustment between each card.
    
    This function adds the label "Discard pile" and draws each card in the discard pile
    with small positional adjustment to simulate the pile shape.
    All cards are drawn face down.
    
    Returns:
        None
    """
    base_x = SCREEN_WIDTH - CARD_WIDTH - 100
    base_y = (SCREEN_HEIGHT // 2) - (CARD_HEIGHT // 2)
    # Adjustment to show the pile effect
    adjustment = 2.3

    #Draw the 'Discard pile' text
    font = pygame.font.SysFont(None, 36)
    draw_stack_text = font.render("Discard pile", True, WHITE)
    text_x = base_x + 10
    text_y = base_y - CARD_HEIGHT // 2 - 40
    screen.blit(draw_stack_text, (text_x, text_y))

    #Draw each card in the discard pile faced down
    for i, card in enumerate(discard_pile):
        x = base_x + (i * adjustment)
        y = base_y - (i * adjustment)
        card.draw(x, y, face_up=False)
#ID: 5671165

#ID: 5672969
# Draw the game board
def draw_game_board():
    """Draws the game board.
    
    This function draws all the game elements including the player's hand,
    played cards, discard pile, draw stack, play button, wait message,
    and scores based on the current game state.
    
    Returns:
        tuple: A tuple containing (play_button_rect, play_again_button_rect)
               where each element is a pygame.Rect or None.
    """
    #Background
    screen.fill(GREEN)
    
    # Draw relevant elements based on game state
    if game_state != GAME_OVER:
        # Draw player's hand
        draw_player_hand()
        
        # Draw played cards
        draw_played_cards()

        #Draw discard pile
        draw_discard_pile()

        #Draw draw_stack
        draw_draw_stack()
        
        # Draw button
        play_button = draw_play_button()
        
        # Draw wait message if needed
        draw_wait_message()

        # Draw scores and round messages
        draw_scores_and_messages()
        
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
#ID: 5672969

#ID: 5672969
# Check for card selection
def handle_card_selection(pos):
    """Handles the card selection.
    
    This function processes mouse clicks to select a card from the player's hand.
    When a card is selected, all other cards are deselected.
    
    Args:
        pos (tuple): The (x, y) coordinates of the mouse click.
        
    Returns:
        Card or None: The selected card if a valid selection was made,
                     None if no card was selected.
    """
    for card in player_hand:
        if card.rect.collidepoint(pos):
            # Deselect all cards
            for c in player_hand:
                c.selected = False
            # Select this card
            card.selected = True
            return card
    return None
#ID: 5672969

#ID: 5672969
# Main function
def main():
    """Main function to run the game.
    
    This function initializes and runs the main game loop, handling:
    - Card selection and playing
    - Computer turns
    - Game state transitions
    - User input
    - Game over conditions
    
    Returns:
        None
    """
    global player_score, computer_score, game_state, player_played_card, computer_played_card, result_message
    global previous_player_card, previous_computer_card, played_card_message

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
                            computer_play_time = current_time + 500
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
            discard_pile, result_message, played_info = resolve_round()  
            played_card_message = played_info  
            if game_state != GAME_OVER:  
                game_state = SHOWING_RESULT
        
        # Draw everything
        play_button_rect, play_again_button_rect = draw_game_board()
    
    pygame.quit()
    sys.exit()
#ID: 5672969
if __name__ == "__main__":
    main()