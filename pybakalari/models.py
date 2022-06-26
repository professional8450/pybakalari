from typing import Any, Dict, Optional


class ApiInformation:
    """
    A class that gives you information about the API of the Bakaláři server
    that the :class:`Client` is making requests to.

    Attributes
    ----------
    api_version : :class:`str`
        The API version that is being used.
    application_version : :class:`str`
        The application version that is being used.
    base_url : :class:`str`
        The base URL of the Bakaláři server.

    """

    __slots__ = (
        'api_version',
        'application_version',
        'base_url'
    )

    def __init__(self, data: Dict[str, Any]):
        self.api_version: str = data['ApiVersion']
        self.application_version: str = data['ApplicationVersion']
        self.base_url: str = data['BaseUrl']

    def __repr__(self):
        return (
            f'<ApiInformation api_version={self.api_version} application_version={self.application_version} '
            f'base_url={self.base_url}>'
        )


class Object:
    """
    Represents a generic Bakaláři object. Any object that has an ID
    attribute is a subclass of this object.

    Attributes
    ----------
    id : :class:`str`
        The ID of the object.
    """
    def __init__(self, *, id: str):
        self.id: str = id

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and other.id == self.id

    def __ne__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return other.id != self.id
        return True


class Commissioner(Object):
    """
    Represents a GDPR commissioner.

    Attributes
    ----------
    name : :class:`str`
        The name of the commissioner.
    mobile : Optional[:class:`str`]
        The mobile number of the commissioner.
    phone : Optional[:class:`str`]
        The phone number of the commissioner.
    email : Optional[:class:`str`]
        The email of the commissioner.
    web : Optional[:class:`str`]
        The URL of the commissioner's website.
    data_box : Optional[:class:`str`]
        The data box address of the commissioner.
    """
    def __init__(self, data: Dict[str, Any]):
        super().__init__(id=data['Id'])
        self.name: str = data['Name']
        self.mobile: Optional[str] = None
        self.phone: Optional[str] = None
        self.email: Optional[str] = None
        self.web: Optional[str] = None
        self.data_box: Optional[str] = None

        if data.get('Mobile'):
            self.mobile = data.pop('Mobile')

        if data.get('Phone'):
            self.phone = data.pop('Phone')

        if data.get('Email'):
            self.email = data.pop('Email')

        if data.get('Web'):
            self.web = data.pop('Web')

        if data.get('DataBox'):
            self.data_box = data.pop('DataBox')

    def __repr__(self):
        return (
            f'<Commissioner id={self.id} name={self.name} mobile={self.mobile} phone={self.phone} email={self.email} '
            f'web={self.web} data_box={self.data_box}>'
        )


class Class(Object):
    """
    Represents a Bakaláři class.

    Attributes
    ----------
    id : :class:`str`
        The ID of the class.
    abbreviation : Optional[:class:`str`]
        The abbreviation of the class.
    name : Optional[:class:`str`]
        The name of the class.
    """
    __slots__ = (
        'id',
        'abbreviation',
        'name'
    )

    def __init__(self, data: Dict[str, Any]):
        super().__init__(id=data['Id'])
        self.abbreviation: Optional[str] = data.get('Abbrev', None)
        self.name: Optional[str] = data.get('Name', None)

    def __repr__(self):
        return (
            f'<Class id={self.id} abbreviation={self.abbreviation} name={self.name}>'
        )


class Cycle(Object):
    """
    Represents a Bakaláři cycle.

    Attributes
    ----------
    id : :class:`str`
        The ID of the cycle.
    abbreviation : Optional[:class:`str`]
        The abbreviation of the cycle.
    name : Optional[:class:`str`]
        The name of the cycle.
    """
    __slots__ = (
        'id',
        'abbreviation',
        'name'
    )

    def __init__(self, data: Dict[str, Any]):
        super().__init__(id=data['Id'])
        self.abbreviation: Optional[str] = data.get('Abbrev')
        self.name: Optional[str] = data.get('Name')

    def __repr__(self):
        return (
            f'<Cycle id={self.id} abbreviation={self.abbreviation} name={self.name}>'
        )


class Group(Object):
    """
    Represents a Bakaláři group.

    Attributes
    ----------
    id : :class:`str`
        The ID of the group.
    abbreviation : Optional[:class:`str`]
        The abbreviation of the group.
    name : Optional[:class:`str`]
        The name of the group.
    class : Optional[:class:`Class`]
        The class that the group belongs to.
    """
    __slots__ = (
        'id',
        'abbreviation',
        'name',
        'group_class'
    )

    def __init__(self, data: Dict[str, Any]):
        super().__init__(id=data['Id'])
        self.abbreviation: Optional[str] = data.get('Abbrev', None)
        self.name: Optional[str] = data.get('Name', None)
        self.group_class: Optional[Class] = None

        if data.get('Class'):
            self.group_class = Class(data['Class'])

    def __repr__(self):
        return (
            f'<Group id={self.id} abbreviation={self.abbreviation} name={self.name}> group_class={self.group_class}>'
        )


