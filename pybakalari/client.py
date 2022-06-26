from .http import HTTPClient
from .models import ApiInformation, Commissioner, User
from .subject import Subject
from .absence import AbsenceData
from .event import Event
from .marks import SubjectMarkData, TermMarkData, PedagogicalMeasure
from .homework import Homework
from .changes import Change
from .timetable import Day, _generate_timetable_data
from .komens import Message
from datetime import datetime
from typing import List, Optional


class Client:
    """
    A class that is used to interact with the Bakaláři API.

    .. note::
        The :attr:`api_version` attribute is set after you call :meth:`Client.login`.

    Parameters
    ----------
    route : :class:`str`
        The URL address of the Bakaláři application that you want to use.

    Attributes
    ----------
    api_version : :class:`str`
        The API version that the Bakaláři server is using.

    """
    def __init__(self, *, route: str):
        self.route: str = route
        self.api_version: Optional[str] = None
        self._http: HTTPClient = HTTPClient(self.route)

    async def login(self, *, username: str, password: str, reauthenticate: Optional[bool] = True) -> str:
        """
        Logs into the Bakaláři API with the credentials provided.
        Returns the token that the API returned.

        Parameters
        ----------
        username : :class:`str`
            The username to use when logging in.
        password : :class:`str`
            The password to use when logging in.
        reauthenticate : Optional[:class:`bool`]
            Whether to re-authenticate automatically after the access to the API expires.

        Raises
        ------
        :class:`BadRequest`
            The username or password were invalid.

        Returns
        -------
        :class:`str`
        """

        token, version = await self._http.api_login(username=username, password=password, refresh=reauthenticate)
        self.api_version = version
        return token

    async def get_subjects(self) -> List[Subject]:
        """
        Retrieve a list of your subjects.

        Returns
        -------
        List[:class:`.Subject`]
        """
        data = await self._http.subjects()
        
        return [Subject(self._http, item) for item in data]

    async def get_absences(self) -> AbsenceData:
        """
        Retrieve your absence data.

        Returns
        -------
        :class:`AbsenceData`
        """
        data = await self._http.absence()
        return AbsenceData(data)

    async def get_api_v3_information(self) -> ApiInformation:
        """
        Retrieve information about the Bakaláři v3 API.

        Returns
        -------
        :class:`ApiInformation`
        """
        data = await self._http.api_v3()
        return ApiInformation(data)

    async def get_api_information(self) -> List[ApiInformation]:
        """
        Retrieve information about each API version being used.

        Returns
        -------
        List[:class:`ApiInformation`]
        """
        data = await self._http.api()
        return [ApiInformation(item) for item in data]

    async def get_marks(self) -> List[SubjectMarkData]:
        """
        Retrieves data about your marks for each subject.

        Returns
        -------
        List[:class:`SubjectMarkData`]
        """
        data = await self._http.marks()
        return [SubjectMarkData(self._http, subject) for subject in data]

    async def get_term_marks(self) -> List[TermMarkData]:
        """
        Retrieves data about your final marks for each term.

        Returns
        -------
        List[:class:`TermMarkData`]
        """
        data = await self._http.marks_final()
        return [TermMarkData(self._http, term) for term in data]

    async def get_pedagogical_measures(self) -> List[PedagogicalMeasure]:
        """
        Retrieves a list of all pedagogical measures given to you.

        Returns
        -------
        List[:class:`PedagogicalMeasure`]
        """
        data = await self._http.marks_measures()
        return [PedagogicalMeasure(measure) for measure in data]

    async def get_new_marks_amount(self) -> int:
        """
        Returns the amount of new marks.

        Returns
        -------
        :class:`int`
        """
        return await self._http.marks_new()

    async def get_all_events(self, *, since: Optional[datetime.date] = None, until: Optional[datetime.date] = None) -> List[Event]:
        """
        Retrieves a list of all events.

        Parameters
        ----------
        since : Optional[:class:`datetime.date`]
            Retrieves events before this date. If you do not provide this parameter, it returns all
            events from the current school year.

        until : Optional[:class:`datetime.date`]
            Retrieves events until this date.

        Returns
        -------
        List[:class:`Event`]
        """
        data = await self._http.events(
            since=str(since) if since else None, 
            until=str(until) if until else None
        )

        return [Event(event) for event in data]

    async def get_public_events(self, *, since: Optional[datetime.date] = None, until: Optional[datetime.date] = None) -> List[Event]:
        """
        Retrieves a list of public events.

        Parameters
        ----------
        since : Optional[:class:`datetime.date`]
            Retrieves events before this date. If you do not provide this parameter, it returns all
            public events from the current school year.

        until : Optional[:class:`datetime.date`]
            Retrieves events until this date.

        Returns
        -------
        List[:class:`Event`]
        """
        data = await self._http.events(
            since=str(since) if since else None, 
            until=str(until) if until else None,
            type='public'
        )

        return [Event(event) for event in data]
    
    async def get_my_events(self, *, since: Optional[datetime.date] = None, until: Optional[datetime.date] = None) -> List[Event]:
        """
        Retrieves a list of your events.

        Parameters
        ----------
        since : Optional[:class:`datetime.date`]
            Retrieves events before this date. If you do not provide this parameter, it returns all
            of your events from the current school year.

        until : Optional[:class:`datetime.date`]
            Retrieves events until this date.

        Returns
        -------
        List[:class:`Event`]
        """
        data = await self._http.events(
            since=str(since) if since else None, 
            until=str(until) if until else None,
            type='my'
        )

        return [Event(event) for event in data]

    async def get_homework(self, *, since: Optional[datetime.date] = None, until: Optional[datetime.date] = None) -> List[Homework]:
        """
        Retrieves a list of your homework.

        Parameters
        ----------
        since : Optional[:class:`datetime.date`]
            Retrieves homework before this date. If you do not provide this parameter, it defaults
            to fourteen days before the current date.

        until : Optional[:class:`datetime.date`]
            Retrieves homework until this date. If you do not provide this parameter, it defaults
            to one day after the current date.

        Returns
        -------
        List[:class:`Homework`]
        """
        data = await self._http.homework(
            since=str(since) if since else None, until=str(until) if until else None
        )
        
        return [Homework(self._http, homework) for homework in data]

    async def get_gdpr_commissioners(self) -> List[Commissioner]:
        """
        Retrieves a list of GDPR commissioners.

        Returns
        -------
        List[:class:`Commissioner`]
        """
        data = await self._http.gdpr_commissioners()
        return [Commissioner(commissioner) for commissioner in data]

    async def get_unclosed_homework_count(self) -> int:
        """
        Returns the amount of your homework that hasn't been completed yet.

        Returns
        -------
        :class:`int`
        """
        return await self._http.homework_unclosed()

    async def get_user(self) -> User:
        """
        Retrieves your user information.

        Returns
        -------
        :class:`User`
        """
        data = await self._http.user()
        return User(data)

    async def get_actual_timetable(self, *, date: Optional[datetime.date] = None) -> List[Day]:
        """
        Retrieves the actual timetable for the current week.
        
        Parameters
        ----------
        date : Optional[:class:`datetime.date`]
            Retrieves the timetable for the week of the date provided.

        Returns
        -------
        List[:class:`Day`]
        """
        data = await self._http.timetable("actual", date=str(date) if date else None)
        return _generate_timetable_data(self._http, data)

    async def get_permanent_timetable(self) -> List[Day]:
        """
        Retrieves the permanent timetable.

        Returns
        -------
        List[:class:`Day`]
        """
        data = await self._http.timetable("public")
        return _generate_timetable_data(self._http, data)

    async def get_timetable_changes(self, *, since: Optional[datetime.date] = None, until: Optional[datetime.date] = None) -> List[Change]:
        """
        Retrieves a list of timetable changes.

        Parameters
        ----------
        since : Optional[:class:`datetime.date`]
            Retrieves homework before this date. If you do not provide this parameter, it defaults
            to fourteen days before the current date.

        until : Optional[:class:`datetime.date`]
            Retrieves homework until this date. If you do not provide this parameter, it defaults
            to one day after the current date.

        Returns
        -------
        List[:class:`Change`]
        """
        data = await self._http.substitutions(
            since=str(since) if since else None, 
            until=str(until) if until else None
        )

        return [Change(change) for change in data]

    async def get_received_messages(self) -> List[Message]:
        """
        Retrieves your received messages.

        Returns
        -------
        List[:class:`Message`]
        """
        data = await self._http.received_messages()
        return [Message(self._http, message) for message in data]

    async def get_noticeboard_messages(self) -> List[Message]:
        """
        Retrieves all messages that are pinned to the noticeboard.

        Returns
        -------
        List[:class:`Message`]
        """
        data = await self._http.noticeboard()
        return [Message(self._http, message) for message in data]

    async def close(self) -> None:
        """
        Closes the client's HTTP session.
        """
        await self._http.close()
