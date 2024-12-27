#!/usr/bin/python
import ast
import random
import unicodedata

blacklist = [
    "exec",
    "eval",
    "str",
    "compile",
    "open",
    "read",
    "file",
    "import",
    "globals",
    "locals",
    "class",
    "os",
    "subprocess",
    "input",
    "setattr",
    "getoutput",
    "getattr",
    "delattr",
    "vars",
    "__",
    "dir",
    "builtin",
    "base",
    "help",
]


def poem_creator():
    print("Welcome to the Poem Creator!")
    print("Enter the name of your muse:")

    user_input = input("> ")
    normalized_user_input = (
        unicodedata.normalize("NFKD", user_input).encode("ASCII", "ignore").decode()
    )
    if any(func in normalized_user_input for func in blacklist):
        print("Denied")
        return

    muse_name = eval(
        f"""\'{user_input}\'"""
    )  # muse_name = ast.literal_eval(f"""\'{user_input}\'""")

    print(muse_name)

    stanza_beginnings = [
        f"Under the moonlight, {muse_name} dances gracefully,",
        f"In the garden of dreams, {muse_name} whispers secrets softly,",
        f"Amidst the stars, {muse_name} shines brightly,",
        f"With each sunrise, {muse_name} paints the sky with colors divine,",
    ]
    stanza_middles = [
        "Inspiring hearts and minds,",
        "Captivating all who behold,",
        "Enchanting with every step,",
        "Bringing joy to the world,",
    ]
    stanza_ends = [
        "A muse beyond compare.",
        "In every verse, a tale to share.",
        "A timeless beauty beyond compare.",
        "In every heart, forever there.",
    ]

    # Randomly selecting elements for the poem
    beginning = random.choice(stanza_beginnings)
    middle = random.choice(stanza_middles)
    end = random.choice(stanza_ends)

    print(f"\n{beginning}\n{middle}\n{end}")


poem_creator()
