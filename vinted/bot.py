from mongodb import MongoDB
from settings import DISCORD_TOKEN, DISCORD_ROOM_ID
from vinted_api import VintedApi
from discord.ext import commands, tasks
import discord


class VintedBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._db_client = MongoDB()
        self._api = VintedApi()
        self._channel = None

    async def on_ready(self):
        print(f"{self.user} has connected to Discord!")

        self._channel = self.get_channel(int(DISCORD_ROOM_ID))
        await self._channel.send("Bot is online!")

        # start periodic task
        self.check_for_new_items.start()

    @tasks.loop(seconds=30)
    async def check_for_new_items(self):
        # get url from db
        urls = await self._db_client.get_urls()

        for url in urls:
            items = self._api.search_url(url, per_page=16)

            collection = self._db_client._db['items']

            if items is None:
                continue

            for i in range(len(items)):
                item = items.iloc[i]
                print(item)

                if await collection.find_one({'id_item': int(item['id'])}):
                    continue

                # send message to channel specified in .env
                await self._channel.send(
                    f"{item['url']} with price {item['price']}"
                )

                print(f"Inserting item with id {item['id']} to db")
                await collection.insert_one({'id_item': int(item['id'])})


if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.messages = True  # for on_message event
    intents.guilds = True  # for id of channel

    client = VintedBot(command_prefix="!", intents=intents)
    client.run(DISCORD_TOKEN)
