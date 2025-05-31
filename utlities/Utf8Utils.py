class Utf8Utils:
    @staticmethod
    def convert_to_code_point_list(input_str: str) -> list[int]:
        return [ord(char) for char in input_str]