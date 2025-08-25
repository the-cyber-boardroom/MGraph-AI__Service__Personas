from osbot_utils.type_safe.primitives.safe_str.text.Safe_Str__Text import Safe_Str__Text

TYPE_SAFE_STR__PROMPT__MAX_LENGTH = 20000           # todo: move to global config file

class Safe_Str__Prompt(Safe_Str__Text):             # Safe string type for LLM prompts
    max_length = TYPE_SAFE_STR__PROMPT__MAX_LENGTH