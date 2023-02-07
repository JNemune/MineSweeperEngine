from json import dump, load
from os import listdir, mkdir, path, system

from pyrogram import Client, filters
from pyrogram.types.messages_and_media.message import Message

from classes import Map


class App(object):
    def __init__(self):
        with open(path.join(".", "target", "config.json"), "r") as f:
            config = load(f)
        self.api_id = config["api_id"]
        self.api_hash = config["api_hash"]
        self.admin_id = config["admin_id"]
        self.target1 = config["target1"]
        self.tranc = {
            "⬜️": -1,
            " ": 0,
            "1⃣": 1,
            "2⃣": 2,
            "3⃣": 3,
            "4⃣": 4,
            "5⃣": 5,
            "6⃣": 6,
            "7⃣": 7,
            "8⃣": 8,
            "🔵️": 9,
            "🔴": 9,
        }

        self.app = Client(
            "MineSweeperEngine", api_id=self.api_id, api_hash=self.api_hash
        )

        self.maps = {}

        self.message_manager()
        self.app.run()

    def extractor(self, inp: list):
        out = list()
        for i in inp[:8]:
            for j in i:
                out.append(
                    (
                        int(j.callback_data[-1]),
                        7 - int(j.callback_data[-3]),
                        self.tranc[j.text],
                    )
                )
        return out

    async def game_manager(self, client: Client, m: Message):
        inp = self.extractor(m.reply_markup.inline_keyboard)
        if not path.exists(path.join(".", "data_saver", f"{m.id}")):
            mkdir(path.join(".", "data_saver", f"{m.id}"))
            await m.reply(m.id)
        id = len(listdir(path.join(".", "data_saver", f"{m.id}")))
        with open(path.join(".", "data_saver", f"{m.id}", f"{id:>02}.json"), "w") as f:
            dump(inp, f)

        self.maps[m.id] = self.maps.get(m.id, Map(7, 8, 15)).update(inp)

        for i in self.maps[m.id].moves():
            inline = m.reply_markup.inline_keyboard[7 - i[1]][i[0]]
            if self.tranc[inline.text] == -1:
                try:
                    await client.request_callback_answer(
                        m.chat.id,
                        m.id,
                        inline.callback_data,
                    )
                except TimeoutError:
                    pass

        system("clear")
        print(self.maps[m.id])

    def message_manager(self):
        @self.app.on_edited_message(filters.chat(int(self.target1)))
        async def F_message(client: Client, m: Message):
            if (
                "inline_keyboard" in dir(m.reply_markup)
                and len(m.reply_markup.inline_keyboard) == 10
                and m.text[:11] == "🎮 #Turn: ⁩"
            ):
                await self.game_manager(client, m)

        @self.app.on_message(filters.chat(int(self.target1)))
        async def new_message(client: Client, m: Message):
            if (
                "inline_keyboard" in dir(m.reply_markup)
                and len(m.reply_markup.inline_keyboard) == 10
                and m.text[:11] == "🎮 #Turn: ⁩"
            ):
                await self.game_manager(client, m)


if __name__ == "__main__":
    App()

    # app = Client("MineSweeperEngine")
    # async def main():
    #     async with app:
    #         async for dialog in app.get_dialogs():
    #             print(dialog.chat.title, dialog.chat.first_name, dialog.chat.id)
    # app.run(main())
