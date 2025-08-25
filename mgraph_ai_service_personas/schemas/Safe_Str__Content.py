import re
from osbot_utils.type_safe.primitives.safe_str.text.Safe_Str__Text import Safe_Str__Text

TYPE_SAFE_STR__CONTENT__MAX_LENGTH = 10000          # todo: move to global config file

class Safe_Str__Content(Safe_Str__Text):            # Safe string type for content to be translated or generated
    max_length = TYPE_SAFE_STR__CONTENT__MAX_LENGTH