from typing                                                      import Tuple, Optional
from osbot_utils.type_safe.Type_Safe                             import Type_Safe

from mgraph_ai_service_personas.schemas.Enum__Expertise_Level import Enum__Expertise_Level
from mgraph_ai_service_personas.schemas.Schema__Persona import Schema__Persona


class Persona__Prompt_Builder(Type_Safe):                                                    # Builds prompts for persona-based LLM operations

    def build_translate_prompt(self, content: str,
                                      persona: Schema__Persona) -> Tuple[str, str]:
        system_prompt = self._build_translate_system_prompt(persona)
        user_prompt   = self._build_translate_user_prompt(content, persona)
        return system_prompt, user_prompt

    def build_respond_prompt(self, query  : str,
                                    persona: Schema__Persona,
                                    context: Optional[str] = None) -> Tuple[str, str]:
        system_prompt = self._build_respond_system_prompt(persona)
        user_prompt   = self._build_respond_user_prompt(query, context)
        return system_prompt, user_prompt

    # todo: move add 'prompt' text into separate const class with only those values (so that it is not mixed with the code below)
    def build_generate_persona_prompt(self, description: str,
                                            name       : Optional[str] = None) -> Tuple[str, str]:
        system_prompt = """You are an expert at creating detailed persona profiles for communication systems.
Your task is to generate a complete persona definition in JSON format based on a description.

The persona JSON must include:
- id: A unique identifier (lowercase, underscores for spaces)
- name: The persona's name
- role: Their professional role or position
- description: A brief description
- language: Language code (e.g., en-US, pt-PT, es-ES)
- expertise: Object mapping domains to expertise levels (none, basic, intermediate, advanced, expert)
- interests: Array of interests
- priorities: Array of what matters most to this persona
- communication_style: Object with:
  - tone: formal/informal/professional/casual/technical/friendly
  - detail_level: minimal/summary/moderate/detailed/comprehensive
  - style_notes: Additional style guidance
  - prefers_examples: boolean
  - prefers_analogies: boolean
  - prefers_bullet_points: boolean
  - max_response_length: approximate word count (optional)
- urgency_preference: How they handle urgent information
- background_context: Additional background
- common_terminology: Object of domain-specific terms they use
- avoid_terms: Array of terms to avoid

Ensure the persona is realistic and consistent with the description provided."""

        user_prompt  = f"Create a persona based on this description:\n\n{description}"
        if name:
            user_prompt += f"\n\nThe persona's name should be: {name}"
        user_prompt += "\n\nProvide the complete persona definition as valid JSON."

        return system_prompt, user_prompt

    def _build_translate_system_prompt(self, persona: Schema__Persona) -> str:
        prompt_parts = ["You are a professional communication translator and adapter.",
                        "Your task is to translate and adapt messages for specific audiences.",
                        "",
                        "TARGET AUDIENCE PROFILE:",
                        persona.to_prompt_context(), ""]

        expert_domains  = persona.get_primary_expertise_domains()
        knowledge_gaps  = persona.get_knowledge_gaps()
        style           = persona.communication_style

        if expert_domains:
            prompt_parts += [f"This audience has deep expertise in: {', '.join(expert_domains)}",
                             "You can use technical terminology in these areas without explanation.", ""]

        if knowledge_gaps:
            prompt_parts += [f"This audience has limited knowledge in: {', '.join(knowledge_gaps)}",
                             "Explain or simplify terminology from these areas.", ""]

        prompt_parts += ["COMMUNICATION GUIDELINES:",
                         f"- Use {style.tone.value} tone",
                         f"- Provide {style.detail_level.value} level of detail"]

        if style.prefers_examples:     prompt_parts.append("- Include relevant examples")
        if style.prefers_analogies:    prompt_parts.append("- Use analogies to explain complex concepts")
        if style.prefers_bullet_points:prompt_parts.append("- Use bullet points for clarity")
        if style.max_response_length: prompt_parts.append(f"- Keep response to approximately {style.max_response_length} words")

        prompt_parts += ["",
                         f"OUTPUT LANGUAGE: {persona.language}",
                         f"Translate the message to {persona.language} if needed.",
                         "Ensure all output is in the specified language.", ""]

        if persona.common_terminology:
            prompt_parts.append("PREFERRED TERMINOLOGY:")
            for term, replacement in persona.common_terminology.items():
                prompt_parts.append(f"- Use '{replacement}' instead of '{term}'")
            prompt_parts.append("")

        if persona.avoid_terms:
            prompt_parts.append(f"AVOID THESE TERMS: {', '.join(persona.avoid_terms)}")
            prompt_parts.append("")

        prompt_parts += ["INSTRUCTIONS:",
                         "1. Adapt the message for the target audience",
                         "2. Adjust technical level based on their expertise",
                         "3. Use appropriate tone and style",
                         "4. Ensure clarity and relevance",
                         "5. Preserve the core message and facts",
                         "6. Output in the specified language"]

        return "\n".join(prompt_parts)

    def _build_translate_user_prompt(self, content: str, persona: Schema__Persona) -> str:
        prompt_parts = ["Please translate and adapt the following message for the target audience:",
                        "",
                        "ORIGINAL MESSAGE:",
                        content,
                        "",
                        f"TRANSLATE TO: {persona.language}",
                        f"ADAPT FOR: {persona.name} ({persona.role})",
                        "",
                        "Provide the adapted message that will be clear and relevant to this specific audience."]

        if persona.priorities:
            prompt_parts += ["",
                             "Focus on these priorities in your adaptation:",
                             "- " + "\n- ".join(persona.priorities)]

        return "\n".join(prompt_parts)

    def _build_respond_system_prompt(self, persona: Schema__Persona) -> str:
        prompt_parts = [f"You are {persona.name}, {persona.role}.",
                        "",
                        "YOUR IDENTITY AND BACKGROUND:",
                        persona.to_prompt_context()]

        if persona.description:
            prompt_parts += ["", f"About you: {persona.description}"]

        if persona.background_context:
            prompt_parts += ["", f"Additional context: {persona.background_context}"]

        prompt_parts += ["", "YOUR EXPERTISE:"]

        # todo: this feels quite over the top since couldn't we just do: "Level of expertise of user per domain:...
        for domain, level in persona.expertise.items():
            if level   == Enum__Expertise_Level.EXPERT:      msg = "You are an expert with deep knowledge"
            elif level == Enum__Expertise_Level.ADVANCED:    msg = "You have advanced knowledge"
            elif level == Enum__Expertise_Level.INTERMEDIATE:msg = "You have moderate knowledge"
            elif level == Enum__Expertise_Level.BASIC:       msg = "You have basic understanding"
            else:                                            msg = "You have limited or no knowledge"
            prompt_parts.append(f"- {domain}: {msg}")

        style = persona.communication_style
        prompt_parts += ["", "YOUR COMMUNICATION STYLE:",
                         f"- You speak in a {style.tone.value} tone",
                         f"- You provide {style.detail_level.value} responses"]

        if style.style_notes:
            prompt_parts.append(f"- {style.style_notes}")

        if persona.interests:
            prompt_parts += ["", "YOUR INTERESTS:", "- " + "\n- ".join(persona.interests)]

        if persona.priorities:
            prompt_parts += ["", "YOUR PRIORITIES:", "- " + "\n- ".join(persona.priorities)]

        prompt_parts += ["", f"IMPORTANT: Respond in {persona.language}",
                         "Stay in character as this persona.",
                         "Draw from your specified expertise and background.",
                         "Maintain consistency with your role and knowledge level.",
                         "Express opinions and perspectives aligned with your priorities."]

        return "\n".join(prompt_parts)

    def _build_respond_user_prompt(self, query: str, context: Optional[str] = None) -> str:
        prompt_parts = []
        if context:
            prompt_parts += ["CONTEXT:", context, ""]
        prompt_parts += ["QUERY:", query, "", "Please respond to this query from your perspective, using your knowledge, expertise, and communication style."]
        return "\n".join(prompt_parts)
