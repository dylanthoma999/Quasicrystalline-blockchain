import math


def compute_reputation_score(compliance, performance, availability, settlement):
    """Simple weighted reputation score for institutional participants."""
    return 0.35 * compliance + 0.25 * performance + 0.20 * availability + 0.20 * settlement


def weighted_validation_score(reputation_score, volume):
    """Maps a reputation score and transaction volume into a trust-weighted score."""
    return reputation_score * math.log1p(volume)


if __name__ == "__main__":
    participants = {
        "Bank_A": (0.95, 0.90, 0.92, 0.91),
        "Bank_B": (0.88, 0.85, 0.87, 0.84),
        "Custodian_C": (0.91, 0.89, 0.90, 0.88),
    }

    for name, values in participants.items():
        score = compute_reputation_score(*values)
        validation = weighted_validation_score(score, 120)
        print(f"{name}: reputation={score:.3f}, trust_weighted_validation={validation:.3f}")
