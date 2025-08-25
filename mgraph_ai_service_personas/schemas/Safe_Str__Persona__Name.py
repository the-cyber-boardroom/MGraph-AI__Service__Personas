import re
from osbot_utils.type_safe.primitives.safe_str.Safe_Str import Safe_Str

TYPE_SAFE_STR__PERSONA__NAME__MAX_LENGTH = 64
TYPE_SAFE_STR__PERSONA__NAME__REGEX      = r'[^a-zA-Z0-9-_ ()]'

class Safe_Str__Text(Safe_Str):
    regex      = re.compile(TYPE_SAFE_STR__PERSONA__NAME__REGEX)
    max_length = TYPE_SAFE_STR__PERSONA__NAME__MAX_LENGTH