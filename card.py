class Card:
    def __init__(self, colour: str, number: int, special: bool = False, name: str = ""):
        self.colour = colour
        self.number = number
        self.special = special
        self.name = name #To identify special cards

    def __str__(self):
        # If its a special card it returns its name, otherwise show colour and number
        return f"{self.colour} {self.number}" if not self.special else self.name