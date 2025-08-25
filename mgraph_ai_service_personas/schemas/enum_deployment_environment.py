from enum import Enum

class Enum__Deployment_Environment(Enum):       # Deployment environment for the service
    LOCAL = "local"
    DEV   = "dev"
    QA    = "qa"
    PROD  = "prod"