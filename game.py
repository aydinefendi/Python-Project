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
WILD_CARD = 4
LAST_ROUND = 5
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

#ID: 5671165
# Wild card global variables
top_four_cards = []
player_used_wild = False
last_player_wild_choice = None
#ID: 5671165

#ID: 5671165
# Watcher card global variables
player_card_history = None
computer_card_history = None
leftover_points = 0
watcher_message = ""
#ID: 5671165

# Card class
#ID: 5672969, 5671165
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
        elif card_type == "joker":
            self.image = pygame.image.load(os.path.join("CARDS", "JOKER.png"))
        elif card_type == "swap":
            self.image = pygame.image.load(os.path.join("CARDS", "SWAP.png"))
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
    #Comparison methods needed for MaxHeap
    def __lt__(self, other: object) -> bool:
        """Less than method to compare cards according to their number.

        Args:
            other (object): Another card to compare with.

        Returns:
            bool: True if self is less than other, otherwise False.
        """
        if not isinstance(other, Card):
            return NotImplemented

        if self.number < other.number:
            return True
        else:
            return False

    def __gt__(self, other: object) -> bool:
        """Greater than method to compare cards according to their number.

        Args:
            other (object): Another card to compare with.

        Returns:
            bool: True if self is greater than other, otherwise False.
        """
        if not isinstance(other, Card):
            return NotImplemented

        if self.number > other.number:
            return True
        else:
            return False

    def __eq__(self, other: object) -> bool:
        """Equality method to compare cards according to their color, number and card type.

        Args:
            other (object): Another card to compare with.

        Returns:
            bool: True if all attributes are equal, otherwise False.
        """
        if not isinstance(other, Card):
            return False

        if (self.color == other.color and 
            self.number == other.number and 
            self.card_type == other.card_type):
            return True
        else:
            return False
        
    def __ne__(self, other: object) -> bool:
        """Inequality method to compare cards according to their color, number and card type.

        Args:
            other (object): Another card to compare with.

        Returns:
            bool: True if any attribute doesn't match, otherwise False.
        """
        if self.__eq__(other):
            return False
        else:
            return True
    #ID: 5671165
#ID: 5672969, 5671165

#ID: 5671165
#MaxHeap Class
class MaxHeap:
    """A max-heap data structure implementation for storing 
    cards objects used for implementing Wild card.

    This class adds elements to the MaxHeap list,
    retrieves the largest element, and finds the top four largest values.
    It uses a binary heap data structure that is stored in a list 
    and starts at index 1.

    Attributes:
        heap_list (List[Card]): The initial list that represents the heap.
        count (int): Number of elements in the heap (excluding 0 index).
    """

    def __init__(self) -> None:
        """Initializes an empty max heap attributes with a
        counter that starts at index 0.
        """
        self.heap_list: list = [None]
        self.count: int = 0

    def parent_idx(self, idx: int) -> int:
        """Returns the index of the parent node.

        Args:
            idx (int): Index of the child node.

        Returns:
            int: Index of the parent node.
        """
        return idx // 2

    def left_child_idx(self, idx: int) -> int:
        """Returns the index of the left child node.

        Args:
            idx (int): Index of the parent node.

        Returns:
            int: Index of the left child node.
        """
        return idx * 2

    def right_child_idx(self, idx: int) -> int:
        """Returns the index of the right child node.

        Args:
            idx (int): Index of the parent node.

        Returns:
            int: Index of the right child node.
        """
        return idx * 2 + 1
    
    def child_present(self, idx: int) -> bool:
        """Check if the given node index has at least one 
        child (specifically, the left child's presence).

        Args:
            idx (int): Index of the parent node.

        Returns:
            bool: Returns True if the left child exists, otherwise False.
        """
        return self.left_child_idx(idx) <= self.count

    def add(self, element: object) -> None:
        """Adds a new element to the heap list and restores the heap property.

        Args:
            element (object): The element to be added to the heap list.

        Returns:
            None
        """
        self.count += 1
        self.heap_list.append(element)
        self.heapify_up()
    
    def heapify_up(self) -> None:
        """Restores the max-heap property by moving the last 
        element up to its correct position.
        """
        idx = self.count
        while self.parent_idx(idx) > 0:
            parent_idx = self.parent_idx(idx)
            if self.heap_list[parent_idx] < self.heap_list[idx]:
                self.heap_list[parent_idx], self.heap_list[idx] = self.heap_list[idx], self.heap_list[parent_idx]
                idx = parent_idx
            else:
                break
    
    def retrieve_max(self) -> object:
        """Removes the heap elements to restore the max-heap property 
        and returns the maximum element from the heap.

        Returns:
            object: The maximum element, or None if the heap is empty.
        """
        if self.count == 0:
            return None
        max_value = self.heap_list[1]
        self.heap_list[1] = self.heap_list[self.count]
        self.count -= 1
        self.heap_list.pop()
        self.heapify_down()
        return max_value

    def heapify_down(self) -> None:
        """Moves the top element to its correct position to maintain heap property.
        """
        idx = 1
        while self.child_present(idx):
            larger_child_idx = self.get_larger_child_idx(idx)
            if self.heap_list[idx] < self.heap_list[larger_child_idx]:
                self.heap_list[idx], self.heap_list[larger_child_idx] = self.heap_list[larger_child_idx], self.heap_list[idx]
                idx = larger_child_idx
            else:
                break

    def get_larger_child_idx(self, idx: int) -> int:
        """Returns the index of the larger child node.

        Args:
            idx (int): Index of the parent node.

        Returns:
            int: Index of the child with the larger value.
        """
        if self.right_child_idx(idx) > self.count:
            return self.left_child_idx(idx)
        else:
            left_child = self.heap_list[self.left_child_idx(idx)]
            right_child = self.heap_list[self.right_child_idx(idx)]

        if left_child > right_child:
            return self.left_child_idx(idx)
        else:
            return self.right_child_idx(idx)

    def get_largest_four(self) -> list:
        """Returns the top four largest elements in the heap without modifying the original heap.

        Returns:
            list: A list of up to four largest elements in descending order.
        """
        if self.count == 0:
            return []

        temp_heap = MaxHeap()
        temp_heap.heap_list = self.heap_list[:]
        temp_heap.count = self.count

        largest = []
        for _ in range(min(4, self.count)):
            largest.append(temp_heap.retrieve_max())
        return largest
