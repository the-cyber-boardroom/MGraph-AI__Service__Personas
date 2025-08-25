from typing                                                           import Literal, Optional
from osbot_utils.type_safe.Type_Safe                                  import Type_Safe
from osbot_utils.type_safe.primitives.safe_int.Timestamp_Now          import Timestamp_Now
from osbot_utils.type_safe.primitives.safe_str.text.Safe_Str__Text    import Safe_Str__Text

class Schema__Response__Base(Type_Safe):            # Base response schema for all API responses
    status    : Literal["success", "error"]
    message   : Optional[Safe_Str__Text]
    timestamp : Timestamp_Now