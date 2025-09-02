import re

import pytest
from unittest                                                             import TestCase
from osbot_utils.type_safe.Type_Safe                                      import Type_Safe
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict     import Type_Safe__Dict
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List     import Type_Safe__List
from osbot_utils.utils.Objects                                            import base_classes, __
from osbot_utils.type_safe.primitives.safe_str.identifiers.Safe_Id        import Safe_Id
from osbot_utils.type_safe.primitives.safe_str.text.Safe_Str__Text        import Safe_Str__Text
from osbot_utils.type_safe.primitives.safe_int.Timestamp_Now              import Timestamp_Now
from mgraph_ai_service_personas.schemas.Enum__Expertise_Level             import Enum__Expertise_Level
from mgraph_ai_service_personas.schemas.Enum__Communication_Tone          import Enum__Communication_Tone
from mgraph_ai_service_personas.schemas.Enum__Detail_Level                import Enum__Detail_Level
from mgraph_ai_service_personas.schemas.Safe_Str__Language_Code           import Safe_Str__Language_Code
from mgraph_ai_service_personas.schemas.Schema__Communication_Style       import Schema__Communication_Style
from mgraph_ai_service_personas.schemas.Schema__Persona                   import Schema__Persona


class test_Schema__Persona(TestCase):

    def test__init__(self):                                                # Test auto-initialization of Schema__Persona
        with Schema__Persona() as _:
            assert type(_)                      is Schema__Persona
            assert base_classes(_)              == [Type_Safe, object]

            assert type(_.id)                   is Safe_Id                  # Field type initialization - collections are Type_Safe variants
            assert type(_.name)                 is Safe_Str__Text
            assert type(_.role)                 is Safe_Id
            assert type(_.description)          is Safe_Str__Text
            assert type(_.language)             is Safe_Str__Language_Code
            assert type(_.locale_context)       is Safe_Str__Text
            assert type(_.expertise)            is Type_Safe__Dict          # dict -> Type_Safe__Dict
            assert type(_.interests)            is Type_Safe__List          # list -> Type_Safe__List
            assert type(_.priorities)           is Type_Safe__List          # list -> Type_Safe__List
            assert type(_.communication_style)  is Schema__Communication_Style
            assert type(_.urgency_preference)   is Safe_Id
            assert type(_.version)              is type(None)
            assert type(_.created_at)           is Timestamp_Now
            assert type(_.updated_at)           is Timestamp_Now
            assert type(_.tags)                 is Type_Safe__List          # list -> Type_Safe__List
            assert type(_.background_context)   is Safe_Str__Text
            assert type(_.common_terminology)   is Type_Safe__Dict          # dict -> Type_Safe__Dict
            assert type(_.avoid_terms)          is Type_Safe__List          # list -> Type_Safe__List

    def test__init__with_values(self):                                      # Test initialization with specific values
        test_id        = Safe_Id("test-persona-1")
        test_name      = Safe_Str__Text("Test Persona")
        test_role      = Safe_Id("ciso")
        test_desc      = Safe_Str__Text("Test CISO persona")
        test_lang      = Safe_Str__Language_Code("pt-PT")
        test_expertise = {Safe_Id("cybersecurity"): Enum__Expertise_Level.EXPERT,
                          Safe_Id("finance")      : Enum__Expertise_Level.BASIC }

        with Schema__Persona(id          = test_id,
                             name        = test_name,
                             role        = test_role,
                             description = test_desc,
                             language    = test_lang,
                             expertise   = test_expertise) as _:

            # Direct value checks for non-collections
            assert _.id          == test_id
            assert _.name        == test_name
            assert _.role        == test_role
            assert _.description == test_desc
            assert _.language    == test_lang

            # Expertise becomes a Type_Safe__Dict but preserves content
            assert type(_.expertise) is Type_Safe__Dict
            assert _.expertise[Safe_Id("cybersecurity")] == Enum__Expertise_Level.EXPERT
            assert _.expertise[Safe_Id("finance")]       == Enum__Expertise_Level.BASIC

            # Defaults for collections (Type_Safe variants)
            assert type(_.interests)   is Type_Safe__List
            assert type(_.priorities)  is Type_Safe__List
            assert type(_.tags)        is Type_Safe__List
            assert _.interests         == []
            assert _.priorities        == []
            assert _.tags              == []

    def test_type_enforcement(self):                                        # Test runtime type checking
        with Schema__Persona() as _:
            # Valid assignments
            _.id   = Safe_Id("valid-id")
            _.name = Safe_Str__Text("Valid Name")


            _.id = "raw-string!@£"
            assert _.id == Safe_Id('raw-string___')                     # we can confirm with the type
            assert _.id == 'raw-string___'                              # but due to the automapping, direct strings also work
            _.name = 123
            assert _.name == '123'
            _.language = "en-US"
            assert _.language == Safe_Str__Language_Code('en-US')
            with pytest.raises(ValueError, match=re.escape("Invalid language code format: 'en-USAAAA'. Expected format like 'en', 'en-US', or 'pt-PT'")):
                _.language = "en-USAAAA"

            # Invalid assignments should raise TypeError
            # with pytest.raises(TypeError):
            #     _.id = "raw-string"                                         # Must be Safe_Id

            # with pytest.raises(TypeError):
            #     _.name = 123                                                # Must be Safe_Str__Text

            # with pytest.raises(TypeError):
            #     _.language = "en-US"                                        # Must be Safe_Str__Language_Code

    def test_serialization_round_trip(self):                                # Test JSON serialization preserves types
        with Schema__Persona(id          = Safe_Id("test-123"),
                             name        = Safe_Str__Text("Test User"),
                             role        = Safe_Id("engineer"),
                             description = Safe_Str__Text("A test engineer"),
                             language    = Safe_Str__Language_Code("en-US"),
                             expertise   = {Safe_Id("python"): Enum__Expertise_Level.EXPERT},
                             interests   = [Safe_Id("coding"), Safe_Id("testing")],
                             # keep priorities default (Type_Safe__Dict) to avoid schema mismatch
                             ) as original:

            json_data = original.json()                                     # Serialize
            with Schema__Persona.from_json(json_data) as restored:          # Deserialize

                # Prefer complete object comparison for fidelity
                assert restored.obj() == original.obj()

                # Spot-check key type preservation
                assert type(restored.id        ) is Safe_Id
                assert type(restored.name      ) is Safe_Str__Text
                assert type(restored.language  ) is Safe_Str__Language_Code
                assert type(restored.interests ) is Type_Safe__List
                assert type(restored.expertise ) is Type_Safe__Dict
                assert type(restored.priorities) is Type_Safe__List

    def test_communication_style_initialization(self):                      # Test nested Schema__Communication_Style initialization
        with Schema__Persona() as _:
            # Auto-initialized nested schema and defaults
            assert type(_.communication_style)            is Schema__Communication_Style
            assert _.communication_style.tone             == Enum__Communication_Tone.PROFESSIONAL
            assert _.communication_style.detail_level     == Enum__Detail_Level.MODERATE
            assert _.communication_style.prefers_examples is False

            # Customization
            _.communication_style.tone                   = Enum__Communication_Tone.CASUAL
            _.communication_style.prefers_bullet_points  = True

            assert _.communication_style.tone                  == Enum__Communication_Tone.CASUAL
            assert _.communication_style.prefers_bullet_points is True

    def test_no_shared_mutable_state(self):                                  # Verify each instance has its own collections
        with Schema__Persona() as persona1:
            with Schema__Persona() as persona2:
                persona1.interests.append(Safe_Id("test-interest"))
                persona1.expertise[Safe_Id("domain")] = Enum__Expertise_Level.EXPERT

                assert persona2.interests == []                               # No shared state
                assert persona2.expertise == {}                               # No shared state

                assert len(persona1.interests) == 1
                assert len(persona1.expertise) == 1


    def test__regression__in__Safe_Str__Language_Code(self):                                      # Test initialization with specific values
        test_id        = "test-persona-1"
        test_name      = "Test Persona"
        test_role      = "ciso"
        test_desc      = "Test CISO persona"
        test_lang      = "pt-PT"
        test_expertise = { "cybersecurity": Enum__Expertise_Level.EXPERT,
                           "finance"      : Enum__Expertise_Level.BASIC }

        with Schema__Persona(id          = test_id,
                             name        = test_name,
                             role        = test_role,
                             description = test_desc,
                             language    = test_lang,
                             expertise   = test_expertise) as _:

            # Direct value checks for non-collections
            assert _.id          == test_id
            assert _.name        == test_name
            assert _.role        == test_role
            assert _.description == test_desc
            assert _.language    == 'pt-PT'                 # FIXED : BUG, should be "pt-PT"

            assert _.obj().contains( __(id         = 'test-persona-1'                                ,
                                       name        = 'Test Persona'                                  ,
                                       role        = 'ciso'                                          ,
                                       description ='Test CISO persona'                              ,
                                       language    = 'pt-PT'                                         ,
                                       expertise   = __(cybersecurity = Enum__Expertise_Level.EXPERT ,
                                                        finance       = Enum__Expertise_Level.BASIC)))
