import argparse
from utlities.Utf8Utils import Utf8Utils
from processors.FileDecryptor import Decryptor

# Test configuration
DEFAULT_INPUT = "test_output.txt"
DEFAULT_OUTPUT = "test_output(D).txt"
DEFAULT_PASSWORD = "123"


def main():
    parser = argparse.ArgumentParser(description="File Encryption Tool")
    parser.add_argument('-i', '--input', default=DEFAULT_INPUT, help="Input file")
    parser.add_argument('-o', '--output', default=DEFAULT_OUTPUT, help="Output file")
    parser.add_argument('-p', '--password', default=DEFAULT_PASSWORD, help="Password")

    args = parser.parse_args()

    password_codepoints = Utf8Utils.convert_to_code_point_list(args.password)

    if not password_codepoints:
        raise ValueError("Password cannot be empty")

    decryptor = Decryptor(password_codepoints)
    decryptor.process_file(args.input, args.output)


if __name__ == "__main__":
    main()