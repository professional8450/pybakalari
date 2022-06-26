import datetime
from typing import Any, Dict, List, Optional
from dateutil import parser


class AbsenceEntry:
    """
    Represents an absence entry.

    Attributes
    ----------
    date : :class:`datetime.date`
        The date of the absence entry.
    unsolved : :class:`int`
        The number of lessons where the absence has not been resolved yet.
    ok : :class:`int`
        The number of lessons where the absence was marked as 'ok'.
    missed : :class:`int`
        The number of lessons where the absence was marked as 'missed'.
    late : :class:`int`
        The number of lessons where you arrived late.
    soon : :class:`int`
        The number of lessons where you left early.
    school : :class:`int`
        The number of lessons where the absence was due to a school event.
    distance_teaching : :class:`int`
        The number of lessons where you attended the lesson remotely.
    """
    __slots__ = (
        "date",
        "unsolved",
        "ok",
        "missed",
        "late",
        "soon",
        "school",
        "distance_teaching"
    )

    def __init__(self, data: Dict[str, Any]):
        dt: datetime.datetime = parser.isoparse(data["Date"])
        self.date: Optional[datetime.date] = datetime.date(dt.year, dt.month, dt.day)

        self.unsolved: int = data["Unsolved"]
        self.ok: int = data["Ok"]
        self.missed: int = data["Missed"]
        self.late: int = data["Late"]
        self.soon: int = data["Soon"]
        self.school: int = data["School"]
        self.distance_teaching: int = data["DistanceTeaching"]

    def __repr__(self):
        return f"<AbsenceEntry date={self.date}>"


class AbsencePerSubjectEntry:
    """
    Represents an absence entry for a :class:`Subject`.

    .. note::
        The :attr:`lesson_count` attribute represents how many lessons of the
        subject have taken place, not how many lessons you missed.

    Attributes
    ----------
    lesson_count : :class:`int`
        The total amount of lessons for the subject.
    subject : :class:`Subject`
        The absence entry's subject.
    base : :class:`int`
        The number of lessons that you missed.
    late : :class:`int`
        The number of lessons where you arrived late.
    soon : :class:`int`
        The number of lessons where you left early.
    school : :class:`int`
        The number of lessons where the absence was due to a school event.
    distance_teaching : :class:`int`
        The number of lessons where you attended the lesson remotely.
    """
    __slots__ = (
        "lesson_count",
        "subject",
        "base",
        "late",
        "soon",
        "school",
        "distance_teaching"
    )

    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)
        self.lesson_count: int = data["LessonsCount"]
        self.subject: str = data["SubjectName"]
        self.base: int = data["Base"]
        self.late: int = data["Late"]
        self.soon: int = data["Soon"]
        self.school: int = data["School"]
        self.distance_teaching: int = data["DistanceTeaching"]

    def __repr__(self):
        return (
            f"<AbsencePerSubjectEntry lesson_count={self.lesson_count} base={self.base} late={self.late} "
            f"soon={self.soon} school={self.school} distance_teaching={self.distance_teaching} subject={self.subject}>"
        )


class AbsenceData:
    """
    A class that gives you data about your absence.

    Attributes
    ----------
    percentage_threshold : :class:`float`
        The absence percentage threshold.
    absences : List[:class:`AbsenceEntry`]
        A list of :class:`AbsenceEntry` objects.
    absences_per_subject : List[:class:`AbsencePerSubjectEntry`]
        A list of :class:`AbsencePerSubjectEntry` objects.

    """

    __slots__ = (
        "percentage_threshold",
        "absences",
        "absences_per_subject"
    )

    def __init__(self, data: Dict[str, Any]):
        self.percentage_threshold: float = data["PercentageThreshold"]
        self.absences: List[AbsenceEntry] = [AbsenceEntry(item) for item in data["Absences"]]
        self.absences_per_subject: List[AbsencePerSubjectEntry] = [AbsencePerSubjectEntry(item) for item in data["AbsencesPerSubject"]]

    def __repr__(self):
        return (
            f"<AbsenceData percentage_threshold={self.percentage_threshold} "
            f"absences={self.absences} absences_per_subject={self.absences_per_subject}"
        )
