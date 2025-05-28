import random
class FileProcessor:
    def __init__(self, utf8_values):
        self.utf8_values = utf8_values  # List of characters (e.g., ['a', 'b', 'c']

    def process_file(self, input_file, output_file):
        try:
            with open(input_file, 'r', encoding='utf-8') as reader, \
                    open(output_file, 'w', encoding='utf-8') as writer:
                while True:
                    char = reader.read(1)  # Read one character at a time
                    if not char:  # End of file
                        break
                    char_value = ord(char)  # Convert character to Unicode code point

                    # Get random index, password char, and salt
                    password_index = RandomSelector.select_gaussian_index(self.utf8_values)
                    password_char = ord(self.utf8_values[password_index])
                    salt = ord(self.utf8_values[-1])  # Last element as salt

                    # Encrypt and write to file
                    encrypted_value = char_value + password_char + salt
                    encrypted_char = chr(encrypted_value)
                    writer.write(f"{password_index}/{encrypted_char}\n")

                print(f"Encrypted values written to: {output_file}")

        except IOError as e:
            print(f"Error: {e}")


class Utf8Utils:
    @staticmethod
    def convert_to_character_list(password):
        return list(password)  # Convert string to list of characters


class RandomSelector:
    @staticmethod
    def select_gaussian_index(values):
        mean = (len(values) - 1) / 2.0
        std_dev = len(values) / 4.0
        selected_index = -1

        while True:
            # Generate Gaussian-distributed index (not cryptographically secure)
            gaussian = random.gauss(mean, std_dev)
            selected_index = int(round(gaussian))
            if 0 <= selected_index < len(values):
                break

        return selected_index