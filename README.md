# Password Strength Checker

## Video URL

https://youtu.be/TBkurlXUnGY?si=MBtGMh2V33Qaw5iC

## Description

Password Strength Checker is a command-line Python application that evaluates the strength of a password and can also generate secure passwords.

The project uses several different checks instead of relying on password length alone. It calculates the estimated entropy of a password, searches for potentially weak patterns such as repeated or sequential characters, checks whether the password appears in a list of common passwords, and combines these results into a score from 0 to 100. The score is then converted into a simple strength label: Weak, Medium, or Strong.

The program has two main modes.

### Audit Mode

Audit mode is the default mode. Running:

    python project.py

prompts the user for a password using Python's `getpass` module. The password is not displayed while it is being entered.

The program then displays information such as:

- Estimated entropy in bits
- Whether the password is found in the common-password list
- Patterns detected in the password
- A score from 0 to 100
- A final strength label

For example, a password containing repeated characters or a sequential pattern can receive deductions from its score.

### Generate Mode

The program can also generate a secure random password:

    python project.py --generate

The default generated password is 12 characters long.

A custom length can be specified using:

    python project.py --generate --length 20

The generated password contains at least one lowercase letter, one uppercase letter, one digit, and one symbol.

### Files

The main files in the project are:

- `project.py` - Contains the main application and all of the password analysis and generation functions.
- `test_project.py` - Contains tests for the functions in `project.py`.
- `common_passwords.txt` - Contains a manually created list of commonly used passwords that is used by `is_common()`.
- `requirements.txt` - Lists the Python packages required by the project, including `pytest` for running the test suite.
- `README.md` - Contains the documentation for the project.

## Testing

The project includes automated tests in `test_project.py` using `pytest`.

To install the required dependency, run:

    pip install -r requirements.txt

To run the test suite, use:

    pytest -q

The tests check the main functionality of the project, including entropy calculation, pattern detection, common-password detection, password scoring, strength labels, and generated password properties such as length and character categories.

## Design Choices

### Entropy, patterns, and common passwords

I decided not to judge a password using only its length or entropy. A password can have a relatively high mathematical entropy while still having characteristics that make it less desirable, such as repeated or sequential characters.

The project therefore uses three different types of checks.

First, `calculate_entropy()` estimates entropy using the password length and the character categories present in it. Lowercase letters, uppercase letters, digits, and symbols contribute to the possible character pool.

Second, `find_patterns()` looks for repeated characters and sequential runs. These checks help identify predictable structures that are not fully represented by the entropy calculation.

Finally, `is_common()` checks the password against a local list of common passwords. This is important because a password can still be a poor choice if it is frequently used.

### Scoring formula

The `score_password()` function combines the results into a score between 0 and 100.

For the entropy portion, I use 60 bits as a practical ceiling:

    base_score = min(100, (entropy / 60) * 100)

This means that 60 bits of entropy corresponds to 100 base points. Entropy above 60 bits does not increase the base score beyond 100.

I subtract 15 points for each pattern detected:

    score -= 15 * len(patterns)

I chose this as a moderate deduction because patterns are a weakness, but they do not necessarily make an otherwise long password completely unusable.

Common passwords are treated differently. If a password is found in `common_passwords.txt`, its score is set to 10. I chose this because being a commonly used password is a significant weakness, regardless of what its mathematical entropy calculation might suggest.

Finally, the score is clamped between 0 and 100 so that deductions cannot produce a negative score.

The resulting score is converted into a label using these ranges:

- 0-39: Weak
- 40-69: Medium
- 70-100: Strong

These values are a scoring model created for this project rather than a universal standard for measuring password security.

### Secure password generation

For password generation, I use Python's `secrets` module instead of the `random` module.

The `random` module is designed primarily for general-purpose pseudo-random operations and is not intended for security-sensitive applications. The `secrets` module is specifically designed for generating cryptographically strong random values.

The generator first selects one character from each of the four required categories: lowercase, uppercase, digit, and symbol. It then fills the remaining positions using the combined character pool.

The characters are shuffled using `secrets.SystemRandom().shuffle()` so that the four guaranteed characters are not always placed at the beginning of the password.

The generator requires a minimum password length of 8 characters. If a shorter length is requested, `generate_password()` raises a `ValueError`, which is handled by `main()` and displayed as a readable error message instead of allowing the program to terminate with an unhandled exception.

### Hidden password input

I use Python's `getpass.getpass()` instead of the normal `input()` function when auditing a password.

With `input()`, the password would be visible on the terminal while the user types it. `getpass` prevents the password from being echoed to the screen, which is more appropriate for sensitive information.

### Common-password file path

The project uses `common_passwords.txt` as an external wordlist. The program needs to be able to find this file regardless of the directory from which the program is executed.

For this reason, I use `os.path` to construct the path relative to the location of `project.py` rather than relying entirely on the current working directory.

This makes the program more reliable when it is run from different locations or when the test suite imports the project.

### Sequential patterns

I define a sequential pattern as three or more consecutive characters that increase or decrease by one position.

Examples include:

- `abc`
- `bcd`
- `123`
- `456`
- `zyx`
- `987`

The check is restricted to characters from the same category. For example, lowercase letters are checked together, uppercase letters are checked together, and digits are checked together.

Mixed patterns such as `Abc` or `a1b` are not considered sequential patterns because they mix character cases or character types.

This keeps the pattern detection simple and makes the definition of a sequential pattern clear and consistent.
