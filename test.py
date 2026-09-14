import re
import math
import getpass


COMMON_PASSWORDS = {
    "password",
    "password123",
    "123456",
    "12345678",
    "qwerty",
    "qwerty123",
    "admin",
    "letmein",
    "welcome",
    "iloveyou",
}


def calculate_entropy(password):
    """Estimate password entropy in bits."""
    charset = 0

    if re.search(r"[a-z]", password):
        charset += 26
    if re.search(r"[A-Z]", password):
        charset += 26
    if re.search(r"\d", password):
        charset += 10
    if re.search(r"[^A-Za-z0-9]", password):
        charset += 32

    if charset == 0:
        return 0

    return len(password) * math.log2(charset)


def has_repeated_characters(password):
    """Detect the same character repeated 3 or more times."""
    return bool(re.search(r"(.)\1\1", password))


def has_sequential_pattern(password):
    """Detect simple ascending/descending number sequences."""
    sequences = [
        "0123456789",
        "9876543210",
        "abcdefghijklmnopqrstuvwxyz",
        "zyxwvutsrqponmlkjihgfedcba",
    ]

    password_lower = password.lower()

    for sequence in sequences:
        for length in range(3, 5):
            for i in range(len(sequence) - length + 1):
                if sequence[i:i + length] in password_lower:
                    return True

    return False


def check_password(password):
    score = 0
    warnings = []
    suggestions = []

    # Length
    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Use at least 8 characters.")

    if len(password) >= 12:
        score += 1

    if len(password) >= 16:
        score += 1

    # Character variety
    if re.search(r"[a-z]", password):
        score += 1
    else:
        suggestions.append("Add lowercase letters.")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        suggestions.append("Add uppercase letters.")

    if re.search(r"\d", password):
        score += 1
    else:
        suggestions.append("Add numbers.")

    if re.search(r"[^A-Za-z0-9]", password):
        score += 1
    else:
        suggestions.append("Add special characters.")

    # Common password check
    if password.lower() in COMMON_PASSWORDS:
        warnings.append("This is a commonly used password.")
        score = max(0, score - 3)

    # Repeated characters
    if has_repeated_characters(password):
        warnings.append("Avoid repeating the same character 3+ times.")

    # Sequential patterns
    if has_sequential_pattern(password):
        warnings.append("Avoid simple sequential patterns like 1234 or abcd.")

    # Entropy
    entropy = calculate_entropy(password)

    if entropy < 40:
        entropy_level = "Low"
    elif entropy < 60:
        entropy_level = "Moderate"
    elif entropy < 80:
        entropy_level = "Good"
    else:
        entropy_level = "High"

    # Final strength
    if score <= 3:
        strength = "Weak"
    elif score <= 5:
        strength = "Medium"
    else:
        strength = "Strong"

    return strength, score, entropy, entropy_level, warnings, suggestions


def main():
    print("=" * 45)
    print("       PASSWORD STRENGTH CHECKER v2")
    print("=" * 45)

    password = getpass.getpass("Enter password: ")

    if not password:
        print("\nPassword cannot be empty.")
        return

    (
        strength,
        score,
        entropy,
        entropy_level,
        warnings,
        suggestions,
    ) = check_password(password)

    print("\nResult")
    print("-" * 45)
    print(f"Strength : {strength}")
    print(f"Score    : {score}/7")
    print(f"Entropy  : {entropy:.1f} bits ({entropy_level})")

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"  ! {warning}")

    if suggestions:
        print("\nSuggestions:")
        for suggestion in suggestions:
            print(f"  - {suggestion}")

    if not warnings and not suggestions:
        print("\nYour password passes all basic checks.")


if __name__ == "__main__":
    main()