import argparse
from Utf8Utils import Utf8Utils
from processors.FileEncryptor import FileProcessor

# Test configuration
DEFAULT_INPUT = "test.txt"
DEFAULT_OUTPUT = "test_output.txt"
DEFAULT_PASSWORD = "my_test_password"


def main():
    parser = argparse.ArgumentParser(description="File Encryption Tool")
    parser.add_argument('-i', '--input', default=DEFAULT_INPUT, help="Input file")
    parser.add_argument('-o', '--output', default=DEFAULT_OUTPUT, help="Output file")
    parser.add_argument('-p', '--password', default=DEFAULT_PASSWORD, help="Password")

    args = parser.parse_args()

    password_codepoints = Utf8Utils.convert_to_code_point_list(args.password)

    if not password_codepoints:
        raise ValueError("Password cannot be empty")

    processor = FileProcessor(password_codepoints)
    processor.process_file(args.input, args.output)


if __name__ == "__main__":
    main()