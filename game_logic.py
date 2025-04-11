from card import Card
from scoring import calculate_points
from typing import List

# Resolving round function
def resolve_round(player_card: Card, computer_card: Card,
          scores: dict, discard_pile: list[Card],
          previous_player_card: Card = None,
          previous_computer_card: Card = None) -> tuple[dict, list[Card]]:

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


# Refilling hands function
def refill_hands(player_hand: List[Card], computer_hand: List[Card],
                 draw_stack: List[Card], discard_pile: List[Card]) -> tuple[List[Card], List[Card], List[Card], List[Card]]:

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
