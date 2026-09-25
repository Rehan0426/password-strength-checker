import os
import string
import secrets
import argparse
import getpass
from math import log2

def main():
    parser = argparse.ArgumentParser(description="Password strength checker")

    parser.add_argument(
        "--generate",
        action="store_true",
        help="Generate a secure password"
    )

    parser.add_argument(
        "--length",
        type=int,
        default=12,
        help="Length of generated password (default: 12)"
    )

    args = parser.parse_args()

    if args.generate:
        try:
            password = generate_password(args.length)
            print(f"Generated password: {password}")
        except ValueError as e:
            print(f"Error: {e}")
        return

    password = getpass.getpass("Enter Password: ")

    entropy = calculate_entropy(password)
    patterns = find_patterns(password)
    common = is_common(password)
    score = score_password(password)
    label = get_strength_label(score)

    print("\n--- Password Audit ---")
    print(f"Entropy: {entropy:.2f} bits")
    print(f"Common password: {'Yes' if common else 'No'}")
    print(f"Score: {score:.2f}/100")
    print(f"Strength: {label}")

    if patterns:
        print("Patterns found:")
        for pattern in patterns:
            print(f"  > {pattern}")
    else:
        print("Patterns found:\n  > None")


# calculate entropy
def calculate_entropy(password):
    # check which categories are present
    has_lower = any(char.islower() for char in password)
    has_upper = any(char.isupper() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_symbol = any(char in string.punctuation for char in password)

    # calculate pool size
    pool_size = 0

    if has_lower:
        pool_size += 26
    if has_upper:
        pool_size += 26
    if has_digit:
        pool_size += 10
    if has_symbol:
        pool_size += 32

    # handling empty/invalid password
    if len(password) == 0 or pool_size == 0:
        return 0.0

    # calculate entropy
    entropy = len(password)*log2(pool_size)

    return entropy


#finding patterns
def find_patterns(password):
    issues = []

    # Check repeated characters
    for i in range(len(password) - 2):
        if password[i] == password[i+1] == password[i+2]:
            issues.append("Repeated characters.")
            break

    # check sequences
    for i in range(len(password) - 2):
        a = password[i]
        b = password[i+1]
        c = password[i+2]


        # All digits
        if (a.isdigit() and b.isdigit() and c.isdigit()):
            if (ord(b) - ord(a) == 1 and ord(c) - ord(b) == 1):
                issues.append("Sequential characters.")
                break

            if (ord(b) - ord(a) == -1 and ord(c) - ord(b) == -1):
                issues.append("Sequential characters.")
                break

        # All lower
        elif (a.islower()and b.islower() and c.islower()):
            if (ord(b) - ord(a) == 1 and ord(c) - ord(b) == 1):
                issues.append("Sequential characters.")
                break

            if (ord(b) - ord(a) == -1 and ord(c) - ord(b) == -1):
                issues.append("Sequential characters.")
                break

        # All upper
        elif (a.isupper()and b.isupper() and c.isupper()):
            if (ord(b) - ord(a) == 1 and ord(c) - ord(b) == 1):
                issues.append("Sequential characters.")
                break

            if (ord(b) - ord(a) == -1 and ord(c) - ord(b) == -1):
                issues.append("Sequential characters.")
                break

    return issues


#check common passwords
def is_common(password):
    script_dir = os.path.dirname(__file__)
    file_path  = os.path.join(script_dir, "common_passwords.txt")
    with open(file_path, "r") as file:
        for line in file:
            common_password = line.strip()

            if password.lower() == common_password.lower():
                return True

    return False

#score the password
def score_password(password):
    entropy = calculate_entropy(password)
    patterns = find_patterns(password)

    base_score = min(100, (entropy/60)*100)
    score = base_score
    score -= 15 * len(patterns)

    if is_common(password):
        score = 10

    score = max(0, min(100, score))

    return score


#label the score
def get_strength_label(score):
    if score < 40:
        return "Weak"
    if score < 70:
        return "Medium"
    else:
        return "Strong"


#generate password
def generate_password(length=12):
    if length < 8:
        raise ValueError("Password length must be atleast 8")

    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = string.punctuation

    all_char = lowercase + uppercase + digits + symbols

    password = [
        secrets.choice(lowercase),
        secrets.choice(uppercase),
        secrets.choice(digits),
        secrets.choice(symbols)
    ]

    for _ in range(length - 4):
        password.append(secrets.choice(all_char))

    secrets.SystemRandom().shuffle(password)

    return "".join(password)



if __name__ == "__main__":
    main()
