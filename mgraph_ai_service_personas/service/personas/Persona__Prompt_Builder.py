from typing                                                         import Optional
from osbot_utils.type_safe.Type_Safe                                import Type_Safe
from mgraph_ai_service_personas.prompts.Prompts__Persona            import Prompts__Persona
from mgraph_ai_service_personas.schemas.Safe_Str__Content           import Safe_Str__Content
from mgraph_ai_service_personas.schemas.Safe_Str__Persona__Name     import Safe_Str__Text
from mgraph_ai_service_personas.schemas.Safe_Str__Prompt            import Safe_Str__Prompt
from mgraph_ai_service_personas.schemas.Safe_Str__Query             import Safe_Str__Query
from mgraph_ai_service_personas.schemas.Schema__Persona             import Schema__Persona
from mgraph_ai_service_personas.schemas.Schema__Prompt__Request     import Schema__Prompt__Request
from mgraph_ai_service_personas.service.personas.Persona__Manager   import Persona__Manager


class Persona__Prompt_Builder(Type_Safe):           # Builds prompts for persona-based LLM operations

    persona_manager : Persona__Manager
    prompts         : Prompts__Persona

    def build_translate_prompt(self, content : Safe_Str__Content,
                                     persona : Schema__Persona
                               ) -> Schema__Prompt__Request:        # Build prompt for translating content to a persona

        system_prompt = self._build_translate_system_prompt(persona)
        user_prompt   = self._build_translate_user_prompt(content, persona)

        return Schema__Prompt__Request(
            system_prompt = system_prompt,
            user_prompt   = user_prompt,
            language      = persona.language,
            max_tokens    = persona.communication_style.max_response_length
        )

    def build_impersonate_prompt(self, query   : Safe_Str__Query,
                                       persona : Schema__Persona
                                 ) -> Schema__Prompt__Request:      # Build prompt for impersonating (responding as) a persona

        system_prompt = self._build_impersonate_system_prompt(persona)
        user_prompt   = self._build_impersonate_user_prompt(query)

        return Schema__Prompt__Request(
            system_prompt = system_prompt,
            user_prompt   = user_prompt,
            language      = persona.language,
            max_tokens    = persona.communication_style.max_response_length
        )

    def build_generate_persona_prompt(self, description : Safe_Str__Content,
                                            name        : Optional[Safe_Str__Text] = None
                                      ) -> Schema__Prompt__Request:
        """Build prompt for generating a persona from description"""

        system_prompt = Safe_Str__Prompt(self.prompts.GENERATE__SYSTEM)

        name_instruction = f"\nThe persona's name should be: {name}" if name else ""
        user_content     = self.prompts.GENERATE__USER__TEMPLATE.format(
            description      = description,
            name_instruction = name_instruction
        )
        user_prompt = Safe_Str__Prompt(user_content)

        return Schema__Prompt__Request(
            system_prompt = system_prompt,
            user_prompt   = user_prompt
        )

    def _build_translate_system_prompt(self, persona: Schema__Persona) -> Safe_Str__Prompt:
        """Build system prompt for translation"""

        prompt_parts = [
            self.prompts.TRANSLATE__SYSTEM__INTRO,
            "",
            "TARGET AUDIENCE PROFILE:",
            str(self.persona_manager.to_prompt_context(persona)),
            ""
        ]

        expert_domains = self.persona_manager.get_primary_expertise_domains(persona)
        knowledge_gaps = self.persona_manager.get_knowledge_gaps(persona)
        style          = persona.communication_style

        if expert_domains:
            prompt_parts += [
                f"This audience has deep expertise in: {', '.join(str(d) for d in expert_domains)}",
                "You can use technical terminology in these areas without explanation.",
                ""
            ]

        if knowledge_gaps:
            prompt_parts += [
                f"This audience has limited knowledge in: {', '.join(str(d) for d in knowledge_gaps)}",
                "Explain or simplify terminology from these areas.",
                ""
            ]

        prompt_parts += [
            "COMMUNICATION GUIDELINES:",
            f"- Use {style.tone.value} tone",
            f"- Provide {style.detail_level.value} level of detail"
        ]

        if style.prefers_examples:
            prompt_parts.append("- Include relevant examples")
        if style.prefers_analogies:
            prompt_parts.append("- Use analogies to explain complex concepts")
        if style.prefers_bullet_points:
            prompt_parts.append("- Use bullet points for clarity")
        if style.max_response_length:
            prompt_parts.append(f"- Keep response to approximately {style.max_response_length} words")

        prompt_parts += [
            "",
            f"OUTPUT LANGUAGE: {persona.language}",
            f"Translate the message to {persona.language} if needed.",
            "Ensure all output is in the specified language.",
            "",
            self.prompts.TRANSLATE__INSTRUCTIONS
        ]

        return Safe_Str__Prompt("\n".join(prompt_parts))

    def _build_translate_user_prompt(self, content : Safe_Str__Content,
                                           persona : Schema__Persona
                                     ) -> Safe_Str__Prompt:
        """Build user prompt for translation"""

        prompt_parts = [
            self.prompts.TRANSLATE__USER__PREFIX,
            "",
            "ORIGINAL MESSAGE:",
            str(content),
            "",
            f"TRANSLATE TO: {persona.language}",
            f"ADAPT FOR: {persona.name} ({persona.role})",
            "",
            "Provide the adapted message that will be clear and relevant to this specific audience."
        ]

        if persona.priorities:
            prompt_parts += [
                "",
                "Focus on these priorities in your adaptation:",
                "- " + "\n- ".join(str(p) for p in persona.priorities)
            ]

        return Safe_Str__Prompt("\n".join(prompt_parts))

    def _build_impersonate_system_prompt(self, persona: Schema__Persona) -> Safe_Str__Prompt:
        """Build system prompt for impersonation"""

        intro = self.prompts.IMPERSONATE__SYSTEM__INTRO.format(
            name = persona.name,
            role = persona.role
        )

        prompt_parts = [
            intro,
            "",
            "YOUR IDENTITY AND BACKGROUND:",
            str(self.persona_manager.to_prompt_context(persona))
        ]

        if persona.description:
            prompt_parts += ["", f"About you: {persona.description}"]

        if persona.background_context:
            prompt_parts += ["", f"Additional context: {persona.background_context}"]

        # Simplified expertise description per TODO
        expertise_map = ", ".join([f"{domain}: {level.value}"
                                  for domain, level in persona.expertise.items()])
        prompt_parts += [
            "",
            "YOUR EXPERTISE:",
            self.prompts.EXPERTISE__TEMPLATE.format(expertise_map=expertise_map)
        ]

        style = persona.communication_style
        prompt_parts += [
            "",
            "YOUR COMMUNICATION STYLE:",
            f"- You speak in a {style.tone.value} tone",
            f"- You provide {style.detail_level.value} responses"
        ]

        if style.style_notes:
            prompt_parts.append(f"- {style.style_notes}")

        if persona.interests:
            prompt_parts += ["", "YOUR INTERESTS:", "- " + "\n- ".join(str(i) for i in persona.interests)]

        if persona.priorities:
            prompt_parts += ["", "YOUR PRIORITIES:", "- " + "\n- ".join(str(p) for p in persona.priorities)]

        instructions = self.prompts.IMPERSONATE__INSTRUCTIONS.format(language=persona.language)
        prompt_parts += ["", instructions]

        return Safe_Str__Prompt("\n".join(prompt_parts))

    def _build_impersonate_user_prompt(self, query: Safe_Str__Query) -> Safe_Str__Prompt:
        """Build user prompt for impersonation"""

        prompt_parts = [
            "QUERY:",
            str(query),
            "",
            self.prompts.IMPERSONATE__USER__PREFIX
        ]

        return Safe_Str__Prompt("\n".join(prompt_parts))




