from __future__ import annotations

import datetime
import dateutil.parser
from .models import Object, Teacher
from typing import Any, Dict, List, Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from .http import HTTPClient


class Subject(Object):
    """
    Represents a Bakaláři subject.

    Attributes
    ----------
    name : str
        The name of the subject.
    abbreviation : str
        The abbreviation of the subject.
    teacher : Optional[:class:`Teacher`]
        The teacher for the subject.

    """
    __slots__ = (
        "_http",
        "id",
        "name",
        "abbreviation",
        "teacher"
    )

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Subject id={self.id} name={self.name} abbreviation={self.abbreviation}> teacher={self.teacher}>'

    def __init__(self, http: HTTPClient, data: Dict[str, Any]):
        super().__init__(id=data['SubjectID'])
        self._http: HTTPClient = http
        self.name: str = data['SubjectName']
        self.abbreviation: str = data['SubjectAbbrev'].strip()
        self.teacher: Optional[Teacher] = Teacher(data) if data.get('TeacherID', None) else None

    async def get_lessons(self) -> List[SubjectLessonEntry]:
        """
        Returns a list of a subject's lessons.

        Returns
        =======
        List[:class:`.SubjectLessonEntry`]
        """
        data = await self._http.themes(self.id)
        return [SubjectLessonEntry(entry) for entry in data]


class SubjectLessonEntry:
    """
    Represents a lesson entry for a :class:`Subject`.

    Attributes
    ----------
    date : :class:`datetime.datetime`
        The date of the lesson.
    theme : Optional[:class:`str`]
        The theme of the lesson.
    note : Optional[:class:`str`]
        The note for the lesson.
    hour_caption : :class:`str`
        The hour caption of the lesson.
    lesson_label : :class:`str`
        The label of the lesson.

    """
    __slots__ = (
        "date",
        "theme",
        "note",
        "hour_caption",
        "lesson_label"
    )

    def __init__(self, data: Dict[str, Any]):
        self.date: datetime.datetime = dateutil.parser.isoparse(data['Date'])
        self.theme: Optional[str] = data.get('Theme')
        self.note: Optional[str] = data.get('Note')
        self.hour_caption: str = data['HourCaption']
        self.lesson_label: str = data['LessonLabel']

    def __repr__(self):
        return f'<SubjectLessonEntry date={self.date} theme={self.theme}>'