#ID: 5671165

#ID: 5671165
class Queue:
    """Fixed size queue implementation using lists.
        
    This queue includes a method of adding and removing items from the object 
    list of data at the same time according to queue properties and queue size. 
    The class also includes methods for indexing, clearing queue data and 
    extracting queue length.
    
    Attributes:
        size (int): The maximum number of elements in the queue.
        data (List[Card]): List to store queue data in.
    """
    def __init__(self, size: int) -> None:
        """Initialise queue attributes with a fixed size.

        Args:
            size (int): The Card objects the queue countains.
        """
        self.size: int = size
        self.data: list = []

    def enqueue(self, card) -> None:
        """Add a Card object to the front of the queue.

        If the queue is full of cards, the first object intered the queue
        is removed before inserting the new one.

        Args:
            card: The Card object needs to be added in the queue.
        """
        if len(self.data) >= self.size:
            self.data.pop()
        self.data.insert(0, card)

    def clear(self) -> None:
        """Remove all Card objects from the queue.
        """
        self.data = []

    def __getitem__(self, index: int):
        """Method that gits Card object index from the queue.

        Args:
            index (int): The index of the Card object needs to be found.

        Returns:
            The Card object at that index.
        """
        return self.data[index]

    def __len__(self) -> int:
        """Method to get the length of a queue.

        Returns:
            The length of the queue.
        """
        return len(self.data)
#ID: 5671165

#ID: 5671165
#Shuffling algorithm
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

#ID: 5671165
#Check if a list or cards objects has a regular cards
def has_regular(cards: list[Card]) -> bool:
    """Checks whether the given list of cards contains any regular cards.

    A regular card is categorised by the attribute `card_type` equal to "regular".
    This is used for the Wild card implementation.

    Args:
        cards (list[Card]): A list of Card objects to be checked.

    Returns:
        bool: True if at least one card is regular, otherwise False.
    """
    for card in cards:
        if card.card_type == "regular":
            return True
    return False
#ID: 5671165

#ID: 5672969
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
    deck.append(Card("", 0, "joker"))
    deck.append(Card("", 0, "swap"))
    
    shuffle(deck)

    return deck
