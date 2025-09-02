from typing                                                         import Dict, Any, Optional
from osbot_fast_api.api.routes.Fast_API__Routes                     import Fast_API__Routes
from osbot_utils.type_safe.primitives.safe_str.identifiers.Safe_Id  import Safe_Id
from mgraph_ai_service_personas.service.personas.Persona__Service   import Persona__Service


TAG__ROUTES_TRANSLATE     = 'translate'
ROUTES_PATHS__TRANSLATE   = [f'/{TAG__ROUTES_TRANSLATE}/translate',
                             f'/{TAG__ROUTES_TRANSLATE}/batch'   ,
                             f'/{TAG__ROUTES_TRANSLATE}/chain'   ]


class Routes__Translate(Fast_API__Routes):                                                               # Routes for persona-based translation

    tag             : str               = TAG__ROUTES_TRANSLATE
    persona_service : Persona__Service = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.persona_service = Persona__Service()

    def translate(self, content     : str,
                        persona_id  : Optional[str]           = None,
                        persona_data: Optional[Dict[str, Any]] = None,
                        use_cache   : bool                    = True
                 ) -> Dict[str, Any]:                                                               # POST /translate
        try:
            if not persona_id and not persona_data:
                return {'status': 'error', 'message': 'Either persona_id or persona_data must be provided'}

            safe_persona_id = Safe_Id(persona_id) if persona_id else None

            return self.persona_service.translate_to_persona(content     = content,
                                                             persona_id  = safe_persona_id,
                                                             persona_data= persona_data,
                                                             use_cache   = use_cache)
        except Exception as e:
            return {'status': 'error', 'message': f'Translation failed: {str(e)}'}

    def batch(self, content     : str,
                    persona_ids : list[str],
                    use_cache   : bool = True
             ) -> Dict[str, Any]:                                                                 # POST /translate/batch
        try:
            if not persona_ids:
                return {'status': 'error', 'message': 'No persona IDs provided'}

            translations = []
            errors       = []

            for persona_id in persona_ids:
                safe_id = Safe_Id(persona_id)
                result  = self.persona_service.translate_to_persona(content    = content,
                                                                    persona_id = safe_id,
                                                                    use_cache  = use_cache)
                if result.get('status') == 'success':
                    translations.append({'persona_id'        : persona_id,
                                          'persona_name'      : result.get('persona_name')     ,
                                          'language'           : result.get('language')         ,
                                          'translated_content' : result.get('translated_content'),
                                          'from_cache'         : result.get('from_cache', False)})
                else:
                    errors.append({'persona_id': persona_id, 'error': result.get('message')})

            return {'status'                 : 'success',
                    'original_content'       : content,
                    'translations'           : translations,
                    'errors'                 : errors if errors else None,
                    'total_personas'         : len(persona_ids),
                    'successful_translations': len(translations)}
        except Exception as e:
            return {'status': 'error', 'message': f'Batch translation failed: {str(e)}'}

    def chain(self, content         : str,
                    from_persona_id: Optional[str] = None,
                    to_persona_id  : str           = None,
                    include_response: bool         = False
             ) -> Dict[str, Any]:                                                                 # POST /translate/chain
        try:
            if not to_persona_id:
                return {'status': 'error', 'message': 'to_persona_id is required'}

            safe_from_id = Safe_Id(from_persona_id) if from_persona_id else None
            safe_to_id   = Safe_Id(to_persona_id)

            return self.persona_service.chain_translation(content         = content,
                                                          from_persona_id = safe_from_id,
                                                          to_persona_id   = safe_to_id,
                                                          include_response= include_response)
        except Exception as e:
            return {'status': 'error', 'message': f'Chain translation failed: {str(e)}'}

    def setup_routes(self):                                                                            # Setup all translation routes
        self.add_route_post(self.translate)
        self.add_route_post(self.batch    )
        self.add_route_post(self.chain    )
