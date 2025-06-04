import os
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

    def decrypt_file_to_string(self, input_path: str) -> str:
        """
        Reads an encrypted file and returns the decrypted content as a string
        """
        # Verify input file exists
        input_path = os.path.abspath(input_path)
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

        adjusted_sum = self.big_sum
        used_values = set()
        decrypted_chars = []

        try:
            with open(input_path, 'r', encoding='utf-8') as reader:
                for line in reader:
                    line = line.strip()
                    if not line or '/' not in line:
                        continue  # Skip empty or invalid lines

                    # Split into index and encrypted character
                    parts = line.split('/', 1)
                    index_str = parts[0].strip()
                    encrypted_char = parts[1].strip()

                    # Skip lines without both components
                    if not index_str or not encrypted_char:
                        continue

                    try:
                        # Get password character using index
                        password_index = int(index_str)
                        password_char = self.utf8_values[password_index]
                    except (ValueError, IndexError):
                        # Invalid index - use replacement character
                        decrypted_chars.append('\ufffd')
                        continue

                    # Reset adjustment sum when depleted
                    if adjusted_sum <= 0:
                        adjusted_sum = self.big_sum
                        used_values.clear()

                    # Track used values and adjust sum
                    if password_char not in used_values:
                        used_values.add(password_char)
                        adjusted_sum -= password_char

                    # Decrypt the character
                    try:
                        encrypted_code = ord(encrypted_char)
                        # Reverse the encryption calculation
                        original_code = (encrypted_code - password_char - adjusted_sum) % 0x110000
                        original_char = chr(original_code)

                        # Validate it's a proper UTF-8 character
                        original_char.encode('utf-8', errors='strict')
                    except (ValueError, UnicodeEncodeError):
                        original_char = '\ufffd'  # Replacement character

                    decrypted_chars.append(original_char)

            return ''.join(decrypted_chars)

        except IOError as e:
            raise IOError(f"Error reading file: {str(e)}")

    def decrypt_string(self, encrypted_content: str) -> str:
        """
        Decrypts a string in memory using the same algorithm as process_file
        Returns decrypted plain text
        """
        adjusted_sum = self.big_sum
        used_values = set()
        decrypted_chars = []

        lines = encrypted_content.split('\n')

        for line in lines:
            line = line.strip()
            if not line or '/' not in line:
                continue  # Skip empty or invalid lines

            # Split into index and encrypted character
            parts = line.split('/', 1)
            index_str = parts[0].strip()
            encrypted_char = parts[1].strip()

            # Skip lines without both components
            if not index_str or not encrypted_char:
                continue

            try:
                # Get password character using index
                password_index = int(index_str)
                password_char = self.utf8_values[password_index]
            except (ValueError, IndexError):
                # Invalid index - use replacement character
                decrypted_chars.append('\ufffd')
                continue

            # Reset adjustment sum when depleted
            if adjusted_sum <= 0:
                adjusted_sum = self.big_sum
                used_values.clear()

            # Track used values and adjust sum
            if password_char not in used_values:
                used_values.add(password_char)
                adjusted_sum -= password_char

            # Decrypt the character
            try:
                encrypted_code = ord(encrypted_char)
                # Reverse the encryption calculation
                original_code = (encrypted_code - password_char - adjusted_sum) % 0x110000
                original_char = chr(original_code)

                # Validate it's a proper UTF-8 character
                original_char.encode('utf-8', errors='strict')
            except (ValueError, UnicodeEncodeError):
                original_char = '\ufffd'  # Replacement character

            decrypted_chars.append(original_char)

        return ''.join(decrypted_chars)

