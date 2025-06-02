import random

OPENINGS = [
    "Wait, did I just witness",
    "Not gonna lie,",
    "Seriously?",
    "Bruh.",
    "I was NOT ready for",
    "Plot twist:",
    "This reminds me of",
    "Actual goosebumps from",
    "Lowkey impressed by",
    "Hot take:",
]

PHRASES = [
    "that knight sac was illegal in 42 countries.",
    "Stockfish just fainted.",
    "I’ve never seen someone blunder so gracefully.",
    "pure opening theory collapse.",
    "is this what 600 ELO chess looks like?",
    "he calculated for 20 moves and still lost the rook.",
    "nah cause who plays the Bongcloud unironically?",
    "this is why I don't play the London.",
    "engine says +9.3 and he still flagged.",
    "f3 on move 1 is criminal.",
    "if you don't see the mate in 3, uninstall.",
    "this is why we don’t push the h-pawn early.",
    "actual GM tactics or just vibes?",
    "the bishop was just chilling and got sacrificed like that?",
    "the disrespect with that queen sac 💀",
    "king walked across the board like he owns it.",
    "rook lift of the century.",
    "he had mate in 1 and played a3 instead.",
    "my Rapid rating just dropped watching this.",
    "objectively terrible, but aesthetically glorious.",
    "this man is roleplaying as AlphaZero.",
    "someone please revoke their chess license.",
    "I felt that blunder in my soul.",
    "chess will never be the same.",
]

CLOSERS = [
    "Wild game.",
    "10/10 entertainment value.",
    "I need a rematch immediately.",
    "More of this chaos please.",
    "Petition to ban them from playing blitz.",
    "Absolute masterpiece.",
    "Makes me want to uninstall Lichess.",
    "Chef’s kiss.",
    "Peak content.",
    "Never let them touch a board again.",
]


def generate_chess_comment() -> str:
    sentence_count = random.randint(1, 5)
    sentences = []

    for _ in range(sentence_count):
        opener = random.choice(OPENINGS) if random.random() < 0.4 else ""
        body = random.choice(PHRASES)
        closer = random.choice(CLOSERS) if random.random() < 0.2 else ""
        sentence = " ".join([opener, body, closer]).strip()
        sentences.append(sentence)

    return " ".join(sentences)
