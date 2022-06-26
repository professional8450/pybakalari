from __future__ import annotations

from .subject import Subject
from dateutil import parser
from .models import Object
from typing import Any, Dict, List, Literal, Union, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime
    from .http import HTTPClient


class PredictionMark:
    def __init__(
            self,
            *,
            mark: Union[int, Literal['1', '1-', '2', '2-', '3', '3-', '4', '4-', '5']],
            weight: int
    ):
        self.id = None
        self.text = str(mark)
        self.max_points = 0
        self.weight = weight


class Mark(Object):
    """
    Represents a Bakaláři mark.

    Attributes
    ----------
    id : :class:`str`
        The ID of the mark.
    subject : :class:`Subject`
        The subject that the mark belongs to.
    date : :class:`datetime.datetime`
        A date representing when the mark was given.
    edited_at : :class:`datetime.datetime`
        A date representing when the mark was last edited.
    text : :class:`str`
        The text of the mark.
    weight : :class:`int`
        The weight of the mark.
    is_new : :class:`bool`
        Whether the mark is new.
    is_points : :class:`bool`
        Whether the mark uses points instead of regular marks.
    max_points : :class:`int`
        The maximum amount of points you can get for this mark.
    caption : Optional[:class:`str`]
        The caption of the mark.
    teacher_id : Optional[:class:`str`]
        The ID of the teacher that gave the mark.
    type : Optional[:class:`str`]
        The type of the mark.
    type_note : Optional[:class:`str`]
        The note for the type of the mark.
    calculated_mark_text : Optional[:class:`str`]
        The calculated mark text.
    class_rank_text : Optional[:class:`str`]
        The class rank text.
    points : Optional[:class:`int`]
        The amount of points you received.
    """
    def __init__(self, data: Dict[str, Any], subject: Subject):
        super().__init__(id=data['Id'])
        self.subject: Subject = subject
        self.date: datetime = parser.isoparse(data['MarkDate'])
        self.edited_at: datetime = parser.isoparse(data['EditDate'])
        self.text: str = data['MarkText']
        self.weight: int = data['Weight']
        self.is_new: bool = data['IsNew']
        self.is_points: bool = data['IsPoints']
        self.max_points: int = data['MaxPoints']
        self.caption: Optional[str] = None
        self.theme: Optional[str] = None
        self.teacher_id: Optional[str] = None
        self.type: Optional[str] = None
        self.type_note: Optional[str] = None
        self.calculated_mark_text: Optional[str] = None
        self.class_rank_text: Optional[str] = None
        self.points: Optional[int] = None

        if data.get('Caption'):
            self.caption = data.pop('Caption')

        if data.get('Theme'):
            self.theme = data.pop('Theme').rstrip('\n').strip()

        if data.get('TeacherId'):
            self.teacher_id = data.pop('TeacherId')

        if data.get('Type'):
            self.type = data.pop('Type')

        if data.get('TypeNote'):
            self.type_note = data.pop('TypeNote')

        if data.get('CalculatedMarkText'):
            self.calculated_mark_text = data.pop('CalculatedMarkText')

        if data.get('ClassRankText'):
            self.class_rank_text = data.pop('ClassRankText')

        if data.get('PointsText'):
            self.points = int(data.pop('PointsText'))

    def __repr__(self):
        return (
            f'<Mark date={self.date} caption={self.caption} theme={self.theme} text={self.text}>'
        )

    def __str__(self):
        return self.text


class FinalMark(Mark):
    """
    Represents a Bakaláři final mark.

    Attributes
    ----------
    id : :class:`str`
        The ID of the mark.
    subject : :class:`Subject`
        The subject that the mark belongs to.
    date : :class:`datetime.datetime`
        A date representing when the mark was given.
    edited_at : :class:`datetime.datetime`
        A date representing when the mark was last edited.
    text : :class:`str`
        The text of the mark.
    """
    def __init__(self, data: Dict[str, Any], subject: Subject):
        super().__init__(data=data, subject=subject)
        self.id: str = data['Id']
        self.subject: Subject = subject
        self.date: datetime = parser.isoparse(data['MarkDate'])
        self.edited_at: datetime = parser.isoparse(data['EditDate'])
        self.text: str = data['MarkText']

    def __repr__(self):
        return (
            f'<FinalMark id={self.id} date={self.date} text={self.text}>'
        )

    def __str__(self):
        return self.text


