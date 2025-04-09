#ID: 5670726

from typing import List

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

#ID: 5670726