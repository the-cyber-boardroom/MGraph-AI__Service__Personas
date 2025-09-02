

# Service identification
SERVICE_NAME              = 'mgraph_ai_service_personas'
FAST_API__TITLE           = "MGraph-AI Personas Service"
FAST_API__DESCRIPTION     = "Persona-based translation and response generation service"

# LocalStack configuration
LOCALSTACK__ENDPOINT_URL  = 'http://localhost:4566'
LOCALSTACK__REGION_NAME   = 'us-east-1'

# Lambda configuration
LAMBDA_DEPENDENCIES__FAST_API_SERVERLESS = ['osbot-fast-api-serverless==v1.17.0']

# Cache configuration
PERSONA_CACHE__DEFAULT__ROOT_FOLDER = 'persona-cache/'
PERSONA_CACHE__BUCKET_NAME__PREFIX  = 'service-persona-cache'
PERSONA_CACHE__BUCKET_NAME__SUFFIX  = 'data'
PERSONA_CACHE__DEFAULT_TTL_HOURS    = 24

# Persona storage configuration
PERSONA_STORAGE__BUCKET_NAME__PREFIX  = 'service-personas'
PERSONA_STORAGE__BUCKET_NAME__SUFFIX  = 'storage'
PERSONA_STORAGE__DEFAULT__ROOT_FOLDER = 'personas/'

# LLM Service configuration
LLM_SERVICE__DEFAULT_URL          = 'http://llms.prod.mgraph.ai'
LLM_SERVICE__DEFAULT_MODEL        = 'openai/gpt-4o-mini'
LLM_SERVICE__DEFAULT_TEMPERATURE  = 0.7
LLM_SERVICE__DEFAULT_MAX_TOKENS   = 1000

# Environment variable names
ENV_VAR__LOCALSTACK_ENABLED   = 'LOCALSTACK_ENABLED'
ENV_VAR__LLM_SERVICE_URL      = 'LLM_SERVICE_URL'
ENV_VAR__PERSONAS_CACHE_TTL   = 'PERSONAS_CACHE_TTL_HOURS'

# Default test data
TEST_DATA__SAMPLE_CONTENT = """
There has been a security incident involving ransomware in Division X. 
The attack has compromised several servers and is impacting the P&L statement. 
Q4 financial reporting may be delayed. Technical teams are actively working 
to contain the malware and restore systems from backups.
"""

TEST_DATA__SAMPLE_PERSONA = {
    "id"                : "ciso_pt",
    "name"              : "João Silva",
    "role"              : "Chief Information Security Officer",
    "language"          : "pt-PT",
    "expertise"         : {
        "cybersecurity" : "expert",
        "finance"       : "basic",
        "business"      : "intermediate"
    },
    "priorities"        : ["risk mitigation", "incident response", "technical accuracy"],
    "communication_style": {
        "tone"                : "professional",
        "detail_level"        : "detailed",
        "prefers_bullet_points": True
    }
}

# API Rate limits
API_RATE_LIMIT__REQUESTS_PER_MINUTE = 60
API_RATE_LIMIT__BURST_SIZE          = 10

# Validation constraints
PERSONA__MAX_NAME_LENGTH        = 100
PERSONA__MAX_ROLE_LENGTH        = 200
PERSONA__MAX_DESCRIPTION_LENGTH = 1000
PERSONA__MAX_PRIORITIES         = 10
PERSONA__MAX_EXPERTISE_DOMAINS  = 20

# Supported languages (can be extended)
SUPPORTED_LANGUAGES = [
    'en-US',  # English (US)
    'en-GB',  # English (UK)
    'pt-PT',  # Portuguese (Portugal)
    'pt-BR',  # Portuguese (Brazil)
    'es-ES',  # Spanish (Spain)
    'es-MX',  # Spanish (Mexico)
    'fr-FR',  # French (France)
    'de-DE',  # German (Germany)
    'it-IT',  # Italian (Italy)
    'nl-NL',  # Dutch (Netherlands)
    'pl-PL',  # Polish (Poland)
    'ru-RU',  # Russian (Russia)
    'zh-CN',  # Chinese (Simplified)
    'zh-TW',  # Chinese (Traditional)
    'ja-JP',  # Japanese (Japan)
    'ko-KR',  # Korean (South Korea)
    'ar-SA',  # Arabic (Saudi Arabia)
    'hi-IN'   # Hindi (India)
]
