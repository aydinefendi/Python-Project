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
        self.name = name #Used to identify special cards

    def __str__(self):
        # If its a special card it returns its name, otherwise show colour and number
        return f"{self.colour} {self.number}" if not self.special else self.name

def round(player_card: Card, computer_card: Card, scores: dict, discard_pile: list[Card]) -> tuple[dict, list[Card]]:
    """
    Compares the player's and computer's cards and updated the scores and discard pile accordingly.

    Parameters:
        player_card (Card): The card chosen by the player.
        computer_card (Card): The card chosen by the computer.
        scores (dict): Current scores of both players.
        discard_pile (list): the pile where the card played will be added.

    Returns:
    tuple: Updated scores and discard pile.
    """
    