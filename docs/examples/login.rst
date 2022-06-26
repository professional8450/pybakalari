===========
Login
===========

The following example details how to log into the Bakaláři API with pybakalari.

.. code-block:: py
    :caption: Code

    import asyncio
    import pybakalari

    client = pybakalari.Client(route="https://your-url-here.cz")

    # Since the library is asynchronous, anything we do with
    # our client needs to be inside of an async function.

    async def main():

        # If the credentials you provide are invalid, the library will raise
        # an error.

        await client.login(username="your-username", password="your-password")

        # Once logged in, we can use the other functions of the client.
        # For example, we can use get_user() to print out our own name.

        user = await client.get_user()
        print(user.name)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())