from __future__ import annotations

from .models import Class, Room, Object, Student, Teacher
from typing import Any, Dict, List, Optional, TYPE_CHECKING

import dateutil.parser

if TYPE_CHECKING:
    from datetime import datetime


class EventTime:
    """
    A class that represents the time of a :class:`Event`.

    Attributes
    ----------
    whole_day : :class:`bool`
        Indicates whether the event is for the entire day or a specific time period.
    start_time : :class:`datetime.datetime`
        The starting time of the event.
    end_time : :class:`datetime.datetime`
        The ending time of the event.
    """
    def __init__(self, data: Dict[str, Any]):
        self.whole_day: bool = data['WholeDay']
        self.start_time: datetime = dateutil.parser.parse(data['StartTime'])
        self.end_time: datetime = dateutil.parser.parse(data['EndTime'])

    def __repr__(self):
        return (
            f'<EventTime start_time={self.start_time} end_time={self.end_time} whole_day={self.whole_day}>'
        )


class EventType(Object):
    """
    A class that represents the type of a :class:`Event`.

    Attributes
    ----------
    id : :class:`str`
        The ID of the event type.
    abbreviation : Optional[:class:`str`]
        The abbreviation of the event type.
    name : Optional[:class:`str`]
        The name of the event type.
    """
    def __init__(self, data: Dict[str, Any]):
        super().__init__(id=data['Id'])
        self.abbreviation: Optional[str] = data.get('Abbreviation')
        self.name: Optional[str] = data['Name']

    def __repr__(self):
        return (
            f'<EventType id={self.id} abbreviation={self.abbreviation} name={self.name}>'
        )


class Event(Object):
    """
    Represents a Bakaláři event.

    Attributes
    ----------
    id : :class:`str`
        The ID of the event.
    title : :class:`str`
        The title of the event.
    type : :class:`EventType`
        The type of the event.
    date_changed : :class:`datetime.datetime`
        A date that represents when the event was last changed.
    description : Optional[:class:`str`]
        The description of the event.
    times : List[:class:`EventTime`]
        A list of times that represent when the event will occur.
    teachers : List[:class:`Teacher`]
        A list of teachers attached to this event.
    classes : List[:class:`Class`]
        A list of classes attached to this event.
    rooms : List[:class:`Room`]
        A list of rooms attached to this event.
    students : List[:class:`Student`]
        A list of students attached to this event.
    note : Optional[:class:`str`]
        The note for the event.
    """
    def __init__(self, data: Dict[str, Any]):
        super().__init__(id=data['Id'])
        self.title: str = data['Title']
        self.type: EventType = EventType(data['EventType'])
        self.date_changed: datetime = dateutil.parser.parse(data['DateChanged'])
        self.description: Optional[str] = None
        self.times: List[EventTime] = []
        self.teachers: List[Teacher] = []
        self.classes: List[Class] = []
        self.rooms: List[Room] = []
        self.students: List[Student] = []
        self.note: Optional[str] = None

        if data['Description']:
            self.description: Optional[str] = data['Description']

        if data['Times']:
            self.times = [EventTime(time) for time in data['Times']]

        if data['Teachers']:
            for teacher in data['Teachers']:
                info = {
                    'TeacherID': teacher['Id'],
                    'TeacherAbbrev': teacher['Abbrev'],
                    'TeacherName': teacher['TeacherName']
                }

                self.teachers.append(Teacher(info))

        if data['Note']:
            self.note = data['Note']

        if data['Classes']:
            self.classes = [Class(item) for item in data['Classes']]

        if data['Rooms']:
            self.rooms = [Room(item) for item in data['Rooms']]

        if data['Students']:
            self.students = [Student(item) for item in data['Students']]

    def __repr__(self):
        return (
            f'<Event id={self.id} title={self.title} type={self.type} date_changed={self.date_changed} description={self.description} '
            f'times={self.times} teachers={self.teachers} note={self.note}>'
        )
