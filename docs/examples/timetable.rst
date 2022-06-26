===========
Timetable
===========

The following example details how to retrieve your timetable data with pybakalari.

.. note::
    The following code example assumes that you have already logged in.

.. code-block:: py
    :caption: Code

    import asyncio
    import datetime

    client = pybakalari.Client(route="https://your-url-here.cz")

    async def main():
        ...

        # By default, get_actual_timetable returns the timetable for the current week.
        # However, we can also pass a datetime.date object to get the timetable
        # for the week of a specific date, like so:

        date = datetime.date(year=2022, month=6, day=17)
        days = await client.get_actual_timetable(date=date)

        # get_actual_timetable returns a list of Day objects, so we need to loop
        # through the list:

        for day in days:
            # We can then access the lessons attribute of each day to print out the lessons
            # for the day:

            for lesson in day.lessons:
                print(
                    f'Hour: {lesson.hour.begin_time}-{lesson.hour.end_time}, Subject: {lesson.subject}'
                )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

.. code-block:: text
    :caption: Example output

    2022-06-17 00:00:00+02:00
    Hour: 8:10-8:55, Subject: Český jazyk a literatura
    Hour: 9:05-9:50, Subject: Dějepis
    Hour: 10:00-10:45, Subject: Fyzika
    Hour: 11:00-11:45, Subject: Základy databází
    Hour: 11:55-12:40, Subject: Matematika
    Hour: 13:00-13:45, Subject: Základy síťových technologií
    ...