#ID: 5672969

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
    if draw_stack:
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
    if draw_stack:
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
    global player_hand, computer_hand, draw_stack, player_score, computer_score, discard_pile, top_four_cards
    
    # Reset scores when starting a new game
    player_score = 0
    computer_score = 0
    
    draw_stack = initialize_deck()
    player_hand = [draw_stack.pop() for _ in range(5)]
    computer_hand = [draw_stack.pop() for _ in range(5)]
    discard_pile = []
    top_four_cards = []
#ID: 5672969

#ID: 5671165
#Calculate leftover cards
def process_leftover_card(card : Card, owner : str) -> None:
    """Processes a leftover card at the end of the game and calculates their scores.

    This function calculates the point of a leftover card based on its type 
    and gives it to the appropriate player (player or computer). 
    The card is then added to the discard pile. 

    Args:
        card (Card): The leftover card to process.
        owner (str): The owner of the card "player" or "computer".

    Returns:
        None
    """
    global player_score, computer_score, discard_pile, leftover_points, game_state

    if card.card_type == "regular":
        leftover_points = card.number
    elif card.card_type in ("wild", "watcher", "joker"):
        leftover_points = 10
    elif card.card_type in ("colorstorm", "ascendancy", "swap"):
        leftover_points = 0
    elif card.card_type in ("twopoints", "twopoints2"):
        leftover_points = 2
    if owner == "player":
        player_score += leftover_points
    else:
        computer_score += leftover_points

    discard_pile.append(card)
#ID: 5671165

#ID: 5672969
def check_game_over() -> None:
    """Checks the end of the game and processes leftover cards.

    This function checks if the game has ended according to:
    - One card remains between both hands.
    - Both players have one card remaining, and at least one is a Watcher card.
    - No cards in the draw stack or either hand.

    Returns:
        None
    """
    global player_hand, computer_hand, game_state, result_message

    #One card remains between both hands
    if len(player_hand) == 1 and len(computer_hand) == 0:
        result_message = "Game ended with 1 leftover card."
        process_leftover_card(player_hand.pop(), "player")
        game_state = LAST_ROUND

    elif len(computer_hand) == 1 and len(player_hand) == 0:
        result_message = "Game ended with 1 leftover card."
        process_leftover_card(computer_hand.pop(), "computer")
        game_state = LAST_ROUND

    #Both players have one card remaining, and at least one is a Watcher card
    elif len(player_hand) == 1 and len(computer_hand) == 1:
        if player_hand[0].card_type == "watcher":
            result_message = f"Game ended with 2 leftover cards."
            process_leftover_card(player_hand.pop(), "player")
            process_leftover_card(computer_hand.pop(), "computer")
            game_state = LAST_ROUND

        elif computer_hand[0].card_type == "watcher":
            result_message = f"Game ended with 2 leftover cards."
            process_leftover_card(computer_hand.pop(), "computer")
            process_leftover_card(player_hand.pop(), "player")
            game_state = LAST_ROUND

    #No cards in the draw stack or either hand
    elif len(draw_stack) == 0 and len(player_hand) == 0 and len(computer_hand) == 0:
        result_message = "Game ended. No cards left to play or draw."
        game_state = LAST_ROUND
#ID: 5672969

#ID: 5671165
#Initialize Watcher queues
def initialise_watcher_history() -> None:
    """Initialise history queues for Watcher card.

    Build fixed size queues to track the last two cards played by both the
    player and the computer. These histories are used by the Watcher card logic. 

    Returns:
        None
    """
    global player_card_history, computer_card_history

    player_card_history = Queue(2)
    computer_card_history = Queue(2)
