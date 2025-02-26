import math


def normal_cdf(x, mean, std_dev):
    """Computes the cumulative distribution function (CDF) for a normal distribution."""
    z = (x - mean) / std_dev
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def edge_probability(size, std_dev):
    mean = (size - 1) / 2  # Center index of the list
    left_edge_prob = normal_cdf(0, mean, std_dev)  # Probability of selecting index 0
    right_edge_prob = 1 - normal_cdf(size - 1, mean, std_dev)  # Probability of selecting last index

    return (left_edge_prob + right_edge_prob) * 100  # Convert to percentage


size = 512  # List size
std_dev = (size * 0.25)  # Standard deviation

print(f"Probability of selecting an edge (0 or {size - 1}): {edge_probability(size, std_dev):.4f}%")
