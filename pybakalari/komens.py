from __future__ import annotations

import dateutil.parser
from .attachments import Attachment
from .models import Object, Teacher
from typing import Any, Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime
    from .http import HTTPClient


class Message(Object):
    """
    Represents a Bakaláři message.

    .. warning::
        The :attr:`text` attribute does not return raw text.
        It also includes HTML tags which the library does not remove.

    Attributes
    ----------
    id : :class:`str`
        The ID of the message.
    title : :class:`str`
        The title of the message.
    text : :class:`str`
        The text of the message.
    sent_at : :class:`datetime.datetime`
        A date representing when the message was sent.
    attachments : List[:class:`Attachment`]
        A list of attachments that are attached to the message.
    sender : :class:`Teacher`
        The sender of the message.
    relevant_name : :class:`str`
        The name of the relevant person or entity that sent the message.
    sender_type : :class:`str`
        The type of the person that sent the message.
    read : :class:`bool`
        Whether the message was read.
    confirmed : :class:`bool`
        Whether the message was confirmed.
    hidden : :class:`bool`
        Whether the message is hidden.
    can_confirm : :class:`bool`
        Whether you can confirm the message.
    can_answer : :class:`bool`
        Whether you can answer the message.
    can_hide : :class:`bool`
        Whether you can hide the message.
    """
    def __init__(self, http: HTTPClient, data: Dict[str, Any]):
        super().__init__(id=data['Id'])
        self.title: str = data['Title']
        self.text: str = data['Text']
        self.sent_at: datetime = dateutil.parser.isoparse(data['SentDate'])
        self.attachments: List[Attachment] = [Attachment(http, attachment) for attachment in data['Attachments']]
        self.relevant_name: str = data['RelevantName']
        self.sender_type: str = data['RelevantPersonType']
        self.read: bool = data['Read']
        self.confirmed: bool = data['Confirmed']
        self.hidden: bool = data['Hidden']
        self.can_confirm: bool = data['CanConfirm']
        self.can_answer: bool = data['CanAnswer']
        self.can_hide: bool = data['CanHide']

        teacher_information: Dict[str, Any] = {
            'TeacherID': data['Sender']['Id'],
            'TeacherName': data['Sender']['Name']
        }

        self.sender: Teacher = Teacher(teacher_information)

    def __repr__(self):
        return (
            f'<Message id={self.id} title={self.title} sent_at={self.sent_at} sender={self.sender} attachments={self.attachments} '
            f'relevant_name={self.relevant_name} relevant_person_type={self.sender_type}>'
        )
