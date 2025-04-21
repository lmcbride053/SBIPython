"""
scoring.py

Implements heuristic scoring rules for ranking potential ligand-binding pockets 
based on geometric criteria such as volume, depth, enclosure, and curvature.

Usage:
    python Scoring.py <input_pockets.json> <output_scored_pockets.json>

Inputs:
    - input_pockets.json: JSON file with a list of pocket dicts, each containing:
        {
            'volume': float,
            'depth': float,
            'enclosure': float,
            'curvature': float
        }

Outputs:
    - output_scored_pockets.json: Same as input, with an added 'score' field and sorted by score.
"""

import sys
import json

def score_pocket(pocket):
    """
    Scores a pocket based on its geometric properties.

    Parameters:
    - pocket (dict): A dictionary with geometric properties:
        {
            'volume': float,
            'depth': float,
            'enclosure': float,  # 0 to 1 (1 = fully enclosed)
            'curvature': float,  # avg negative curvature preferred
        }

    Returns:
    - int: Heuristic score (higher = more likely to bind ligand)
    """
    score = 0

    # Volume scoring
    if pocket['volume'] > 800:
        score += 2
    elif pocket['volume'] > 300:
        score += 1

    # Depth scoring
    if pocket['depth'] > 10:
        score += 2
    elif pocket['depth'] > 5:
        score += 1

    # Enclosure scoring
    if pocket['enclosure'] > 0.7:
        score += 2
    elif pocket['enclosure'] > 0.4:
        score += 1

    # Curvature (negative = concave, desirable)
    if pocket['curvature'] < -0.3:
        score += 2
    elif pocket['curvature'] < -0.1:
        score += 1

    return score


def rank_pockets(pockets):
    """
    Ranks a list of pockets by their heuristic scores.

    Parameters:
    - pockets (list): List of dicts, each representing a pocket.

    Returns:
    - List of dicts, each with an added 'score' field, sorted by score descending.
    """
    for pocket in pockets:
        pocket['score'] = score_pocket(pocket)
    return sorted(pockets, key=lambda p: p['score'], reverse=True)


def main(input_file, output_file):
    with open(input_file, 'r') as f:
        pockets = json.load(f)

    ranked = rank_pockets(pockets)

    with open(output_file, 'w') as f:
        json.dump(ranked, f, indent=4)

    print(f"Scored pockets written to {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    main(input_file, output_file)
