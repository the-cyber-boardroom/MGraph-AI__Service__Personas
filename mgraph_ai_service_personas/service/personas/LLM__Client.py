import requests
from osbot_utils.type_safe.Type_Safe                                import Type_Safe
from osbot_utils.type_safe.primitives.safe_str.identifiers.Safe_Id  import Safe_Id
from osbot_utils.type_safe.primitives.safe_str.text.Safe_Str__Text  import Safe_Str__Text
from osbot_utils.type_safe.primitives.safe_uint.Safe_UInt           import Safe_UInt
from mgraph_ai_service_personas.schemas.Safe_Str__Content           import Safe_Str__Content
from mgraph_ai_service_personas.schemas.Safe_Str__Prompt            import Safe_Str__Prompt
from mgraph_ai_service_personas.schemas.Schema__LLM__Config         import Schema__LLM__Config
from mgraph_ai_service_personas.schemas.Schema__LLM__Response       import Schema__LLM__Response


class LLM__Client(Type_Safe):                       # Client for interacting with LLM service"""
    config: Schema__LLM__Config

    def call_llm(self, system_prompt  : Safe_Str__Prompt,
                      user_prompt    : Safe_Str__Prompt,
                      **overrides
                 ) -> Schema__LLM__Response:            # Make a call to the LLM service

        # Build request payload
        payload = {
            'system_prompt' : str(system_prompt),
            'user_prompt'   : str(user_prompt),
            'model'         : str(self.config.model),
            'temperature'   : float(self.config.temperature),
            'max_tokens'    : int(self.config.max_tokens)
        }

        # Apply any overrides
        if 'response_format' in overrides:
            payload['response_format'] = overrides['response_format']
        if 'max_tokens' in overrides and overrides['max_tokens']:
            payload['max_tokens'] = int(overrides['max_tokens'])

        try:
            # Make the API call
            response = requests.post(
                url     = f"{self.config.service_url}/complete",
                json    = payload,
                timeout = 30
            )
            response.raise_for_status()

            # Parse response
            data = response.json()

            # Return typed response
            return Schema__LLM__Response(
                status      = "success",
                content     = Safe_Str__Content(data.get('response', '')),
                model_used  = Safe_Id(data.get('model')) if data.get('model') else None,
                tokens_used = Safe_UInt(data.get('tokens_used')) if data.get('tokens_used') else None,
                message     = None
            )

        except requests.exceptions.RequestException as e:
            return Schema__LLM__Response(
                status  = "error",
                content = Safe_Str__Content(""),
                message = Safe_Str__Text(f"LLM service error: {str(e)}")
            )
        except Exception as e:
            return Schema__LLM__Response(
                status  = "error",
                content = Safe_Str__Content(""),
                message = Safe_Str__Text(f"Unexpected error: {str(e)}")
            )