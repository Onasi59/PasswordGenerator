
"""
Simple but secure password generator.
Uses the `secrets` module for cryptographic randomness and `string` for character sets.
"""

import string
import secrets
import sys
import random  # used for shuffling 


_sysrand = random.SystemRandom()


def build_charset(use_lower=True, use_upper=True, use_digits=True, use_symbols=True):
    """Return a dict of the chosen character classes and the combined pool."""
    classes = {}
    pool = ""

    if use_lower:
        classes["lower"] = string.ascii_lowercase
        pool += string.ascii_lowercase
    if use_upper:
        classes["upper"] = string.ascii_uppercase
        pool += string.ascii_uppercase
    if use_digits:
        classes["digits"] = string.digits
        pool += string.digits
    if use_symbols:
        
        classes["symbols"] = "!@#$%^&*()-_=+[]{};:,.<>/?"
        pool += classes["symbols"]

    return classes, pool


def generate_password(length, classes, pool):
    """
    Ensure the generated password contains at least one character from each chosen class,
    then fill the rest from the full pool and shuffle to avoid predictable patterns.
    """
    if not pool:
        raise ValueError("Character pool is empty. Enable at least one character type.")

    if length < len(classes):
        raise ValueError(f"Length must be at least {len(classes)} to include one of each selected type.")

   
    password_chars = [secrets.choice(chars) for chars in classes.values()]

   
    remaining = length - len(password_chars)
    password_chars += [secrets.choice(pool) for _ in range(remaining)]

    
    _sysrand.shuffle(password_chars)

    return "".join(password_chars)


def ask_yes_no(prompt, default=True):
    """Ask a yes/no question; return True/False. Accepts 'y/n' or empty for default."""
    default_str = "Y/n" if default else "y/N"
    while True:
        resp = input(f"{prompt} ({default_str}): ").strip().lower()
        if not resp:
            return default
        if resp in ("y", "yes"):
            return True
        if resp in ("n", "no"):
            return False
        print("Please answer 'y' or 'n'.")


def main():
    print("Password Generator — Secure, configurable, simple\n")

    # Ask for length
    try:
        length_input = input("Enter password length (suggested 12-24): ").strip()
        length = int(length_input)
        if length <= 0:
            print("Length must be a positive integer.")
            return
    except ValueError:
        print("Invalid input. Please enter a whole number for length.")
        return

    # Character class choices
    use_lower = ask_yes_no("Include lowercase letters?", True)
    use_upper = ask_yes_no("Include uppercase letters?", True)
    use_digits = ask_yes_no("Include digits (0-9)?", True)
    use_symbols = ask_yes_no("Include symbols (e.g. !@#$%)?", True)

    classes, pool = build_charset(use_lower, use_upper, use_digits, use_symbols)

    if not pool:
        print("You must enable at least one character type. Exiting.")
        return

    # Number of passwords to generate
    try:
        how_many_input = input("How many passwords to generate? (default 1): ").strip()
        how_many = int(how_many_input) if how_many_input else 1
        if how_many <= 0:
            print("Number of passwords must be at least 1.")
            return
    except ValueError:
        print("Invalid number. Exiting.")
        return

    print("\nGenerated password(s):")
    for i in range(how_many):
        try:
            pwd = generate_password(length, classes, pool)
        except ValueError as e:
            print(f"Error: {e}")
            return
        print(pwd)

    
    copy_ok = False
    try:
        import pyperclip
        try:
            pyperclip.copy(pwd)
            copy_ok = True
        except Exception:
            copy_ok = False
    except ImportError:
        copy_ok = False

    if copy_ok:
        print("\nThe last password was copied to your clipboard.")
    else:
        print("\nTip: install 'pyperclip' (`pip install pyperclip`) to enable clipboard copy.")

    print("Done.")


if __name__ == "__main__":
    main()
