import os
from collections.abc import Iterable
from utlities.RandomSelector import RandomSelector

class FileProcessor:
    def __init__(self, utf8_values: list[int]):
        if not isinstance(utf8_values, Iterable):
            raise ValueError("Must provide iterable of integers")
        self.utf8_values = utf8_values
        self._validate_utf8_values()

    def _validate_utf8_values(self):
        for val in self.utf8_values:
            if not (0 <= val <= 0x10FFFF):
                raise ValueError(f"Invalid UTF-8 code point: {val}")

    def process_file(self, input_path: str, output_path: str):
        # Verify paths exist
        input_path = os.path.abspath(input_path)
        output_path = os.path.abspath(output_path)

        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        big_sum = sum(self.utf8_values)
        print(f"bigSum: {big_sum}")

        adjusted_sum = big_sum
        used_values = set()

        try:
            with open(input_path, 'r', encoding='utf-8') as reader, \
                    open(output_path, 'w', encoding='utf-8') as writer:

                while True:
                    char = reader.read(1)
                    if not char:
                        break

                    file_char_value = ord(char)

                    if adjusted_sum <= 0:
                        adjusted_sum = big_sum
                        used_values.clear()

                    password_index = RandomSelector.select_gaussian_index(self.utf8_values)
                    password_char_value = self.utf8_values[password_index]

                    if password_char_value not in used_values:
                        used_values.add(password_char_value)
                        adjusted_sum -= password_char_value

                    raw_value = file_char_value + password_char_value + adjusted_sum
                    encrypted_value = raw_value % 0x110000

                    try:
                        encrypted_char = chr(encrypted_value)
                        encrypted_char.encode('utf-8', errors='strict')
                    except (ValueError, UnicodeEncodeError):
                        encrypted_char = '\ufffd'

                    writer.write(f"{password_index}/{encrypted_char}\n")

                print(f"Encrypted values written to file: {output_path}")

        except IOError as e:
            print(f"Error: {str(e)}")
            raise

    def process_bytes(self, data: bytes) -> bytes:
        """Process data in memory from bytes to bytes"""
        # Decode bytes to string for processing
        text = data.decode('utf-8')
        encrypted_text = self.process_string(text)
        return encrypted_text.encode('utf-8')

    def encrypt_string(self, text: str) -> str:
        """Process string in memory and return encrypted result"""
        big_sum = sum(self.utf8_values)
        print(f"bigSum: {big_sum}")

        adjusted_sum = big_sum
        used_values = set()

        output_lines = []

        for char in text:
            if adjusted_sum <= 0:

                adjusted_sum = big_sum
                used_values.clear()

            password_index = RandomSelector.select_gaussian_index(self.utf8_values)
            password_char_value = self.utf8_values[password_index]

            if password_char_value not in used_values:
                used_values.add(password_char_value)
                adjusted_sum -= password_char_value

            file_char_value = ord(char)
            raw_value = file_char_value + password_char_value + adjusted_sum
            encrypted_value = raw_value % 0x110000

            try:
                encrypted_char = chr(encrypted_value)
                # Validate the character can be encoded as UTF-8
                encrypted_char.encode('utf-8', errors='strict')
            except (ValueError, UnicodeEncodeError):
                encrypted_char = '\ufffd'  # Replacement character

            output_lines.append(f"{password_index}/{encrypted_char}")

        return '\n'.join(output_lines)