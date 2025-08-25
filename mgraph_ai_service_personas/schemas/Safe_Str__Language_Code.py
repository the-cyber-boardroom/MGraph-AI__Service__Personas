import re
from osbot_utils.type_safe.primitives.safe_str.Safe_Str import Safe_Str

TYPE_SAFE_STR__LANGUAGE_CODE__MAX_LENGTH = 10
TYPE_SAFE_STR__LANGUAGE_CODE__REGEX      = re.compile(r'^[a-z]{2,3}(-[A-Z]{2})?$')

class Safe_Str__Language_Code(Safe_Str):        # Language code validator (e.g., en-US, pt-PT)
    max_length        = TYPE_SAFE_STR__LANGUAGE_CODE__MAX_LENGTH
    regex             = TYPE_SAFE_STR__LANGUAGE_CODE__REGEX
    regex_mode        = 'MATCH'
    strict_validation = True