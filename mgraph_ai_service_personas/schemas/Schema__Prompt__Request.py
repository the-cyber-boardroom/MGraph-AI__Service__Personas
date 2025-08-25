from typing                                                          import Optional
from osbot_utils.type_safe.Type_Safe                                 import Type_Safe
from mgraph_ai_service_personas.schemas.Safe_Str__Language_Code      import Safe_Str__Language_Code
from mgraph_ai_service_personas.schemas.Safe_Str__Prompt             import Safe_Str__Prompt
from mgraph_ai_service_personas.schemas.Schema__LLM__Config          import Safe_UInt__Tokens

class Schema__Prompt__Request(Type_Safe):       # Schema for LLM prompt requests
    system_prompt : Safe_Str__Prompt
    user_prompt   : Safe_Str__Prompt
    language      : Optional[Safe_Str__Language_Code]
    max_tokens    : Optional[Safe_UInt__Tokens]