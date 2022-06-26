from __future__ import annotations

from typing import Any, Dict, List, Optional, TYPE_CHECKING
from .changes import Change
from .models import Cycle, Group, Teacher, Room
from .subject import Subject
import dateutil.parser
from enum import Enum

if TYPE_CHECKING:
    from datetime import datetime
    from .http import HTTPClient


class DayType(Enum):
    """
    Specifies the type of a :class:`Day`.

    .. attribute:: work_day

        Represents a work day.

    .. attribute:: weekend

        Represents a weekend day. This day type usually does not appear.

    .. attribute:: celebration

        Represents a state holiday or other important day.

    .. attribute:: holiday

        Represents a holiday.

    .. attribute:: headmaster_day

        Represents a day off given by the school principal.

    .. attribute:: undefined

        Any other type of day. This day type usually does not appear.
    """

    work_day = 'WorkDay'
    weekend = 'Weekend'
    celebration = 'Celebration'
    holiday = 'Holiday'
    headmaster_day = 'DirectorDay'
    undefined = 'Undefined'


class Hour:
    """
    Represents a timetable hour.

    Attributes
    ----------
    id : :class:`str`
        The ID of the timetable hour.
    caption : :class:`str`
        The caption of the timetable hour.
    begin_time : :class:`str`
        Represents the time when the hour begins.
    end_time : :class:`str`
        Represents the time when the hour ends.
    """
    def __init__(self, data: Dict[str, Any]):
        self.id: int = data['Id']
        self.caption: str = data['Caption']
        self.begin_time: str = data['BeginTime']
        self.end_time: str = data['EndTime']

    def __repr__(self):
        return (
            f'<Hour id={self.id} caption={self.caption} begin_time={self.begin_time} end_time={self.end_time}>'
        )


class Lesson:
    """
    Represents a timetable lesson.

    Attributes
    ----------
    hour : :class:`Hour`
        The hour of the lesson.
    groups : List[:class:`Group`]
        The list of the groups that are assigned to the lesson.
    subject : Optional[:class:`Subject`]
        The subject of the lesson.
    teacher : Optional[:class:`Teacher`]
        The teacher assigned to the lesson.
    room : Optional[:class:`Room`]
        The room for the lesson.
    cycles : List[:class:`Cycle`]
        A list of the lesson's cycles.
    homework : List[:class:`str`]
        A list of homework IDs that are due on this lesson.
    change : Optional[:class:`Change`]
        The information about the lesson's change.
    theme : Optional[:class:`str`]
        The theme of the lesson.
    """
    def __init__(self, http: HTTPClient, data: Dict[str, Any]):
        self.hour: Hour = Hour(data['Hour'])
        self.groups: List[Group] = [Group(group) for group in data['Groups']]
        self.subject: Optional[Subject] = None
        self.teacher: Optional[Teacher] = None
        self.room: Optional[Room] = None
        self.cycles: List[Cycle] = [Cycle(cycle) for cycle in data['Cycles']]
        self.homework: List[str] = []
        self.change: Optional[Change] = None
        self.theme: Optional[str] = None

        if data['Subject']:
            subject_information: Dict[str, Any] = {
                'SubjectID': data['Subject']['Id'],
                'SubjectAbbrev': data['Subject']['Abbrev'],
                'SubjectName': data['Subject']['Name']
            }

            self.subject = Subject(http, subject_information)

        if data['Teacher']:
            teacher_information: Dict[str, Any] = {
                'TeacherID': data['Teacher']['Id'],
                'TeacherAbbrev': data['Teacher']['Abbrev'],
                'TeacherName': data['Teacher']['Name']
            }

            self.teacher = Teacher(teacher_information)

        if data['Room']:
            self.room = Room(data['Room'])

        if data['Change']:
            self.change = Change(data['Change'])

        if data['Theme']:
            self.theme = data['Theme']

    def __repr__(self):
        return (
            f'<Lesson hour={self.hour} groups={self.groups} subject={self.subject} teacher={self.teacher} room={self.room} '
            f'cycles={self.cycles} homework={self.homework} change={self.change} theme={self.theme}>'
        )


class Day:
    """
    Represents a timetable day.

    Attributes
    ----------
    day_of_week : :class:`int`
        Represents the number of the day of the week. (1 = Monday, 2 = Tuesday, ...)
    date : :class:`datetime.datetime`
        The date of the day.
    day_description : Optional[:class:`str`]
        The description of the day.
    day_type : :class:`DayType`
        The type of the day.
    lessons : List[:class:`Lesson`]
        A list of lessons for that day.
    """
    def __init__(self, http: HTTPClient, data: Dict[str, Any]):
        self.day_of_week: int = data['DayOfWeek']
        self.date: datetime = dateutil.parser.isoparse(data['Date'])
        self.day_description: Optional[str] = None
        self.day_type: DayType = DayType(data['DayType'])
        self.lessons: List[Lesson] = [Lesson(http, atom) for atom in data['Atoms']]

        if data.get('DayDescription'):
            self.day_description = data.pop('DayDescription')

    def __repr__(self):
        return (
            f'<Day day_of_week={self.day_of_week} date={self.date} day_description={self.day_description} day_type={self.day_type} lessons={self.lessons}>'
        )


def _generate_timetable_data(http: HTTPClient, data: Dict[str, Any]) -> List[Day]:
    days = []
    for key in data:
        if key == 'Days':
            continue

        data[key] = {item['Id']: item for item in data[key]}

    for day in data['Days']:
        for atom in day['Atoms']:

            atom['Hour'] = data.get('Hours', {}).get(atom['HourId'])
            atom['Groups'] = [data.get('Groups', {}).get(group) for group in atom['GroupIds']]

            if any(atom['Groups']):
                for group in atom['Groups']:
                    group['Class'] = data.get('Classes', {}).get(group['ClassId'])

            atom['Subject'] = data.get('Subjects', {}).get(atom['SubjectId'])
            atom['Teacher'] = data.get('Teachers', {}).get(atom['TeacherId'])
            atom['Room'] = data.get('Rooms', {}).get(atom['RoomId'])
            atom['Cycles'] = [data.get('Cycles', {}).get(cycle) for cycle in atom['CycleIds']]

        days.append(Day(http, day))
    return days
