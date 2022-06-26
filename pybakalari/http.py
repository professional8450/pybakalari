from __future__ import annotations

import asyncio
import aiohttp
import json
from urllib.parse import quote
from typing import Any, Dict, List, Literal, Optional, Tuple
from .errors import BadRequest, InvalidServerResponse, Unauthorized, NotFound

class Route:
    def __init__(self, route: str, method: str, path: Optional[str] = None, **parameters: Any) -> None:
        self.base: str = route
        self.method: str = method
        self.path: Optional[str] = path
        url = self.base

        if self.path:
            url = self.base + self.path

        if parameters:
            url = url.format_map({k: quote(v) if isinstance(v, str) else v for k, v in parameters.items()})
        self.url: str = url


class HTTPClient:
    """The internal HTTP client that sends requests to the Bakaláři API."""

    def __init__(self, route: str) -> None:
        self.base: str = route.rstrip('/')
        self.api_version: Optional[str] = None
        self.username: Optional[str] = None
        self.password: Optional[str] = None
        self.token: Optional[str] = None
        self.session: Optional[aiohttp.ClientSession] = None
        self._refresh_token: Optional[str] = None

    async def close(self) -> None:
        if self.session:
            await self.session.close()

    async def request(self, route: Route, raw: bool = False, **kwargs: Dict[Any, Any]) -> Any:
        method = route.method
        url = route.url
        headers: Dict[str, str] = {}
        
        if not kwargs.get('headers'):
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
        else:
            headers = kwargs.pop('headers')

        if not self.session:
            raise Exception('not logged in')

        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'

        async with self.session.request(method, url, headers=headers, **kwargs) as response:
            if not response.status == 200:
                error = await response.json() if response.headers["content-type"].startswith('application/json') else await response.text()

                if response.status == 400:
                    raise BadRequest(error)
                if response.status == 401:
                    raise Unauthorized(error)
                if response.status == 404:
                    raise NotFound(error)

            if not raw and not response.headers["content-type"].startswith('application/json'):
                raise InvalidServerResponse(f'expected application/json, got {response.headers["content-type"]}')

            if raw:
                return await response.read()
            else:
                return await response.json(encoding='utf-8')

    async def _reauthenticate(self, refresh_time: int = 0) -> None:
        await asyncio.sleep(refresh_time)

        data = await self.request(
            Route(self.base, 'POST', '/api/login'),
            data={
                'client_id': 'ANDR',
                'grant_type': 'refresh_token',
                'refresh_token': self._refresh_token
            }
        )

        self.token = data['access_token']
        await self._reauthenticate(data['expires_in'])

    async def api_login(self, *, username: str, password: str, refresh: Optional[bool] = False) -> Tuple[str, str]:
        self.session = aiohttp.ClientSession()

        data = await self.request(
                Route(self.base, 'POST', '/api/login'),
                data={
                    'client_id': 'ANDR',
                    'grant_type': 'password',
                    'username': username,
                    'password': password
                }
        )

        if not self.token and refresh:
            asyncio.create_task(self._reauthenticate(data['expires_in']))

        self.token = data['access_token']
        self._refresh_token = data['refresh_token']
        self.api_version = data['bak:ApiVersion']

        return self.token, self.api_version

    async def subjects(self) -> List[Dict[str, Any]]:
        data = await self.request(
            Route(self.base, 'GET', '/api/3/subjects')
        )

        return data['Subjects']

    async def themes(self, subject_id: str) -> List[Dict[str, Any]]:
        response = await self.request(
            Route(self.base, 'GET', '/api/3/subjects/themes/{subject_id}', subject_id=subject_id)
        )

        return response['Themes']

    async def absence(self) -> Dict[str, Any]:
        return await self.request(
            Route(self.base, 'GET', '/api/3/absence/student')
        )

    async def api(self) -> List[Dict[str, Any]]:
        return await self.request(
            Route(self.base, 'GET', '/api')
        )

    async def api_v3(self) -> Dict[str, Any]:
        return await self.request(
            Route(self.base, 'GET', '/api/3')
        )

    async def events(self, type: Optional[Literal['my', 'public']] = None, since: Optional[str] = None, until: Optional[str] = None) -> List[Dict[str, Any]]:
        params: Dict[str, str] = {}

        if since:
            params['from'] = since

        route = Route(
            self.base,
            'GET',
            '/api/3/events' + f'/{type}' if type else ''
        )

        response = await self.request(route, params=params)
        return response['Events']

    async def gdpr_commissioners(self) -> List[Dict[str, Any]]:
        response = await self.request(
            Route(self.base, 'GET', '/api/3/gdpr/commissioners')
        )

        return response['Commissioners']

    async def homework(self, since: Optional[str] = None, until: Optional[str] = None) -> List[Dict[str, Any]]:
        params: Dict[str, str] = {}

        if since:
            params['from'] = since

        if until:
            params['to'] = until

        route = Route(
            self.base, 'GET', '/api/3/homeworks'
        )

        response = await self.request(route, params=params)
        return response['Homeworks']

    async def marks(self) -> List[Dict[str, Any]]:
        response = await self.request(
            Route(self.base, 'GET', '/api/3/marks')
        )

        return response['Subjects']

    async def marks_final(self) -> List[Dict[str, Any]]:
        response = await self.request(
            Route(self.base, 'GET', '/api/3/marks/final')
        )

        return response['CertificateTerms']

    async def marks_measures(self) -> List[Dict[str, Any]]:
        response = await self.request(
            Route(self.base, 'GET', '/api/3/marks/measures')
        )

        return response['PedagogicalMeasures']

    async def marks_new(self) -> int:
        response: int = await self.request(
            Route(self.base, 'GET', '/api/3/marks/count-new')
        )

        return response

    async def homework_unclosed(self) -> int:
        response: int = await self.request(
            Route(self.base, 'GET', '/api/3/homework/count-actual')
        )

        return response

    async def attachment(self, attachment_id: str) -> bytes:
        return await self.request(
            Route(self.base, 'GET', '/api/3/komens/attachment/{attachment_id}', attachment_id=attachment_id),
            raw=True
        )

    async def homework_done(self, homework_id: str, boolean: bool) -> None:
        return await self.request(
            Route(self.base, 'PUT', '/api/3/homeworks/{homework_id}/student-done/{state}', homework_id=homework_id, state=boolean)
        )

    async def user(self):
        return await self.request(
            Route(self.base, 'GET', '/api/3/user')
        )

    async def predict(self, prediction_data: List[Dict[str, Any]]):
        data = await self.request(
            Route(self.base, 'POST', '/api/3/marks/what-if'),
            data=json.dumps(prediction_data),  # type: ignore
            headers={'Content-Type': 'application/json'}
        )

        return data['AverageText']

    async def substitutions(self, since: Optional[str] = None, until: Optional[str] = None):
        params: Dict[str, str] = {}

        if since:
            params['from'] = since

        if until:
            params['to'] = until

        route = Route(
            self.base, 'GET', '/api/3/substitutions'
        )

        response = await self.request(route, params=params)
        return response['Changes']

    async def timetable(self, _type: Literal['actual', 'public'], date: Optional[str] = None):
        params: Dict[str, str] = {}

        if date:
            params['date'] = date

        route = Route(
            self.base,
            'GET',
            '/api/3/timetable/' + _type
        )

        return await self.request(route, params=params)

    async def received_messages(self):
        data = await self.request(
            Route(self.base, 'POST', '/api/3/komens/messages/received')
        )

        return data['Messages']

    async def noticeboard(self):
        data = await self.request(
            Route(self.base, 'POST', '/api/3/komens/messages/noticeboard')
        )

        return data['Messages']
