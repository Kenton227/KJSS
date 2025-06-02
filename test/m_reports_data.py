import random

BRIEFS = [
    "Engine Use Suspected",
    "Unsportsmanlike Conduct",
    "Inappropriate Username",
    "Spam or Repetitive Posting",
    "Toxic Comment",
    "Offensive Language",
    "Fake Achievement Claim",
    "Cheating Accusation",
    "Harassment in Comments",
    "Suspicious Blitz Win",
    "Graphic Meme in Caption",
    "Excessive Self-Promotion",
    "Impersonating a GM",
    "Illegal Opening Move (?)",
    "Username Contains Slur",
]

DETAILS = [
    "User won 17 bullet games in a row with 99% accuracy. Very likely an engine.",
    "Comment included profanity after losing to a much lower-rated player.",
    "Username appears to contain a hidden offensive slur.",
    "Posted the same link to their Twitch channel on 5 consecutive posts.",
    "User accused others of cheating without evidence in multiple posts.",
    "Their caption contained racial slurs directed at another user.",
    "Claims they beat Magnus Carlsen in a 3+0 blitz match—clearly fake.",
    "Comment section shows repeated personal attacks against other players.",
    "Used a manipulated screenshot to fake a brilliant move.",
    "Posted a violent meme in response to a losing game.",
    "Repeated use of 'gg ez' in a mocking way across several games.",
    "Their caption encouraged viewers to click a sketchy external link.",
    "Their game contained a sequence that violates basic opening theory.",
    "Kept messaging the same user with unsolicited advice.",
    "Multiple accounts appear to be used by the same person for likes.",
]


def generate_fake_report() -> tuple:
    return random.choice(BRIEFS), random.choice(DETAILS)
