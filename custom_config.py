from dlt.sources.rest_api import RESTAPIConfig, rest_api_source
from dlt.common.configuration.specs import BaseConfiguration
from dlt.sources.helpers.rest_client.auth import AuthConfigBase
from requests import PreparedRequest, Session as BaseSession  # noqa: I251
from dlt.common.typing import TSecretStrValue


from dlt.common.configuration.specs.exceptions import NativeValueError
from dlt.sources.config import configspec, with_config
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Final,
    Iterable,
    List,
    Literal,
    Optional,
    Union,
    cast,
)

TApiKeyLocation = Literal[
    "header", "cookie", "query", "param"
]  # Alias for scheme "in" field


@configspec
class APIKeyAuth(AuthConfigBase):
    """Uses provided `api_key` to create authorization data in the specified `location` (query, param, header, cookie) under specified `name`"""

    name1: str = "Authorization"
    api_key: TSecretStrValue = None
    name2: str = "Authorization"
    api_secret: TSecretStrValue = None
    location: TApiKeyLocation = "header"

    def parse_native_representation(self, value: Any) -> None:
        if isinstance(value, str):
            self.api_key = value
        else:
            raise NativeValueError(
                type(self),
                value,
                f"APIKeyAuth api_key must be a string, got {type(value)}",
            )

    def __call__(self, request: PreparedRequest) -> PreparedRequest:
        if self.location == "header":
            request.headers[self.name1] = self.api_key
            request.headers[self.name2] = self.api_secret
        elif self.location in ["query", "param"]:
            request.prepare_url(request.url, {self.name: self.api_key})
        elif self.location == "cookie":
            raise NotImplementedError()
        return request
