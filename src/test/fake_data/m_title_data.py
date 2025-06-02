"""THE BELOW IS GENERATED USING CHATGPT"""

import random

TEMPLATES = [
    "How I {verb_past} {piece} in {number} {moves}",
    "{number} reasons the {opening} is {adjective}",
    "Stop playing the {opening} if you value your rating",
    "My worst {blunder_type} against a {elo_rank} player",
    "Why {grandmaster} says the {opening} is {adjective}",
    "How to crush {elo_rank}s with the {opening}",
    "The {opening} is secretly {adjective} — here's why",
    "Every time I play the {piece}, I get {adjective}",
    "Blundered my {piece} and still won 🤯",
    "If you play {opening}, you're probably {adjective}",
    "Would you resign here? ({number}-move game)",
    "When I {verb_past} my {piece}, the engine went +{eval}",
    "Guess the move: {opening} edition",
]

# Word banks
verbs_past = ["sacrificed", "traded", "blundered", "defended", "pinned", "forked"]
pieces = ["queen", "rook", "bishop", "knight", "pawn", "king"]
openings = [
    "Sicilian Defense",
    "Queen's Gambit",
    "King's Indian",
    "London System",
    "Scandinavian Defense",
    "Caro-Kann",
    "French Defense",
    "Ruy Lopez",
]
adjectives = ["underrated", "overrated", "brilliant", "terrible", "spicy", "solid"]
elo_ranks = ["600", "800", "1000", "1200", "1500", "1800", "2000", "2200", "GM"]
blunder_types = ["mouse slip", "time scramble", "miscalculation", "blunder"]
evals = ["5.4", "3.2", "7.8", "10.0", "-4.5", "0.0"]
numbers = [str(n) for n in range(3, 50)]
moves = ["moves", "turns", "plies"]
grandmasters = [
    "Hikaru",
    "Magnus",
    "GothamChess",
    "Levy",
    "Firouzja",
    "Nakamura",
    "Kramnik",
    "Judith Polgar",
]


# Title generator
def generate_chess_title():
    template = random.choice(TEMPLATES)
    return template.format(
        verb_past=random.choice(verbs_past),
        piece=random.choice(pieces),
        opening=random.choice(openings),
        adjective=random.choice(adjectives),
        elo_rank=random.choice(elo_ranks),
        blunder_type=random.choice(blunder_types),
        eval=random.choice(evals),
        number=random.choice(numbers),
        moves=random.choice(moves),
        grandmaster=random.choice(grandmasters),
    )
