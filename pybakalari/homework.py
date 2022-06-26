from __future__ import annotations

import dateutil.parser
from .models import Class, Group, Object, Teacher
from .attachments import Attachment
from .subject import Subject
from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .http import HTTPClient
    from datetime import datetime


class Homework(Object):
    """
    Represents a Bakaláři homework.

    .. warning::
        The :attr:`date_award`, :attr:`date_control`, :attr:`date_done` attributes are only
        filled if the Bakaláři server's API version is ``3.13.0`` or lower.

    .. warning::
        The :attr:`finished` attribute is only filled if the Bakaláři server's
        API version is higher than ``3.13.0``.

    Attributes
    ----------
    id : :class:`str`
        The ID of the homework.
    assigned_at : :class:`datetime.datetime`
        A date which represents when the homework was assigned.
    due_at : :class:`datetime.datetime`
        A date which represents when the homework is due.
    done : :class:`bool`
        Indicates whether the homework is done.
    closed : :class:`bool`
        Indicates whether the homework has been closed.
    hour : :class:`int`
        A number that represents the timetable hour that the homework is due in.
    homework_class : :class:`Class`
        The class that the homework has been assigned to.
    group : Optional[:class:`Group`]
        The group that the homework has been assigned to.
    subject : Optional[:class:`Subject`]
        The homework's subject.
    teacher : Optional[:class:`Teacher`]
        The teacher that assigned the homework.
    details : Optional[:class:`str`]
        The homework details.
    notice : Optional[:class:`str`]
        The notice message for the homework.
    finished : Optional[:class:`bool`]
        Indicates whether the homework has been finished.
    date_award : Optional[:class:`datetime.datetime`]
        ?
    date_control : Optional[:class:`datetime.datetime`]
        ?
    date_done : Optional[:class:`datetime.datetime`]
        ?
    """
    def __init__(self, http: HTTPClient, data: Dict[str, Any]):
        super().__init__(id=data['ID'])
        self._http: HTTPClient = http
        self.assigned_at: datetime = dateutil.parser.isoparse(data['DateStart'])
        self.due_at: datetime = dateutil.parser.isoparse(data['DateEnd'])
        self.done: bool = data['Done']
        self.closed: bool = data['Closed']
        self.electronic: bool = data['Electronic']
        self.hour: int = data['Hour']
        self.homework_class: Optional[Class] = None
        self.group: Optional[Group] = None
        self.subject: Optional[Subject] = None
        self.teacher: Optional[Teacher] = None
        self.details: Optional[str] = None
        self.notice: Optional[str] = None
        self.finished: Optional[bool] = None
        self.date_award: Optional[datetime] = None
        self.date_control: Optional[datetime] = None
        self.date_done: Optional[datetime] = None
        self.attachments: List[Attachment] = []

        if data.get('Class'):
            self.homework_class = Class(data.pop('Class'))

        if data.get('Group'):
            self.group = Group(data.pop('Group'))

        teacher_information = {}
        if data.get('Teacher'):
            teacher_information: Dict[str, Any] = {
                'TeacherID': data['Teacher']['Id'],
                'TeacherAbbrev': data['Teacher']['Abbrev'],
                'TeacherName': data['Teacher']['Name']
            }

            self.teacher = Teacher(teacher_information)

        if data.get('Subject'):
            subject_information: Dict[str, Any] = {
                'SubjectID': data['Subject']['Id'],
                'SubjectAbbrev': data['Subject']['Abbrev'],
                'SubjectName': data['Subject']['Name']
            }

            if data.get('Teacher'):
                subject_information = {**subject_information, **teacher_information}

            self.subject = Subject(http, subject_information)

        if data.get('Attachments'):
            self.attachments = [Attachment(self._http, attachment) for attachment in data.pop('Attachments')]

        if data.get('Content'):
            self.details = data.pop('Content')

        if data.get('Notice'):
            self.notice = data.pop('Notice')

        if data.get('Finished'):
            self.finished = data.pop('Finished')

        if data.get('DateAward'):
            self.date_award = dateutil.parser.isoparse(data.pop('DateAward'))

        if data.get('DateControl'):
            self.date_control = dateutil.parser.isoparse(data.pop('DateControl'))

        if data.get('DateDone'):
            self.date_done = dateutil.parser.isoparse(data.pop('DateDone'))

    async def mark_as_done(self):
        """
        Marks the homework as done.
        """
        await self._http.homework_done(self.id, True)

    async def mark_as_undone(self):
        """
        Marks the homework as undone.
        """
        await self._http.homework_done(self.id, False)
