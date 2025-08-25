from osbot_utils.type_safe.primitives.safe_str.identifiers.Safe_Id    import Safe_Id
from osbot_utils.type_safe.primitives.safe_str.text.Safe_Str__Text    import Safe_Str__Text
from mgraph_ai_service_personas.schemas.Safe_Str__Language_Code       import Safe_Str__Language_Code
from mgraph_ai_service_personas.schemas.Safe_Str__Content             import Safe_Str__Content
from mgraph_ai_service_personas.schemas.Schema__Response__Base        import Schema__Response__Base


class Schema__Response__Impersonate(Schema__Response__Base):        # Response schema for impersonation (respond as persona) operations
    response      : Safe_Str__Content
    query         : Safe_Str__Content
    persona_id    : Safe_Id
    persona_name  : Safe_Str__Text
    persona_role  : Safe_Id
    language      : Safe_Str__Language_Code
    from_cache    : bool