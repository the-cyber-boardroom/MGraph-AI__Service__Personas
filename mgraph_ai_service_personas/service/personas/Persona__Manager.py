from typing                                                        import List, Optional
from osbot_utils.type_safe.Type_Safe                               import Type_Safe
from osbot_utils.type_safe.primitives.safe_int.Timestamp_Now       import Timestamp_Now
from osbot_utils.type_safe.primitives.safe_str.identifiers.Safe_Id import Safe_Id
from mgraph_ai_service_personas.schemas.Enum__Expertise_Level      import Enum__Expertise_Level
from mgraph_ai_service_personas.schemas.Safe_Str__Prompt           import Safe_Str__Prompt
from mgraph_ai_service_personas.schemas.Schema__Persona            import Schema__Persona

# todo: see if we really need this

class Persona__Manager(Type_Safe):      # Manages persona operations and transformations

    def get_primary_expertise_domains(self, persona: Schema__Persona) -> List[Safe_Id]:
        """Get domains where persona has advanced or expert knowledge"""
        return [domain for domain, level in persona.expertise.items()
                if level in [Enum__Expertise_Level.ADVANCED, Enum__Expertise_Level.EXPERT]]

    def get_knowledge_gaps(self, persona: Schema__Persona) -> List[Safe_Id]:
        """Get domains where persona has basic or no knowledge"""
        return [domain for domain, level in persona.expertise.items()
                if level in [Enum__Expertise_Level.NONE, Enum__Expertise_Level.BASIC]]

    def to_prompt_context(self, persona: Schema__Persona) -> Safe_Str__Prompt:
        """Convert persona to a context string for LLM prompts"""
        context_parts = [
            f"Persona: {persona.name}",
            f"Role: {persona.role}",
            f"Language: {persona.language}"
        ]

        if persona.description:
            context_parts.append(f"Description: {persona.description}")

        expert_domains = self.get_primary_expertise_domains(persona)
        if expert_domains:
            context_parts.append(f"Expert in: {', '.join(str(d) for d in expert_domains)}")

        knowledge_gaps = self.get_knowledge_gaps(persona)
        if knowledge_gaps:
            context_parts.append(f"Limited knowledge in: {', '.join(str(d) for d in knowledge_gaps)}")

        if persona.priorities:
            context_parts.append(f"Priorities: {', '.join(str(p) for p in persona.priorities)}")

        style = persona.communication_style
        context_parts.append(f"Communication: {style.tone.value} tone, {style.detail_level.value} detail")

        if style.style_notes:
            context_parts.append(f"Style notes: {style.style_notes}")

        return Safe_Str__Prompt("\n".join(context_parts))

    def clone_with_updates(self, persona : Schema__Persona,
                                **updates
                          ) -> Schema__Persona:
        """Create a copy of the persona with updates"""
        current_data               = persona.json()
        current_data.update(updates)
        current_data['updated_at'] = Timestamp_Now()
        return Schema__Persona.from_json(current_data)

    def validate_expertise(self, persona: Schema__Persona) -> bool:
        """Validate expertise configuration"""
        if not persona.expertise:
            return False
        for domain, level in persona.expertise.items():
            if not isinstance(level, Enum__Expertise_Level):
                return False
        return True