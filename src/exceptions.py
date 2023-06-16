class MalformedResponseError(Exception):
    pass


class NotSupportedEndpointError(Exception):
    pass


class InvalidCredentials(Exception):
    pass


class ResourceNotFound(Exception):
    pass


class PlanUpgradeRequired(Exception):
    pass


class UnknownError(Exception):
    pass
