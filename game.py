#ID: 5670726

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

def round(player_card: Card, computer_card: Card, scores: dict, discard_pile: list[Card]) -> tuple[dict, list[Card]]:
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
    # Show the cards played
    print(f"Player played: {player_card}")
    print(f"Computer played: {computer_card}")

    # Comparing numbers if colours match
    if player_card.colour == computer_card.colour:
        if player_card.number > computer_card.number:
            winner = "player"
        elif player_card.number < computer_card.number:
            winner = "computer"
        else:
            winner = "tie"

        if winner != "tie":
            points = player_card.number + computer_card.number
            scores[winner] += points
            print(f"{winner.capitalize()} wins the round and gets {points} points!")
        else:
            print("It's a tie!. No points awarded.")
    else: # If colours don't match
        print("Colours doesn't match!. No points awarded.")

    discard_pile.append(player_card)
    discard_pile.append(computer_card)
    return scores, discard_pile

#ID: 5670726