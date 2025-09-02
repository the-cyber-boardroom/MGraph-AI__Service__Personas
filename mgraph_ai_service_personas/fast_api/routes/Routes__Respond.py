from typing                                                         import Dict, Any, Optional
from osbot_fast_api.api.routes.Fast_API__Routes                     import Fast_API__Routes
from osbot_utils.type_safe.primitives.safe_str.identifiers.Safe_Id  import Safe_Id

from mgraph_ai_service_personas.schemas.Schema__Persona import Schema__Persona
from mgraph_ai_service_personas.service.personas.Persona__Service   import Persona__Service


TAG__ROUTES_RESPOND     = 'respond'
ROUTES_PATHS__RESPOND   = [f'/{TAG__ROUTES_RESPOND}/respond'         ,
                           f'/{TAG__ROUTES_RESPOND}/generate-persona',
                           f'/{TAG__ROUTES_RESPOND}/conversation'    ]

# todo: fix this with the same patter
class Routes__Respond(Fast_API__Routes):                                                                # Routes for persona-based response generation

    tag             : str               = TAG__ROUTES_RESPOND
    persona_service : Persona__Service = None


    def respond(self, query       : str,
                      persona     : Schema__Persona
                 ) -> Dict[str, Any]:                                                                # todo: this should be a class

        return self.persona_service.respond_as_persona(query    = query,
                                                       persona  = persona)

    # todo: remove error handling since any errors should be handled insite the persona_service (with a valid object always returned)
    def generate_persona(self, description : str,
                               name        : Optional[str] = None,
                        ) -> Dict[str, Any]:                                                     # todo: this should be a class
        try:
            result = self.persona_service.generate_persona_from_description(description = description,
                                                                            name        = name       )
            if result.get('status') == 'error':
                return result

            return result
        except Exception as e:
            return {'status': 'error', 'message': f'Persona generation failed: {str(e)}'}

    # todo: refactor this to be a impersonate user, with a current message (for now let's not add support for any pass messages)
    def conversation(self, messages        : list[Dict[str, str]],
                           persona         : Schema__Persona
                    ) -> Dict[str, Any]:                                                       # POST /respond/conversation
        try:

            last_user_message = None
            for msg in reversed(messages):
                if msg.get('role') == 'user':
                    last_user_message = msg.get('content')
                    break

            if not last_user_message:
                return {'status': 'error', 'message': 'No user message found in conversation'}

            context = None

            result          = self.persona_service.respond_as_persona(query     = last_user_message,
                                                                       persona  = Schema__Persona)

            if result.get('status') == 'success':
                result['conversation'] = messages + [{'role': 'assistant', 'content': result.get('response')}]

            return result
        except Exception as e:
            return {'status': 'error', 'message': f'Conversation handling failed: {str(e)}'}

    def setup_routes(self):                                                                            # Setup all response generation routes
        self.add_route_post(self.respond)
        self.add_route_post(self.generate_persona)
        self.add_route_post(self.conversation)
