import random

CAPTION_TEMPLATES = [
    "Can't believe I {verb_past} my {piece} like that.",
    "The {opening} always messes me up — need to study it more.",
    "Any tips for handling {elo_rank}s who spam the {opening}?",
    "This game was wild — engine eval went from +3 to -5 in two moves.",
    "Just another day blundering in the {time_control} pool.",
    "I really thought I had mate in {number}, but I completely missed {tactic}.",
    "Lessons learned: always double-check before {verb_ing} a {piece}.",
    "I think the {opening} suits my style better than the {opening_alt}.",
    "Not my cleanest game, but happy with the endgame technique.",
    "This was one of those games where nothing made sense and everything worked.",
    "",  # Blank caption
]

verb_past = ["sacked", "hung", "misclicked", "traded", "lost", "blundered"]
verb_ing = ["sacrificing", "pushing", "fianchettoing", "trading"]
pieces = ["queen", "rook", "knight", "bishop", "pawn"]
openings = ["Scandinavian", "London", "King's Indian", "Sicilian", "French"]
opening_alt = ["Caro-Kann", "Ruy Lopez", "Queen's Gambit"]
tactics = ["the fork", "back rank mate", "a skewer", "a zugzwang", "a stalemate"]
elo_ranks = ["600s", "800s", "1000s", "1200s", "1500s", "1800s", "GM level"]
time_controls = ["blitz", "bullet", "rapid", "classical"]
numbers = [str(n) for n in range(2, 20)]


def generate_chess_caption():
    template = random.choice(CAPTION_TEMPLATES)
    return template.format(
        verb_past=random.choice(verb_past),
        verb_ing=random.choice(verb_ing),
        piece=random.choice(pieces),
        opening=random.choice(openings),
        opening_alt=random.choice(opening_alt),
        tactic=random.choice(tactics),
        elo_rank=random.choice(elo_ranks),
        time_control=random.choice(time_controls),
        number=random.choice(numbers),
    )