class Room(Object):
    """
    Represents a Bakaláři room.

    Attributes
    ----------
    id : :class:`str`
        The ID of the room.
    abbreviation : Optional[:class:`str`]
        The abbreviation of the room.
    name : Optional[:class:`str`]
        The name of the room.
    """
    __slots__ = (
        'id',
        'abbreviation',
        'name'
    )

    def __init__(self, data: Dict[str, Any]):
        super().__init__(id=data['Id'])
        self.abbreviation: Optional[str] = data.get('Abbrev', None)
        self.name: Optional[str] = data.get('Name', None)

    def __repr__(self):
        return (
            f'<Room id={self.id} abbreviation={self.abbreviation} name={self.name}>'
        )


class Student(Object):
    """
    Represents a Bakaláři student.

    Attributes
    ----------
    id : :class:`str`
        The ID of the student.
    abbreviation : Optional[:class:`str`]
        The abbreviation of the student.
    name : Optional[:class:`str`]
        The name of the student.
    """
    __slots__ = (
        'id',
        'abbreviation',
        'name'
    )

    def __init__(self, data: Dict[str, Any]):
        super().__init__(id=data['Id'])
        self.abbreviation: Optional[str] = data.pop('Abbrev', None)
        self.name: Optional[str] = data.pop('Name', None)

    def __repr__(self):
        return (
            f'<Student id={self.id} abbreviation={self.abbreviation} name={self.name}>'
        )


class User(Object):
    """
    Represents a Bakaláři user.

    Attributes
    ----------
    id : :class:`str`
        The ID of the user.
    name : :class:`str`
        The name of the student.
    school_class : :class:`Class`
        The class of the user.
    school_name : :class:`str`
        The name of the user's school.
    user_type : :class:`str`
        The type of the user.
    user_type_text : :class:`str`
        The description of the type.
    study_year : :class:`int`
        The study year of the user.
    """
    __slots__ = (
        'id',
        'school_class',
        'name',
        'school_name',
        'school_type',
        'user_type',
        'user_type_text',
        'study_year',
        'semester'
    )

    def __init__(self, data: Dict[str, Any]):
        super().__init__(id=data['UserUID'])
        self.name: str = data['FullName']
        self.school_class: Class = Class(data['Class'])
        self.school_name: str = data['SchoolOrganizationName']
        self.school_type: Optional[str] = None
        self.user_type: str = data['UserType']
        self.user_type_text: str = data['UserTypeText']
        self.study_year: int = data['StudyYear']

    def __str__(self):
        return self.name

    def __repr__(self):
        return (
            f'<User id={self.id} name={self.name} school_class={self.school_class} school_type={self.school_type} '
            f'user_type={self.user_type} user_type_text={self.user_type_text} study_year={self.study_year}>'
        )


class Teacher(Object):
    """
    Represents a Bakaláři teacher.

    .. note::
       The :attr:`email`, :attr:`web`, :attr:`school_phone`, :attr:`home_phone` and :attr:`mobile_phone`
       attributes are only filled if you're accessing the ``teacher`` attribute of a :class:`Subject`
       which was retrieved from :meth:`Client.get_subjects`.

    Attributes
    ----------
    id : :class:`str`
        The ID of the teacher.
    name : :class:`str`
        The name of the teacher.
    abbreviation : Optional[:class:`str`]
        The abbreviation of the teacher.
    email : Optional[:class:`str`]
        The email address of the teacher.
    web : Optional[:class:`str`]
        The URL of the teacher's website.
    school_phone : Optional[:class:`str`]
        The school phone number of the teacher.
    home_phone : Optional[:class:`str`]
        The home phone number of the teacher.
    mobile_phone : Optional[:class:`str`]
        The mobile phone number of the teacher.
    """
    __slots__ = (
        'id',
        'name',
        'abbreviation',
        'email',
        'web',
        'school_phone',
        'home_phone',
        'mobile_phone'
    )

    def __init__(self, data: Dict[str, Any]):
        super().__init__(id=data['TeacherID'])
        self.name: str = data['TeacherName']
        self.abbreviation: Optional[str] = None
        self.email: Optional[str] = None
        self.web: Optional[str] = None
        self.school_phone: Optional[str] = None
        self.home_phone: Optional[str] = None
        self.mobile_phone: Optional[str] = None

        if data.get('TeacherAbbrev'):
            self.abbreviation = data.pop('TeacherAbbrev')

        if data.get('TeacherEmail'):
            self.email = data.pop('TeacherEmail')

        if data.get('TeacherWeb'):
            self.web = data.pop('TeacherWeb')

        if data.get('TeacherSchoolPhone'):
            self.school_phone = data.pop('TeacherSchoolPhone')

        if data.get('TeacherHomePhone'):
            self.home_phone = data.pop('TeacherHomePhone')

        if data.get('TeacherMobilePhone'):
            self.mobile_phone = data.pop('TeacherMobilePhone')

    def __str__(self):
        return self.name

    def __repr__(self):
        return (
            f'<Teacher id={self.id} name={self.name} abbreviation={self.abbreviation}>'
        )
