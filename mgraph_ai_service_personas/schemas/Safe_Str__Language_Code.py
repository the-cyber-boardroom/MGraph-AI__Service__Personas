import re
from osbot_utils.type_safe.Type_Safe__Primitive import Type_Safe__Primitive

TYPE_SAFE_STR__LANGUAGE_CODE__MAX_LENGTH = 10
TYPE_SAFE_STR__LANGUAGE_CODE__REGEX      = re.compile(r'^[a-z]{2,3}(-[A-Z]{2})?$')

class Safe_Str__Language_Code(Type_Safe__Primitive, str):                       # Language code validator (e.g., en-US, pt-PT)

    def __new__(cls, value: str = None):
        if value is not None:                                                   # Check that it is not None
            value = value.strip()                                               # Trim/strip whitespace

        if not value:                                                           # Allow empty values
            return str.__new__(cls, "")

        if not TYPE_SAFE_STR__LANGUAGE_CODE__REGEX.match(value):                # Validate language code format
            raise ValueError(f"Invalid language code format: '{value}'. Expected format like 'en', 'en-US', or 'pt-PT'")

        if len(value) > TYPE_SAFE_STR__LANGUAGE_CODE__MAX_LENGTH:               # Check length constraint
            raise ValueError(f"Language code '{value}' exceeds maximum length of {TYPE_SAFE_STR__LANGUAGE_CODE__MAX_LENGTH}")

        return str.__new__(cls, value)

    def __add__(self, other):                                                   # Concatenation returns regular str, not Safe_Str__Language_Code
        return str.__add__(self, other)

    def __radd__(self, other):                                                  # Reverse concatenation also returns regular str
        return str.__add__(other, self)