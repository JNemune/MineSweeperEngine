from json import dump, load
from os import listdir, mkdir, path

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import Client, filters, idle
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
        self.app1 = Client("Account1", api_id=self.api_id, api_hash=self.api_hash)
        self.app2 = Client("Account2", api_id=self.api_id, api_hash=self.api_hash)

        self.tranc = {
            "⬜️": -1,
            "🔲": -1,
            " ": 0,
            "1⃣": 1,
            "1️⃣": 1,
            "2⃣": 2,
            "3⃣": 3,
            "4⃣": 4,
            "5⃣": 5,
            "6⃣": 6,
            "6️⃣": 6,
            "7⃣": 7,
            "8⃣": 8,
            "🔵️": 9,
            "🔴": 9,
        }
        self.maps = {}
        self.move = dict()

        async def new_game():
            await self.app1.send_message(self.target1, "🏆 Play in Minroob League")

        scheduler = AsyncIOScheduler()
        scheduler.add_job(new_game, "interval", seconds=75)
        scheduler.start()

        self.message_manager()
        self.app1.start()
        self.app2.start()
        idle()
        self.app1.stop()
        self.app2.stop()

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

    def turn(self, m: Message):
        try:
            if m.text[9:12] == " ⁩ ":
                return True
            return False
        except:
            return False

    async def game_manager(self, client: Client, m: Message, forced=False):
        if not path.exists(path.join(".", "data_saver", f"{m.id}")):
            mkdir(path.join(".", "data_saver", f"{m.id}"))
            self.maps[m.id] = Map(7, 8, 15)
            self.move[m.id] = []
            # await m.reply(m.id)
        inp = self.extractor(m.reply_markup.inline_keyboard)
        id = len(listdir(path.join(".", "data_saver", f"{m.id}")))
        with open(path.join(".", "data_saver", f"{m.id}", f"{id:>02}.json"), "w") as f:
            dump(inp, f)

        if not self.turn(m) and not forced:
            return

        try:
            next_move = self.move[m.id].pop(0)
        except IndexError:
            self.maps[m.id].update(inp)
            self.move[m.id] = [i for i in self.maps[m.id].moves() if (*i, -1) in inp]
            next_move = self.move[m.id].pop(0)
        inline = m.reply_markup.inline_keyboard[7 - next_move[1]][next_move[0]]
        try:
            await client.request_callback_answer(
                m.chat.id,
                m.id,
                inline.callback_data,
            )
        except TimeoutError:
            pass

    def message_manager(self):
        @self.app1.on_edited_message(filters.chat(int(self.target1)))
        @self.app2.on_edited_message(filters.group)
        async def F_message(client: Client, m: Message):
            if "inline_keyboard" in dir(m.reply_markup):
                match len(m.reply_markup.inline_keyboard):
                    case 10:
                        await self.game_manager(client, m)
                    case 12:
                        del self.maps[m.id]
                        del self.move[m.id]

        @self.app1.on_message(filters.chat(int(self.target1)))
        @self.app2.on_message(filters.group)
        async def new_message(client: Client, m: Message):
            if "inline_keyboard" in dir(m.reply_markup):
                match len(m.reply_markup.inline_keyboard):
                    case 3:
                        try:
                            await client.request_callback_answer(
                                m.chat.id,
                                m.id,
                                m.reply_markup.inline_keyboard[0][0].callback_data,
                            )
                        except:
                            pass
                    case 10:
                        await self.game_manager(client, m)


if __name__ == "__main__":
    App()

    # with open(path.join(".", "target", "config.json"), "r") as f:
    #     config = load(f)
    # api_id = config["api_id"]
    # api_hash = config["api_hash"]
    # admin_id = config["admin_id"]
    # target1 = config["target1"]
    # app1 = Client("MineSweeperEngine", api_id=api_id, api_hash=api_hash)

    # async def main():
    #     async with app1:
    #         async for dialog in app1.get_dialogs():
    #             print(dialog.chat.title, dialog.chat.first_name, dialog.chat.id)

    # app1.run(main())