class PedagogicalMeasure:
    """
    Represents a Bakaláři pedagogical measure.

    Attributes
    ----------
    school_year : :class:`str`
        The school year of the pedagogical measure.
    semester : :class:`semester`
        The semester of the pedagogical measure.
    type_id : :class:`str`
        The ID of the type of the pedagogical measure.
    type_label : :class:`str`
        The label of the type of the pedagogical measure.
    date : :class:`datetime.datetime`
        A date representing when the pedagogical measure was given.
    text : :class:`str`
        The text of the pedagogical measure.
    """
    def __init__(self, data: Dict[str, Any]):
        self.school_year: str = data['SchoolYear']
        self.semester: str = data['Semester']
        self.type_id: str = data['TypeId']
        self.type_label: str = data['TypeLabel']
        self.date: datetime = parser.isoparse(data['Date'])
        self.text: str = data['Text']


class SubjectMarkData:
    """
    A class that gives you data about your marks in a specific subject.

    Attributes
    ----------
    subject : :class:`Subject`
        The subject to which the marks belong.
    average : Optional[:class:`float`]
        Your average mark in the subject.
    temporary_mark : Optional[:class:`str`]
        Your temporary mark in the subject.
    subject_note : Optional[:class:`str`]
        The note for the subject.
    temporary_mark_note : Optional[:class:`str`]
        The note for the temporary mark.
    """
    def __init__(self, http: HTTPClient, data: Dict[str, Any]):
        self._http: HTTPClient = http
        self._mark_data = data['Marks']

        subject_information: Dict[str, Any] = {
            'SubjectID': data['Subject']['Id'],
            'SubjectAbbrev': data['Subject']['Abbrev'],
            'SubjectName': data['Subject']['Name']
        }

        self.subject: Subject = Subject(http, subject_information)
        self.average: Optional[float] = None
        self.temporary_mark: Optional[str] = None
        self.subject_note: Optional[str] = None
        self.temporary_mark_note: Optional[str] = None

        if data.get('AverageText'):
            self.average = float(data.pop('AverageText').replace(',', '.'))

        if data.get('TemporaryMark'):
            self.temporary_mark = data.pop('TemporaryMark')

        if data.get('SubjectNote'):
            self.subject_note = data.pop('SubjectNote')

        if data.get('TemporaryMarkNote'):
            self.temporary_mark_note = data.pop('TemporaryMarkNote')

        self.points_only: bool = data['PointsOnly']
        self.mark_prediction_enabled: bool = data['MarkPredictionEnabled']
        self.marks: List[Union[Mark, PredictionMark]] = [Mark(mark_information, self.subject) for mark_information in data['Marks']]

    def __repr__(self):
        return (
            f'<SubjectMarkData subject={self.subject}>'
        )

    def add_mark(
            self,
            *,
            mark: Union[int, Literal['1-', '2-', '3-', '4-']],
            weight: int
    ):
        """
        Adds a mark to the mark data.

        Parameters
        ----------
        mark : Union[:class:`int`, Literal['1-, '2-', '3-', '4-']]
            The mark you want to add.
        weight : :class:`int`
            The weight of the new mark.
        """
        self.marks.append(PredictionMark(mark=mark, weight=weight))

    def edit_mark(
            self,
            index: int,
            *,
            mark: Optional[Union[int, Literal['1', '1-', '2', '2-', '3', '3-', '4', '4-', '5']]] = None,
            weight: Optional[int] = None
    ):
        """
        Edits a mark at the given index.

        Parameters
        ----------
        index : :class:`int`
            The index of the mark you want to edit.
        mark : Optional[Union[:class:`int`, Literal['1-', '2-', '3-', '4-']]]
            The new mark.
        weight : Optional[:class:`int`]
            The weight of the edited mark.

        Raises
        ------
        :class:`IndexError`
            The index of the mark is out of range.
        """
        try:
            if mark:
                self.marks[index].text = mark
            if weight:
                self.marks[index].weight = weight

        except IndexError:
            raise IndexError('mark index out of range')

    def remove_prediction_mark(self, index: int):
        """
        Removes a mark at the given index.

        Parameters
        ----------
        index : :class:`int`
            The index of the mark you want to remove.
        """
        try:
            if type(self.marks[index]) == PredictionMark:
                del self.marks[index]
        except IndexError:
            pass

    def reset_marks(self):
        """
        Removes any changes that were made to the marks.
        """
        self.marks = [Mark(mark_information, self.subject) for mark_information in self._mark_data]

    async def predict(self) -> float:
        """
        Predicts your average mark.

        Returns
        -------
        :class:`float`
            The average mark that was returned by the API.
        """
        prediction_data = [
            {
                'Id': mark.id,
                'MarkText': mark.text,
                'Weight': mark.weight,
                'MaxPoints': mark.max_points,
                'SubjectId': self.subject.id
            }

            for mark in self.marks
        ]

        data = await self._http.predict(prediction_data)
        return float(data.replace(',', '.'))


