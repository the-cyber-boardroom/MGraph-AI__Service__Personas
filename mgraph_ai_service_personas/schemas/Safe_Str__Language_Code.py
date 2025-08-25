from osbot_utils.type_safe.primitives.safe_str.Safe_Str import Safe_Str

# todo: fix this method since the validate doesn't exist
class Safe_Str__Language_Code(Safe_Str):                                                        # Language code validator (e.g., en-US, pt-PT)
    max_length = 10

    def validate(self) -> bool:
        if not super().validate():
            return False
        parts = self.value.split('-')                                                           # Basic validation for language-region format
        if len(parts) not in [1, 2]:
            return False
        if len(parts[0]) not in [2, 3]:                                                         # ISO 639-1 or 639-2
            return False
        return True