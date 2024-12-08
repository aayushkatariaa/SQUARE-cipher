import csv
import numpy as np
# Load DDT from a CSV file
def load_ddt(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        ddt = []
        for row in reader:
            ddt.append([int(value) for value in row])
    ddt = np.array(ddt)
    
    # Drop the first row as it contains numbering)
    ddt = ddt[1:, :]  
    return ddt


def compute_differential_probability(trail, ddt):
    """
    Computes the probability of a differential trail based on the DDT.
    :param trail: List of (input_diff, output_diff) tuples for each round.
    :param ddt: Differential Distribution Table as a numpy array.
    :return: Probability of the trail.
    """
    probability = 1.0
    for input_diff, output_diff in trail:
        count = ddt[input_diff, output_diff]
        if count == 0:
            return 0  # Trail is impossible
        probability *= count / np.sum(ddt[input_diff])  # Normalize counts to probabilities
    return probability

# Analyze differential trails
def analyze_trail(input_diff, output_diffs, ddt, num_rounds):
    """
    Analyzes potential differential trails for a cipher.
    :param input_diff: Starting input difference.
    :param output_diffs: Possible output differences for each round.
    :param ddt: Differential Distribution Table as a numpy array.
    :param num_rounds: Number of cipher rounds.
    :return: List of probable differential trails.
    """
    trails = []
    def recursive_trail(round_idx, current_trail, current_prob):
        if round_idx == num_rounds:
            trails.append((current_trail, current_prob))
            # if current_prob>2.9802322387695312e-08: change this probability to filter out the trails with higher probabilities
            print(current_trail,',',current_prob)
            return
        for next_output_diff in output_diffs:
            count = ddt[current_trail[-1][1], next_output_diff]
            if count > 0:
                next_prob = count / np.sum(ddt[current_trail[-1][1]])
                recursive_trail(round_idx + 1, 
                                current_trail + [(current_trail[-1][1], next_output_diff)], 
                                current_prob * next_prob)
    # Start with the initial input difference
    for first_output_diff in output_diffs:
        count = ddt[input_diff, first_output_diff]
        if count >0:
            prob = count / np.sum(ddt[input_diff])
            recursive_trail(1, [(input_diff, first_output_diff)], prob)
    return trails

if __name__ == "__main__":
    ddt_path = "ddt_table.csv"  
    ddt = load_ddt(ddt_path)

    ddt.shape #check shape of ddt table

    input_diff = 0x2  # Example input difference
    output_diffs = list(range(len(ddt)))  # Possible output differences
    num_rounds = 4  # Number of rounds to analyze as per SQUARE research paper

    # Analyze trails
    trails = analyze_trail(input_diff, output_diffs, ddt, num_rounds)

    # Print results
    print(f"Analysis for Input Difference: {input_diff}")
    for trail, probability in trails:
        print(f"Trail: {trail} -> Probability: {probability:.10f}")
    #Aayush k 12140010