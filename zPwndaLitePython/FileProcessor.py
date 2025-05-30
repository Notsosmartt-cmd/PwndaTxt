import random


class FileProcessor:
    def __init__(self, utf8_values):
        # Convert password characters to Unicode code points
        self.utf8_codepoints = [ord(char) for char in utf8_values]
        self.bigSum = sum(self.utf8_codepoints)
        print(f"bigSum: {self.bigSum}")

    def process_file(self, input_file, output_file):
        adjustedSum = self.bigSum
        usedValues = set()

        try:
            with open(input_file, 'r', encoding='utf-8') as reader, \
                    open(output_file, 'w', encoding='utf-8') as writer:

                while True:
                    char = reader.read(1)
                    if not char:
                        break

                    char_value = ord(char)

                    # Reset when adjustedSum depletes
                    if adjustedSum <= 0:
                        adjustedSum = self.bigSum
                        usedValues.clear()

                    # Get random password character
                    password_index = RandomSelector.select_gaussian_index(len(self.utf8_codepoints))
                    password_char_value = self.utf8_codepoints[password_index]

                    # Deduct first occurrence of password char
                    if password_char_value not in usedValues:
                        usedValues.add(password_char_value)
                        adjustedSum -= password_char_value

                    # Calculate encrypted value with wrapping
                    rawValue = char_value + password_char_value + adjustedSum
                    if rawValue > 0x10FFFF:  # Max Unicode code point
                        encrypted_value = rawValue % 0x110000
                    else:
                        encrypted_value = rawValue

                    # Handle valid/invalid Unicode characters
                    if 0 <= encrypted_value <= 0x10FFFF:
                        try:
                            encrypted_char = chr(encrypted_value)
                        except ValueError:
                            encrypted_char = '\uFFFD'  # Replacement character
                    else:
                        encrypted_char = '\uFFFD'

                    # Write password index and encrypted character
                    writer.write(f"{password_index}/{encrypted_char}\n")

                print(f"Encrypted values written to: {output_file}")

        except IOError as e:
            print(f"Error: {e}")


class RandomSelector:
    @staticmethod
    def select_gaussian_index(length):
        mean = (length - 1) / 2.0
        std_dev = length / 4.0

        while True:
            gaussian = random.gauss(mean, std_dev)
            index = int(round(gaussian))
            if 0 <= index < length:
                return index