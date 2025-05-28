import random


class RandomSelector:
    @staticmethod
    def select_gaussian_index(values: list[int]) -> int:
        if not values:
            raise ValueError("Values list cannot be empty")

        mean = (len(values) - 1) / 2.0
        std_dev = len(values) / 4.0

        while True:
            gaussian = random.gauss(mean, std_dev)
            selected_index = int(round(gaussian))
            if 0 <= selected_index < len(values):
                return selected_index