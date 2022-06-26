import dateutil.parser
from enum import Enum
from typing import Any, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime


class ChangeType(Enum):
    """
    Specifies the type of a :class:`Change`.

    .. attribute:: canceled

        The lesson was canceled.

    .. attribute:: added

        The lesson was added into the timetable.

    .. attribute:: removed

        The lesson was removed from the timetable.

    .. attribute:: room_changed

        The room for the lesson was changed.

    .. attribute:: substitution

        The teacher for the lesson was changed.
    """

    canceled = 'Canceled'
    added = 'Added'
    removed = 'Removed'
    room_changed = 'RoomChanged'
    substitution = 'Substitution'


class Change:
    """
    Represents a change in the timetable.

    Attributes
    ----------
    date : :class:`datetime.datetime`
        The date of the change.
    hours: : :class:`str`
        The timetable hours that the change affects.
    type: : :class:`ChangeType`
        The type of the change.
    description : Optional[:class:`str`]
        The description of the change.
    time : :class:`str`
        The time of the change.
    """
    def __init__(self, data: Dict[str, Any]):
        self.date: datetime = dateutil.parser.isoparse(data['Day'])
        self.hours: str = data['Hours']
        self.type: ChangeType = ChangeType(data['ChangeType'])
        self.description: Optional[str] = None
        self.time: str = data['Time']

        if data['Description']:
            self.description: Optional[str] = data['Description']

    def __repr__(self):
        return (
            f'<Change date={self.date} hours={self.hours} type={self.type} description={self.description} time={self.time}>'
        )
