from typing                                                         import Literal
from osbot_utils.type_safe.primitives.safe_str.identifiers.Safe_Id  import Safe_Id
from osbot_utils.type_safe.primitives.safe_uint.Safe_UInt           import Safe_UInt
from mgraph_ai_service_personas.schemas.Safe_Str__Content           import Safe_Str__Content
from mgraph_ai_service_personas.schemas.Schema__Response__Base      import Schema__Response__Base

class Schema__LLM__Response(Schema__Response__Base):            # Response from LLM service"""
    content         : Safe_Str__Content
    model_used      : Safe_Id
    tokens_used     : Safe_UInt
    response_format : Literal["text", "json"]