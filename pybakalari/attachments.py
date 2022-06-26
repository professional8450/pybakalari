from __future__ import annotations

from .models import Object
from typing import Any, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .http import HTTPClient


class Attachment(Object):
    """
    Represents a file attachment.

    Attributes
    ----------
    name : :class:`str`
        The name of the file.
    size : :class:`int`
        The size of the file in bytes.
    type : :class:`str`
        The `MIME type <https://www.iana.org/assignments/media-types/media-types.xhtml>`_ of the file.
    """
    def __init__(self, http: HTTPClient, data: Dict[str, Any]):
        super().__init__(id=data['Id'])
        self._http: HTTPClient = http
        self.name: str = data['Name']
        self.size: int = data['Size']
        self.type: str = data['Type']

    def __repr__(self):
        return (
            f'<Attachment id={self.id} name={self.name} size={self.size} type={self.type}>'
        )

    async def download(self, fp: str, name: Optional[str] = None):
        """
        Downloads the attachment and saves it to a file.

        Parameters
        ----------
        fp : :class:`str`
            The path to the folder in which to save the file.
        name : Optional[:class:`str`]
            The name to use for the file. If not specified, then the name of the attachment is used instead.
        """
        data = await self._http.attachment(self.id)
        name = self.name if not name else name
        file = open(f'{fp.rstrip("/")}/{name}', mode='wb')
        return file.write(data)