class TermMarkData:
    """
    A class that gives you data about your final marks in a specific term.

    Attributes
    ----------
    grade_name : :class:`str`
        The name of the grade.
    grade : :class:`int`
        The number of the grade.
    year_in_school : :class:`int`
        The number of the school year.
    school_year : :class:`str`
        The school year of the term data.
    semester : :class:`str`
        The semester of the term data.
    semester_name : :class:`str`
        The name of the semester.
    repeated : :class:`bool`
        Whether you repeated the term.
    closed : :class:`bool`
        Whether the term is closed.
    achievement_text : :class:`str`
        Unknown
    marks_average : :class:`float`
        The average of your final marks.
    absent_hours : :class:`int`
        The amount of hours that you were absent from.
    not_excused_hours : :class:`int`
        The amount of absent hours that were not excused.
    certificate_date : Optional[:class:`datetime.datetime`]
        The date of the term certificate.
    marks : List[:class:`FinalMark`]
        A list of the final marks.
    """
    def __init__(self, http: HTTPClient, data: Dict[str, Any]):
        self.grade_name: str = data['GradeName']
        self.grade: int = data['Grade']
        self.year_in_school: int = data['YearInSchool']
        self.school_year: str = data['SchoolYear']
        self.semester: str = data['Semester']
        self.semester_name: str = data['SemesterName']
        self.repeated: bool = data['Repeated']
        self.closed: bool = data['Closed']
        self.achievement_text: str = data['AchievementText']
        self.marks_average: float = data['MarksAverage']
        self.absent_hours: int = data['AbsentHours']
        self.not_excused_hours: int = data['NotExcusedHours']
        self.certificate_date: Optional[datetime] = None
        self.marks: List[FinalMark] = []

        if data.get('CertificateDate'):
            self.certificate_date = parser.isoparse(data['CertificateDate'])

        for mark in data['FinalMarks']:
            for subject in data['Subjects']:
                if subject['Id'] == mark['SubjectId']:

                    subject_information: Dict[str, Any] = {
                        'SubjectID': subject['Id'],
                        'SubjectAbbrev': subject['Abbrev'],
                        'SubjectName': subject['Name']
                    }

                    self.marks.append(FinalMark(mark, Subject(http, subject_information)))

    def __repr__(self):
        return (
            f'<TermMarkData grade={self.grade} semester={self.semester} school_year={self.school_year}>'
        )
