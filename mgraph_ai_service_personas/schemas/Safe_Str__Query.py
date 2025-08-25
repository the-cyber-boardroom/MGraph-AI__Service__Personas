import re
from osbot_utils.type_safe.primitives.safe_str.Safe_Str import Safe_Str

TYPE_SAFE_STR__QUERY__MAX_LENGTH = 5000                     # todo: move to global config file

class Safe_Str__Query(Safe_Str):                            # Safe string type for user queries/questions
    max_length       = TYPE_SAFE_STR__QUERY__MAX_LENGTH