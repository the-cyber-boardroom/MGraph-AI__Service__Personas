from osbot_fast_api.api.routes.Routes__Config                       import Routes__Config
from osbot_fast_api.api.routes.Routes__Set_Cookie                   import Routes__Set_Cookie
from osbot_fast_api_serverless.fast_api.Serverless__Fast_API        import Serverless__Fast_API
from mgraph_ai_service_personas.config                              import FAST_API__TITLE
from mgraph_ai_service_personas.fast_api.routes.Routes__Info        import Routes__Info
from mgraph_ai_service_personas.fast_api.routes.Routes__Respond     import Routes__Respond
from mgraph_ai_service_personas.fast_api.routes.Routes__Translate   import Routes__Translate
from mgraph_ai_service_personas.utils.Version                       import version__mgraph_ai_service_personas


class Service__Fast_API(Serverless__Fast_API):
    default_routes = True                           # BUG: without this, service doesn't work offline (npm routes are used)
    name           = FAST_API__TITLE
    version        = version__mgraph_ai_service_personas

    def setup_routes(self):
        self.add_routes(Routes__Info      )
        self.add_routes(Routes__Config    )
        self.add_routes(Routes__Set_Cookie)
        self.add_routes(Routes__Translate )
        self.add_routes(Routes__Respond   )




