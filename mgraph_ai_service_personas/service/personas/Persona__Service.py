from typing                                                                 import Dict, Any, Optional
from osbot_utils.type_safe.Type_Safe                                        import Type_Safe
from osbot_utils.type_safe.primitives.safe_str.identifiers.Safe_Id          import Safe_Id
from osbot_utils.utils.Env                                                  import get_env
from mgraph_ai_service_personas.schemas.Safe_Str__Persona__Name             import Safe_Str__Text
from mgraph_ai_service_personas.schemas.Schema__Persona                     import Schema__Persona
from mgraph_ai_service_personas.service.personas.Persona__Prompt_Builder    import Persona__Prompt_Builder


class Persona__Service(Type_Safe):                                                     # Core service for persona-based translation and response generation
    prompt_builder  : Persona__Prompt_Builder      
    llm_service_url : str                      

    def __init__(self):
        super().__init__()        
        self.llm_service_url = get_env("SERVICE_URL", "http://llms.dev.mgraph.ai")     # todo: the deployment is dev, qa and prod , we should also be capturing this 'deploy environment' value

    def translate_to_persona(self, content: Safe_Str__Text        ,                     # todo: see if Safe_Str__Text is flexible enough
                                   persona: Schema__Persona = None
                              ) -> Dict[str, Any]:
        
        system_prompt, user_prompt = self.prompt_builder.build_translate_prompt(content = content,          # todo: this should return an class instance not a tuple
                                                                                persona = persona)
        llm_response               = self.call_llm_service(system_prompt = system_prompt,
                                                            user_prompt   = user_prompt  ,
                                                            language      = str(persona.language),                              # all this should be part of the object returned by build_translate_prompt
                                                            max_tokens    = persona.communication_style.max_response_length)
        if llm_response.get('status') == 'error':
            return llm_response

        translated_content = llm_response.get('response', '')


        return {
            'status'            : 'success',                                    # todo: covert to Schema__Persona__Translate__Response
            'translated_content': translated_content,
            'persona_id'        : str(persona.id),
            'persona_name'      : str(persona.name),
            'language'          : str(persona.language),
            'from_cache'        : False
        }

    def respond_as_persona(self, query       : str                     ,
                                 persona     : Schema__Persona         ,
                                 context     : Optional[str]     = None,     # todo: see if we need this context (i.e there are valid use cases for it), since all the key info should had been provided via the persona class
                          ) -> Dict[str, Any]:                              # todo: covert to Schema__Persona__Respond_As__Response     # question: should we use "Impersonate" instead of "Response As" ??


        system_prompt, user_prompt = self.prompt_builder.build_respond_prompt(query   = query  ,
                                                                              persona = persona,
                                                                              context = context)
        llm_response               = self.call_llm_service(system_prompt = system_prompt,
                                                            user_prompt   = user_prompt  ,
                                                            language      = str(persona.language),
                                                            max_tokens    = persona.communication_style.max_response_length)
        if llm_response.get('status') == 'error':
            return llm_response

        response_content = llm_response.get('response', '')                     # todo: see if we need to do, since we could just return Schema__Persona__Respond_As__Response from the call_llm_service

        return {
            'status'       : 'success',                                         # todo: covert to Schema__Persona__Respond_As__Response
            'response'     : response_content,
            'persona_id'   : str(persona.id),
            'persona_name' : str(persona.name),
            'persona_role' : str(persona.role),
            'language'     : str(persona.language),
            'from_cache'   : False
        }

    def generate_persona_from_description(self, description: Safe_Str__Text ,
                                                name       : Safe_Id
                                           ) -> Dict[str, Any]:
        system_prompt, user_prompt = self.prompt_builder.build_generate_persona_prompt(description = description,
                                                                                       name        = name)
        llm_response               = self.call_llm_service(system_prompt    = system_prompt,
                                                            user_prompt      = user_prompt  ,
                                                            response_format  = "json")
        if llm_response.get('status') == 'error':
            return llm_response

        persona_data = llm_response.get('response', {})
        persona      = Schema__Persona.from_json(persona_data)
        return persona

    def chain_translation(self, content: str              ,         # todo: find a better name for this "translate + impersonate" step
                                persona: Schema__Persona  = None
                         ) -> Dict[str, Any]:
        results = {'status': 'success', 'original_content': content, 'steps': []}

        translation_result = self.translate_to_persona(content = content, persona = persona)            # todo: this should return a Type_Safe class
        if translation_result.get('status') == 'error':
            return translation_result

        translated_content = translation_result['translated_content']

        results['steps'].append({'step': 'translate_to_persona', 'result': translation_result})         # todo: steps should be a type_safe class

        results['translated_content'] = translated_content



        response_result = self.respond_as_persona(query    = translated_content ,
                                                  persona  = persona            ,
                                                  context  = f"You have just received this message: {translation_result['translated_content']}")    # todo: see if need this, since the respond_as_persona should already have this logic in the system prompt
        if response_result.get('status') == 'success':
            results['steps'].append({'step': 'persona_response', 'result': response_result})
            results['persona_response'] = response_result['response']

        return results                                                                              # todo: this should return a type_class

    def call_llm_service(self, system_prompt  : str,                                                # refactor to separate class
                               user_prompt    : str,
                               language       : Optional[str] = None,                               # todo: what is this language?
                               max_tokens     : Optional[int] = None,                               # todo: have an LLM_Config class which contains this max_tokens and other llm options like model (in fasct look at the current classes/schemas from llms.prod.mgraph.ai
                               response_format: Optional[str] = None
                         ) -> Dict[str, Any]:
        import requests

        payload = {'system_prompt': system_prompt,                                              # this should be provided as a config value (with good defaults)
                   'user_prompt'  : user_prompt  ,
                   'max_tokens'   : max_tokens or 1000,
                   'temperature'  : 0.7}

        if response_format: payload['response_format'] = response_format

        response = requests.post(f"{self.llm_service_url}/complete", json=payload)
        return response.json()