#ID: 5671165

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
    if (game_state == SHOWING_RESULT or game_state == LAST_ROUND) and result_message:
        font = pygame.font.SysFont(None, 36)
        text = font.render(result_message, True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
#ID: 5672969

#ID: 5672969, 5671165
# Computer plays a card
def computer_play_card() -> tuple[Card | None, bool]:
    """Computer selects a card to play.

    The computer randomly selects a card from the computer's hand.
    If a wild card is selected, it is played and discarded.
    The computer then uses the max-heap data structure to choose one of the
    largest four regular cards from the draw stack or discard pile randomly.
    That card is returned as the computer played card.
    Also, it filters the cards if the Watcher card is in the computer hand. 
    So the computer don't choose Watcher card.

    Returns:
        tuple[Card | None, bool]: Contains:
            - The selected Card object.
            - A boolean indicator to tell whether the card was chosen as a result of using the Wild card (True), 
            or from computer hand (False).
    """
    global draw_stack

    if not computer_hand:
        return None, False
    
    #Filter computer hand if Watcher card in computer hand
    playable_cards = list(filter(lambda card: card.card_type != "watcher", computer_hand))
    if not playable_cards:
        return None, False
    
    card = random.choice(playable_cards)
    computer_hand.remove(card)

    #ID: 5671165
    if card.card_type == "wild":
        # Play and discard the wild card
        discard_card(card)

        # Choose source list(draw stack or discard pile) based on regular card availability
        source = draw_stack if has_regular(draw_stack) else discard_pile

        # Build a max-heap list to find the largest four cards
        heap = MaxHeap()
        for card in source:
            if card.card_type == "regular":
                heap.add(card)

        largest_four = heap.get_largest_four()
        if not largest_four:
            return None, False
        
        # Remove the chosen card from draw stack
        chosen_card = random.choice(largest_four)
        draw_stack[:] = list(filter(lambda card: card is not chosen_card, draw_stack))
        return chosen_card, True
    #ID: 5671165

    return card, False 
#ID: 5672969, 5671165

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
def quicksort(cards: list) -> list:
    """
    Sorts a lists of Cards objects in ascending order using Quicksort.

    Parameters:
        cards (list of cards): The list of Card objects to sort.

    Returns:
        list: A new list of cards sorted by their numbers
    """

    if len(cards) <= 1:
        return cards
    else:
        pivot = cards[0]
        less = [card for card in cards[1:] if card.number <= pivot.number]
        greater = [card for card in cards[1:] if card.number > pivot.number]
        return quicksort(less) + [pivot] + quicksort(greater)
#ID: 5670726

#ID: 5670726
# Evaluate the round
def resolve_round(
    computer_used_wild: bool = False,
    player_used_wild: bool = False,
    player_wild_card: Card | None = None
) -> tuple[list[Card], str, str]:
    """Handles a single round of the game.

      Compares player and computer cards.
      Applies scoring and bonus logic.
      Updates the discard pile, game state, and tracks previously played cards.

    Args:
        computer_used_wild (bool): True if the computer played the Wild card.
        player_used_wild (bool): True if the player played the Wild card.
        player_wild_card (Card): The card selected by the player using the Wild card.

    Returns:
        tuple:
             discard_pile (list[Card]): The updated discard pile.
             result_message (str): A message summarizing the round result.
             played_info (str): Detailed info about which cards were played.
    """
    global player_played_card, computer_played_card
    global player_score, computer_score, discard_pile, draw_stack
    global player_hand, computer_hand, game_state, result_message
    global previous_player_card, previous_computer_card, watcher_message
    
    watcher_message = ""

    if not player_played_card or not computer_played_card: # Check if both player played a card
    
        return discard_pile, result_message, "No cards played."
    
    played_info = f"Player played: {player_played_card}" # Show the cards played
    if player_used_wild and player_wild_card:
        played_info += f" (using Wild card)"

    played_info += f" | Computer played: {computer_played_card}" # Show the cards played
    if computer_used_wild:
        played_info += " (using Wild card)"

    #Track last played cards for Watcher implementation
    player_card_history.enqueue(player_played_card)
    computer_card_history.enqueue(computer_played_card)

    #Player Watcher card watching computer history
    if len(computer_card_history) == 2:
        c1, c2 = computer_card_history[0], computer_card_history[1]
        if c1.color == c2.color:
            for i, card in enumerate(player_hand):
                if card.card_type == "watcher":
                    bonus = (c1.number + c2.number + 1) // 2
                    player_score += bonus
                    watcher_message += f"Player's Watcher triggered! +{bonus} points."
                    discard_card(player_hand.pop(i))
                    player_draw_card()
                    break

    #Computer Watcher card watching computer history
    if len(player_card_history) == 2:
        p1, p2 = player_card_history[0], player_card_history[1]
        if p1.color == p2.color:
            for i, card in enumerate(computer_hand):
                if card.card_type == "watcher":
                    bonus = (p1.number + p2.number + 1) // 2
                    computer_score += bonus
                    watcher_message += f"Computer's Watcher triggered! +{bonus} points."
                    discard_card(computer_hand.pop(i))
                    computer_draw_card()
                    break

    # Handling special card vs special card combinations
    twopoints_player = player_played_card.card_type == "twopoints"
    twopoints_computer = computer_played_card.card_type == "twopoints"
    colorstorm_played = player_played_card.card_type == "colorstorm" or computer_played_card.card_type == "colorstorm"
    ascendancy_played = player_played_card.card_type == "ascendancy" or computer_played_card.card_type == "ascendancy"
    joker_player = player_played_card.card_type =="joker"
    joker_computer = computer_played_card.card_type =="joker"
    swap_player = player_played_card.card_type =="swap"
    swap_computer = computer_played_card.card_type =="swap"

    if colorstorm_played or twopoints_player or twopoints_computer or ascendancy_played or joker_player or joker_computer or swap_player or swap_computer:
        discard_card(player_played_card)
        discard_card(computer_played_card)

        # Handling two points card
        if not (joker_player or joker_computer):
            if twopoints_player:
                player_score += 2
            if twopoints_computer:
                computer_score += 2

        # Handling joker card
        if joker_player:
            if computer_played_card.card_type == "regular":
                player_score += computer_played_card.number
                result_message = f"Player played joker and gets {computer_played_card.number} points!"
            else:
                player_score += 5
                result_message = f"Player played joker and gets 5 points! {computer_played_card.card_type.capitalize()} is not activated"
            
        elif joker_computer:
            if player_played_card.card_type == "regular":
                computer_score += player_played_card.number
                result_message = f"Computer played joker and gets {player_played_card.number} points!"
            else:
                computer_score += 5
                result_message = f"computer played joker and gets 5 points! {player_played_card.card_type.capitalize()} is not activated"

        # Handling swap card
        if not (joker_player or joker_computer):
            if swap_player or swap_computer:
                if draw_stack:
                    player_draw_card()
                if draw_stack:
                    computer_draw_card()
                player_hand, computer_hand = computer_hand, player_hand

        # Handles if both colorstorm and ascendancy played together, one of them is randomly chosen
        if not (joker_player or joker_computer):
            if colorstorm_played and ascendancy_played: 
                if len(draw_stack) >= 3:
                    if random.choice(["colorstorm", "ascendancy"]) == "colorstorm": # Handles if colorstorm is activated
                        grouped = defaultdict(list) # Group cards by color
                        for card in draw_stack:
                            grouped[card.color].append(card) 
                        for color in grouped: # Sort each color group numbers in ascending order using quicksort
                            grouped[color] = quicksort(grouped[color])
                        color_order = list(grouped.keys()) # shuffle color groups randomly
                        shuffle(color_order)
                        draw_stack = [] # Rebuild the draw stack
                        for color in color_order:
                            draw_stack.extend(grouped[color])
                    else: # Handles if ascendancy is activated
                        draw_stack = quicksort(draw_stack)
                    result_message = "Colorstorm and Ascendancy played! One card is activated, but it's a mystery."
                else:
                    result_message = "Not enough cards in the draw stack to activate special card."

        # Handling only colorstorm card
        if not (joker_player or joker_computer):
            if colorstorm_played:
                if len(draw_stack) >= 3:
                    grouped = defaultdict(list) # Group cards by color
                    for card in draw_stack:
                        grouped[card.color].append(card) 
                    for color in grouped: # Sort each color group numbers in ascending order using quicksort
                        grouped[color] = quicksort(grouped[color])
                    color_order = list(grouped.keys()) # shuffle color groups randomly
                    shuffle(color_order)
                    draw_stack = [] # Rebuild the draw stack
                    for color in color_order:
                        draw_stack.extend(grouped[color])
                    result_message = "Colorstorm played! Draw stack reordered by color"
                else:
                    result_message = "Colorstorm played! There is no enough cards to reorder in the draw stack"

        # Handling only acendancy card
        if not (joker_player or joker_computer):
            if ascendancy_played: # Sorts the draw stack by numbers
                if len(draw_stack) >= 2:
                    draw_stack = quicksort(draw_stack)
                    result_message = "Ascendancy played! Draw stack is sorted in ascending order"
                else:
                    result_message = "Ascendancy played! There is no enough cards to sort the draw stack"

        # Two points card + swap card combination result messages (if joker wasnt played)
        if not (joker_player or joker_computer):
            if twopoints_player and twopoints_computer:
                result_message =  "Both players used Two points card! Each gets 2 points."
            elif twopoints_player and colorstorm_played:
                result_message = "Two points and Colorstorm Cards are played! Player gets 2 points and Draw stack is reordered"
            elif twopoints_player and ascendancy_played:
                result_message = "Two points and Ascendancy Cards are played! Player gets 2 points and Draw stack is sorted"
            elif twopoints_computer and swap_player:
                result_message = "Two points and Swap cards are played! Computer gets 2 points and hands are swapped"
            elif swap_player and ascendancy_played:
                result_message = "Swap and Ascendancy are played! Draw stack is sorted and hands are swapped"
            elif swap_player and colorstorm_played:
                result_message = "Swap and Colorstorm are played! Draw stack is reordered and hands are swapped"
            elif twopoints_player:
                result_message = "Player used two points card and gets 2 points"
                
            elif twopoints_computer and colorstorm_played:
                result_message = "Two points and Colorstorm are played! Computer gets 2 points and draw stack is reordered"
            elif twopoints_computer and ascendancy_played:
                result_message = "Two points and Ascendancy are played! Computer gets 2 points and draw stack is sorted"
            elif twopoints_player and swap_computer:
                result_message = "Two points and Swap are Played! Player gets 2 points and hands are swapped"
            elif swap_computer and ascendancy_played:
                result_message = "Swap and Ascendancy are played! Draw stack is sorted and hands are swapped"
            elif swap_computer and colorstorm_played:
                result_message = "Swap and Colorstorm are played! Draw stack is reordered and hands are swapped"
            elif twopoints_computer:
                result_message = "Computer used two points card and gets 2 points"

        if not result_message and not(joker_player or joker_computer):
            if swap_player:
                result_message = "Player used Swap! Hands have been exchanged"
            elif swap_computer:
                result_message = "Computer used Swap! Hands have been exchanged"
                
        draw_order = ["player", "computer"]
        draw_order = shuffle(draw_order) # Makes drawing cards order random
        for who in draw_order:
            if draw_stack:
                if who == "player" and len(player_hand) < 5:
                    player_draw_card()
                elif who == "computer" and len(computer_hand) < 5:
                    computer_draw_card()

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

    #Illustrate Watcher card message if executed
    if watcher_message:
        result_message += " " + watcher_message

    result_message += round_message

    # Move played cards to discard pile
    discard_card(player_played_card)
    discard_card(computer_played_card)

    # Draw new cards 
    if draw_stack and len(player_hand) < 5:
        player_draw_card()
    if draw_stack and len(computer_hand) < 5:
        computer_draw_card()

    check_game_over()

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
def play_selected_card() -> bool:
    """Plays the selected card and updates the game state.

    This function checks the player's hand for the selected card.
    If the Wild card is selected, the wild card logic is implemented and the card 
    is discarded, otherwise the selected card is set as the player's 
    played card.
    The selected card is removed from player's hand, and the game state is updated.

    Returns:
        bool: True if a regular card was played, 
        False if a wild card was played or no card was selected.
    """
    global player_hand, player_played_card, game_state

    for i, card in enumerate(player_hand): ####
        if card.selected:
            card.selected = False
            
            if card.card_type == "watcher": #########
                return False

            if card.card_type == "wild":
                wild_card_logic()
                discard_card(card)
                game_state = WILD_CARD
                player_hand.pop(i)
                return False
            else:
                player_played_card = card
                player_hand.pop(i)
                game_state = WAITING_FOR_COMPUTER
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

#ID: 5671165
# Wild card logic implementation
def wild_card_logic() -> None:
    """Selects the top four regular cards using a max-heap strategy for the wild card effect.

    This function chooses a list source (draw stack or discard pile) when 
    the Wild card is played based on regular card availability.
    It uses the max-heap data structure to extract the four largest 
    values from regular cards.
    These cards are stored in the global variable `top_four_cards`, 
    which will be shown to the player
    when a wild card is played.
    """
    global draw_stack, discard_pile, top_four_cards

    source = draw_stack if has_regular(draw_stack) else discard_pile

    heap = MaxHeap()
    for card in source:
        if card.card_type == "regular":
            heap.add(card)

    top_four_cards = heap.get_largest_four()
#ID: 5671165

#ID: 5671165
# Draw the wild card display
def draw_wild_display() -> None:
    """Draws the selection screen when the Wild card is played.

    This function draws the selection screen when the Wild card is played
    on top of the game screen, displays a message to the player to choose
    one of the four cards and displays the largest four regular cards stored in 
    the global variable `top_four_cards`.
    """
    global top_four_cards

    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    # Draw game 'Choose one of these cards' message
    font_large = pygame.font.SysFont(None, 72)
    wild_card_text = font_large.render("Choose one of these cards", True, WHITE)
    screen.blit(wild_card_text, (SCREEN_WIDTH // 2 - wild_card_text.get_width() // 2, SCREEN_HEIGHT // 4))
    
    # Draw wild cards options 
    total_width = len(top_four_cards) * CARD_WIDTH + (len(top_four_cards) - 1) * CARD_SPACING

    # Calculate the starting x position to center the cards
    start_x = (SCREEN_WIDTH - total_width) // 2
    
    # Draw each card
    for i, card in enumerate(top_four_cards):
        x = start_x + i * (CARD_WIDTH + CARD_SPACING)
        y = SCREEN_HEIGHT - CARD_HEIGHT - 50
        card.draw(x, y, face_up=True)
#ID: 5671165

#ID: 5672969
# Draw the game board
def draw_game_board():
    """Draws the game board.
    
    This function draws all the game elements including the player's hand,
    played cards, discard pile, draw stack, play button, wait message, 
    the Wild card display if it is choosen by player and 
    scores based on the current game state.
    
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
        
        # Draw the Wild card select display if the Wild card is chosen
        if game_state == WILD_CARD:
            draw_wild_display()

        # Draw game state specific instructions
        font = pygame.font.SysFont(None, 36)
        if game_state == SELECTING_CARD:
            instruction_text = font.render("Select a card and click 'Play Card'", True, WHITE)
        elif game_state == WAITING_FOR_COMPUTER:
            instruction_text = font.render("Waiting for computer to play...", True, WHITE)
        elif game_state == SHOWING_RESULT:
            instruction_text = font.render("Click anywhere to continue", True, WHITE)
        elif game_state == LAST_ROUND:
            instruction_text = font.render("Game over! Click anywhere to see the winner.", True, WHITE)
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

    elif game_state in [SELECTING_CARD, WAITING_FOR_COMPUTER, SHOWING_RESULT, WILD_CARD]:
        check_game_over()
        return play_button, None

    elif game_state == LAST_ROUND:
        return play_button, None

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
        #Prevent choosing Watcher card
        if card.card_type == "watcher":
            continue

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
    - Wild card implementation
    - Last round resolving

    Returns:
        None
    """
    global player_score, computer_score, game_state, player_played_card, computer_played_card, result_message
    global previous_player_card, previous_computer_card, played_card_message, selected_card
    global top_four_cards, player_used_wild, last_player_wild_choice, discard_pile
    global player_card_history, computer_card_history, leftover_points, watcher_message

    # Initialize the game
    deal_cards()
    initialise_watcher_history()
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

            # Handles user input if the Wild card is selected
            if game_state == WILD_CARD:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for card in top_four_cards:
                        if card.rect.collidepoint(event.pos):
                            # Set the selected card as the player played card
                            player_played_card = card
                            # Track the player's Wild card selection for info
                            last_player_wild_choice = card
                            # Mark that the player used the Wild card
                            player_used_wild = True         
                            top_four_cards.remove(card)
                            # Checks that the chosen card is not in the draw stack 
                            draw_stack[:] = list(filter(lambda c: c is not card, draw_stack))
                            game_state = WAITING_FOR_COMPUTER
            
            elif game_state == SHOWING_RESULT:
                # Progress to next round when user clicks
                if event.type == pygame.MOUSEBUTTONDOWN:
                    check_game_over()
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
                        player_card_history.clear()
                        computer_card_history.clear()
                        selected_card = None
                        play_button_rect = None
                        play_again_button_rect = None
                        computer_play_time = 0
                        leftover_points = 0
                        player_played_card = None
                        computer_played_card = None
                        last_player_wild_choice = None
                        result_message = ""
                        played_card_message = ""
                        watcher_message = ""
                        game_state = SELECTING_CARD
            
            elif game_state == LAST_ROUND:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game_state = GAME_OVER

        # Handle computer's turn
        if game_state == WAITING_FOR_COMPUTER and current_time >= computer_play_time:
            computer_played_card, computer_used_wild = computer_play_card()
            discard_pile, result_message, played_info = resolve_round(computer_used_wild, player_used_wild, last_player_wild_choice)
            player_used_wild = False  # reset after use
            last_player_wild_choice = None

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