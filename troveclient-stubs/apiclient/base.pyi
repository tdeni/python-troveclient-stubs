import abc
from typing import Any, Callable, Dict, List, Optional, Self, Union  # type: ignore

import requests
from troveclient.apiclient.client import BaseClient

def getid(obj: Any) -> Union[str, Any]: ...

class HookableMixin(object):
    @classmethod
    def add_hook(cls, hook_type: str, hook_func: Callable) -> None: ...
    @classmethod
    def run_hooks(cls, hook_type: str, *args, **kwargs) -> None: ...

class BaseManager(HookableMixin):
    def __init__(self, client: BaseClient): ...
    def _list(
        self, url: str, response_key: str, obj_class=None, json: Optional[bool] = None
    ): ...
    def _get(self, url: str, response_key: str): ...
    def _head(self, url: str) -> bool: ...
    def _post(
        self, url: str, json: bool, response_key: str, return_raw: bool = False
    ): ...
    def _put(
        self, url: str, json: Optional[bool] = None, response_key: Optional[str] = None
    ): ...
    def _patch(
        self, url: str, json: Optional[bool] = None, response_key: Optional[str] = None
    ): ...
    def _delete(self, url: str) -> requests.Response: ...

class ManagerWithFind(BaseManager, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def list(self) -> List: ...
    def find(self, **kwargs) -> Any: ...
    def findall(self, **kwargs) -> List[Any]: ...

class CrudManager(BaseManager):
    def build_url(self, base_url: Optional[str] = None, **kwargs) -> str: ...
    def _filter_kwargs(self, kwargs: Dict) -> Dict: ...
    def list(self, base_url: Optional[str] = None, **kwargs): ...
    def put(self, base_url: Optional[str] = None, **kwargs): ...
    def find(self, base_url: Optional[str] = None, **kwargs): ...

class Extension(HookableMixin):
    def __init__(self, name: str, module: str): ...

class Resource(object):
    def __init__(self, manager: BaseManager, info: Dict, loaded: bool = False): ...
    @property
    def human_id(self) -> Optional[str]: ...
    def _add_details(self, info: Dict): ...
    def __getattr__(self, k: str): ...
    def __eq__(self, other: Self) -> bool: ...
    @property
    def is_loaded(self) -> bool: ...
    def to_dict(self) -> Dict: ...
