from osbot_utils.type_safe.primitives.safe_str.identifiers.Safe_Id    import Safe_Id
from osbot_utils.type_safe.primitives.safe_str.text.Safe_Str__Text    import Safe_Str__Text
from mgraph_ai_service_personas.schemas.Safe_Str__Language_Code       import Safe_Str__Language_Code
from mgraph_ai_service_personas.schemas.Safe_Str__Content             import Safe_Str__Content
from mgraph_ai_service_personas.schemas.Schema__Response__Base        import Schema__Response__Base


class Schema__Response__Translate(Schema__Response__Base):              # Response schema for translation operations"""
    translated_content : Safe_Str__Content
    original_content   : Safe_Str__Content
    persona_id         : Safe_Id
    persona_name       : Safe_Str__Text
    language           : Safe_Str__Language_Code
    from_cache         : bool