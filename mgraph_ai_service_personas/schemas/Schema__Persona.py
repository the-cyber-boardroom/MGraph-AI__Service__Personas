from typing                                                             import Dict, List
from osbot_utils.type_safe.Type_Safe                                    import Type_Safe
from osbot_utils.type_safe.primitives.safe_int.Timestamp_Now            import Timestamp_Now
from osbot_utils.type_safe.primitives.safe_str.identifiers.Safe_Id      import Safe_Id
from osbot_utils.type_safe.primitives.safe_str.git.Safe_Str__Version    import Safe_Str__Version
from osbot_utils.type_safe.primitives.safe_str.text.Safe_Str__Text      import Safe_Str__Text
from mgraph_ai_service_personas.schemas.Enum__Expertise_Level           import Enum__Expertise_Level
from mgraph_ai_service_personas.schemas.Safe_Str__Language_Code         import Safe_Str__Language_Code
from mgraph_ai_service_personas.schemas.Schema__Communication_Style     import Schema__Communication_Style


class Schema__Persona(Type_Safe):                                                               # Complete persona definition for translation and response generation

    # Core identification
    id                   : Safe_Id
    name                 : Safe_Str__Text
    role                 : Safe_Id
    description          : Safe_Str__Text

    # Language and localization
    language             : Safe_Str__Language_Code
    locale_context       : Safe_Str__Text                                  # Cultural context notes

    # Knowledge and expertise
    expertise            : Dict[Safe_Id, Enum__Expertise_Level]
    interests            : List[Safe_Id]
    priorities           : List[Safe_Id]

    # Communication preferences
    communication_style  : Schema__Communication_Style
    urgency_preference   : Safe_Id

    # Metadata
    version              : Safe_Str__Version                = None
    created_at           : Timestamp_Now
    updated_at           : Timestamp_Now
    tags                 : List[Safe_Id]

    # Additional context
    background_context   : Safe_Str__Text                                   # Additional background info
    common_terminology   : Dict[Safe_Id, Safe_Str__Text]                    # Domain-specific terms
    avoid_terms          : List[Safe_Id]                                    # Terms to avoid or replace

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.created_at is None:
            self.created_at = Timestamp_Now()

    # todo remove the validation from here that is already provided by the Type_Safe classes and move code from this schema file

    def validate_expertise(self) -> bool:                                                       # Validate expertise configuration
        if not self.expertise:
            return False
        for domain, level in self.expertise.items():
            if not isinstance(level, Enum__Expertise_Level):
                return False
        return True

    def get_primary_expertise_domains(self) -> List[str]:                                       # Get domains where persona has advanced or expert knowledge
        return [domain for domain, level in self.expertise.items()
                      if level in [Enum__Expertise_Level.ADVANCED, Enum__Expertise_Level.EXPERT]]

    def get_knowledge_gaps(self) -> List[str]:                                                  # Get domains where persona has basic or no knowledge
        return [domain for domain, level in self.expertise.items()
                      if level in [Enum__Expertise_Level.NONE, Enum__Expertise_Level.BASIC]]

    def to_prompt_context(self) -> str:                                                         # Convert persona to a context string for LLM prompts
        context_parts = [
            f"Persona: {self.name}",
            f"Role: {self.role}",
            f"Language: {self.language}"
        ]

        if self.description:
            context_parts.append(f"Description: {self.description}")

        expert_domains = self.get_primary_expertise_domains()
        if expert_domains:
            context_parts.append(f"Expert in: {', '.join(expert_domains)}")

        knowledge_gaps = self.get_knowledge_gaps()
        if knowledge_gaps:
            context_parts.append(f"Limited knowledge in: {', '.join(knowledge_gaps)}")

        if self.priorities:
            context_parts.append(f"Priorities: {', '.join(self.priorities)}")

        style = self.communication_style
        context_parts.append(f"Communication: {style.tone.value} tone, {style.detail_level.value} detail")

        if style.style_notes:
            context_parts.append(f"Style notes: {style.style_notes}")

        return "\n".join(context_parts)

    def clone_with_updates(self, **updates) -> 'Schema__Persona':                               # Create a copy of the persona with updates
        current_data               = self.json()
        current_data.update(updates)
        current_data['updated_at'] = Timestamp_Now()
        return Schema__Persona.from_json(current_data)
