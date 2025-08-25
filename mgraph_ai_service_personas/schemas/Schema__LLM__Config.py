from typing                                                                    import Optional, Literal
from osbot_utils.type_safe.Type_Safe                                           import Type_Safe
from osbot_utils.type_safe.primitives.safe_float.Safe_Float__Percentage_Exact  import Safe_Float__Percentage_Exact
from osbot_utils.type_safe.primitives.safe_str.identifiers.Safe_Id             import Safe_Id
from osbot_utils.type_safe.primitives.safe_str.web.Safe_Str__Url               import Safe_Str__Url
from mgraph_ai_service_personas.schemas.Safe_Float__Temperature                import Safe_Float__Temperature
from mgraph_ai_service_personas.schemas.Safe_UInt__Tokens                      import Safe_UInt__Tokens

class Schema__LLM__Config(Type_Safe):                   # Configuration for LLM service calls
    service_url     : Safe_Str__Url
    model           : Safe_Id
    temperature     : Safe_Float__Temperature
    max_tokens      : Safe_UInt__Tokens
    response_format : Optional[Literal["text", "json"]]
    top_p           : Optional[Safe_Float__Percentage_Exact]
    frequency_penalty: Optional[Safe_Float__Percentage_Exact]
    presence_penalty : Optional[Safe_Float__Percentage_Exact]