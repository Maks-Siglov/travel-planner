from dependency_injector import containers, providers
from src.config import Settings, settings

class IoCContainer(containers.DeclarativeContainer):
    # ================================ CONFIG ================================

    # Injection into api routes
    wiring_config = containers.WiringConfiguration(
        packages=["src.api", "src.tasks"]
    )

    config: Settings = providers.Configuration()