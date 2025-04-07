#ID: 5670726

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

#ID: 5670726