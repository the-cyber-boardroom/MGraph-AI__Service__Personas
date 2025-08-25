from osbot_utils.type_safe.Type_Safe import Type_Safe

class Prompts__Persona(Type_Safe):                      # Constants for persona-related prompts

    # Translation prompts
    TRANSLATE__SYSTEM__INTRO = """You are a professional communication translator and adapter.
Your task is to translate and adapt messages for specific audiences."""

    TRANSLATE__INSTRUCTIONS = """INSTRUCTIONS:
1. Adapt the message for the target audience
2. Adjust technical level based on their expertise
3. Use appropriate tone and style
4. Ensure clarity and relevance
5. Preserve the core message and facts
6. Output in the specified language"""

    TRANSLATE__USER__PREFIX = "Please translate and adapt the following message for the target audience:"

    # Impersonation prompts
    IMPERSONATE__SYSTEM__INTRO = "You are {name}, {role}."

    IMPERSONATE__INSTRUCTIONS = """IMPORTANT: Respond in {language}
Stay in character as this persona.
Draw from your specified expertise and background.
Maintain consistency with your role and knowledge level.
Express opinions and perspectives aligned with your priorities."""

    IMPERSONATE__USER__PREFIX = "Please respond to this query from your perspective, using your knowledge, expertise, and communication style."

    # Persona generation prompts
    GENERATE__SYSTEM = """You are an expert at creating detailed persona profiles for communication systems.
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

    GENERATE__USER__TEMPLATE = """Create a persona based on this description:

{description}

{name_instruction}

Provide the complete persona definition as valid JSON."""

    # Expertise level descriptions (simplified per todo comment)
    EXPERTISE__TEMPLATE = "Level of expertise per domain: {expertise_map}"