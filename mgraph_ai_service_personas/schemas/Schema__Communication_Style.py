from typing                                                         import Optional
from osbot_utils.type_safe.Type_Safe                                import Type_Safe
from osbot_utils.type_safe.primitives.safe_str.text.Safe_Str__Text  import Safe_Str__Text
from osbot_utils.type_safe.primitives.safe_uint.Safe_UInt           import Safe_UInt
from mgraph_ai_service_personas.schemas.Enum__Communication_Tone    import Enum__Communication_Tone
from mgraph_ai_service_personas.schemas.Enum__Detail_Level          import Enum__Detail_Level


class Schema__Communication_Style(Type_Safe):                                                               # Communication style preferences for a persona
    tone                  : Enum__Communication_Tone  = Enum__Communication_Tone.PROFESSIONAL
    detail_level          : Enum__Detail_Level        = Enum__Detail_Level.MODERATE
    style_notes           : Optional[Safe_Str__Text]        = None                                        # Additional style guidance
    prefers_examples      : bool                      = False
    prefers_analogies     : bool                      = False
    prefers_bullet_points : bool                      = False
    max_response_length   : Safe_UInt                 = None                                        # Approximate word count