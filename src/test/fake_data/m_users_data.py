import random
import csv
from typing import List, Tuple, Optional
from concurrent.futures import ProcessPoolExecutor, as_completed
from wonderwords import RandomWord

FIRST_NAMES = [
    "Tri-An",
    "Audrey",
    "Sylvia",
    "Daniel",
    "Samantha",
    "Darin",
    "Damien",
    "Matthew",
    "Kiana",
    "Austin",
    "Alayna",
    "Annabel",
    "Jason",
    "John",
    "Kenneth",
    "Jordan",
    "Simon",
    "Michael",
    "Youngji",
    "Abigail",
]
LAST_NAMES = [
    "Pham",
    "Tran",
    "Du",
    "Chen",
    "Santosa",
    "Gong",
    "Butler",
    "Britten",
    "Wong",
    "Chai",
    "Toussant",
    "Chong",
    "Loo",
    "Ma",
    "Chou",
    "Lam",
    "Lee",
    "Kim",
    "Pyun",
]

EMAIL_DOMAINS = ["gmail", "yahoo", "hotmail", "outlook", "aol", "msn"]


def random_email() -> str:
    return random.choices(EMAIL_DOMAINS, [0.5, 0.15, 0.15, 0.1, 0.05, 0.05])[0]


def gen_random_name_and_email() -> Tuple[str, Optional[str]]:
    rw = RandomWord()

    email = None
    name = ""

    case = random.randint(0, 3)
    use_email = random.randint(0, 1)
    use_first = random.randint(0, 1)

    if case == 0:
        name = random.choice(FIRST_NAMES if use_first else LAST_NAMES)
        name += str(random.randint(0, 9999))
        if use_email:
            email = f"{name}@{random_email()}.com"

    elif case == 1:
        base_name = random.choice(FIRST_NAMES if use_first else LAST_NAMES)
        try:
            prefix_len = random.randint(1, len(base_name) - 1)
            name = rw.word(starts_with=base_name[:prefix_len])
        except Exception:
            name = base_name[0] + random.choice(LAST_NAMES)
        name += str(random.randint(0, 9999))
        email = f"{name}@{random_email()}.com"

    elif case == 2:
        try:
            adj = rw.word(include_parts_of_speech=["adjectives"])
            noun = rw.word(include_parts_of_speech=["nouns"])
        except Exception:
            adj = "Untitled"
            noun = random.choice(FIRST_NAMES if use_first else LAST_NAMES)
        name = f"{adj}{noun}{random.randint(0, 9999)}"

    elif case == 3:
        name = rw.word()
        name += random.choice(FIRST_NAMES if use_first else LAST_NAMES)
        if random.randint(0, 1):
            name += str(random.randint(0, 99))
        if use_email:
            email = f"{name}@{random_email()}.com"

    return name, email


# ⛏️ Worker function to generate N users
def generate_chunk(chunk_size: int) -> List[Tuple[str, Optional[str]]]:
    return [gen_random_name_and_email() for _ in range(chunk_size)]


# ⚡ Main function using chunked parallelism
def generate_fake_users_chunked(
    total: int, chunk_size: int = 1000, max_workers: int = None
) -> List[Tuple[str, Optional[str]]]:
    chunks = total // chunk_size + (1 if total % chunk_size != 0 else 0)

    results: List[Tuple[str, Optional[str]]] = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(
                generate_chunk,
                chunk_size if i < chunks - 1 else total % chunk_size or chunk_size,
            )
            for i in range(chunks)
        ]
        for future in as_completed(futures):
            results.extend(future.result())

    return results


# 🧪 Usage
if __name__ == "__main__":
    from time import time

    start = time()

    USERS_TO_GENERATE = 1_000_000  # Change to 100_000 or more
    fake_users = generate_fake_users_chunked(total=USERS_TO_GENERATE, chunk_size=1000)

    print(f"Generated {len(fake_users)} users in {round(time() - start, 2)} seconds")
