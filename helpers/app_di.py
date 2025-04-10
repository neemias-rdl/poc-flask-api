class AppDI:
    def __init__(self):
        self._services = {}
        self._repositories = {}
        self._dtos = {}

    def register_service(self, service_name, service_instance):
        self._services[service_name] = service_instance

    def get_service(self, service_name):
        return self._services.get(service_name)
    
    def register_repository(self, repository_name, repository_instance):
        self._repositories[repository_name] = repository_instance

    def get_repository(self, repository_name):
        return self._repositories.get(repository_name)
    
    def register_dto(self, dto_name, dto_instance):
        self._dtos[dto_name] = dto_instance

    def get_dto(self, dto_name):
        return self._dtos.get(dto_name)
    
    def get_all_repositories(self):
        return self._repositories