from collections.abc import Iterable


class Decryptor:
    def __init__(self, utf8_values: list[int]):
        if not isinstance(utf8_values, Iterable):
            raise ValueError("Must provide iterable of integers")
        self.utf8_values = utf8_values
        self.big_sum = sum(utf8_values)
        self._validate_utf8_values()

    def _validate_utf8_values(self):
        for val in self.utf8_values:
            if not (0 <= val <= 0x10FFFF):
                raise ValueError(f"Invalid UTF-8 code point: {val}")

    def process_file(self, input_path: str, output_path: str):
        adjusted_sum = self.big_sum
        used_values = set()

        try:
            with open(input_path, 'r', encoding='utf-8') as reader, \
                    open(output_path, 'w', encoding='utf-8') as writer:

                for line in reader:
                    line = line.strip()
                    if '/' not in line:
                        continue  # Skip invalid lines

                    index_str, encrypted_char = line.split('/', 1)

                    try:
                        password_index = int(index_str)
                        password_char = self.utf8_values[password_index]
                    except (ValueError, IndexError):
                        writer.write('\ufffd')  # Replacement char for errors
                        continue

                    if adjusted_sum <= 0:
                        adjusted_sum = self.big_sum
                        used_values.clear()

                    if password_char not in used_values:
                        used_values.add(password_char)
                        adjusted_sum -= password_char

                    try:
                        encrypted_code = ord(encrypted_char)
                        original_code = (encrypted_code - password_char - adjusted_sum) % 0x110000

                        # Handle valid Unicode characters
                        original_char = chr(original_code)
                        original_char.encode('utf-8', errors='strict')
                    except:
                        original_char = '\ufffd'

                    writer.write(original_char)

                print(f"Decrypted values written to file: {output_path}")

        except IOError as e:
            print(f"Error: {str(e)}")
            raise