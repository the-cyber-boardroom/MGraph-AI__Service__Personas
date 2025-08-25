from typing                                                             import Dict, List, Optional
from osbot_utils.type_safe.Type_Safe                                    import Type_Safe
from osbot_utils.type_safe.primitives.safe_int.Timestamp_Now            import Timestamp_Now
from osbot_utils.type_safe.primitives.safe_str.identifiers.Safe_Id      import Safe_Id
from osbot_utils.type_safe.primitives.safe_str.git.Safe_Str__Version    import Safe_Str__Version
from osbot_utils.type_safe.primitives.safe_str.text.Safe_Str__Text      import Safe_Str__Text
from mgraph_ai_service_personas.schemas.Enum__Expertise_Level           import Enum__Expertise_Level
from mgraph_ai_service_personas.schemas.Safe_Str__Language_Code         import Safe_Str__Language_Code
from mgraph_ai_service_personas.schemas.Schema__Communication_Style     import Schema__Communication_Style

class Schema__Persona(Type_Safe):       # Complete persona definition for translation and response generation

    # Core identification
    id                   : Safe_Id
    name                 : Safe_Str__Text
    role                 : Safe_Id
    description          : Safe_Str__Text

    # Language and localization
    language             : Safe_Str__Language_Code
    locale_context       : Optional[Safe_Str__Text]

    # Knowledge and expertise
    expertise            : Dict[Safe_Id, Enum__Expertise_Level]
    interests            : List[Safe_Id]
    priorities           : List[Safe_Id]

    # Communication preferences
    communication_style  : Schema__Communication_Style
    urgency_preference   : Optional[Safe_Id]

    # Metadata
    version              : Optional[Safe_Str__Version]
    created_at           : Timestamp_Now
    updated_at           : Timestamp_Now
    tags                 : List[Safe_Id]

    # Additional context
    background_context   : Optional[Safe_Str__Text]
    common_terminology   : Dict[Safe_Id, Safe_Str__Text]
    avoid_terms          : List[Safe_Id]