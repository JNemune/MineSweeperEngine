import asyncio
from json import dump, load
from os import listdir, mkdir, path

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import Client, filters
from pyrogram.types.messages_and_media.message import Message

from classes import Map


class App(object):
    def __init__(self):
        with open(path.join(".", "target", "config.json"), "r") as f:
            config = load(f)
        self.api_id = config["api_id"]
        self.api_hash = config["api_hash"]
        self.target1 = config["target1"]
        self.admin = config["admin"]
        self.app = Client("Account2", api_id=self.api_id, api_hash=self.api_hash)

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
        self.move = {}
        self.on = True
        self.messages = {}

        async def new_game():
            if self.on:
                await self.app.request_callback_answer("-1001103224082", 196, "jackpot")
                await self.app.send_message(self.target1, "🏆 Play in Minroob League")

        scheduler = AsyncIOScheduler()
        scheduler.add_job(new_game, "interval", seconds=75)
        scheduler.start()

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

    async def turn(self, m: Message):
        user = await self.app.get_users("me")
        first_name = user.first_name
        try:
            if m.text[10 : 11 + len(first_name)] == first_name + " ":
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

        if not await self.turn(m) and not forced:
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
        @self.app.on_edited_message()
        async def F_message(client: Client, m: Message):
            if self.on and "inline_keyboard" in dir(m.reply_markup):
                match len(m.reply_markup.inline_keyboard):
                    case 3 | 4:
                        if m.chat.id == int(self.target1):
                            for_m = await m.forward(self.admin)
                            self.messages[for_m.id] = m.id
                    case 10:
                        await self.game_manager(client, m)
                    case 12:
                        del self.maps[m.id]
                        del self.move[m.id]

        @self.app.on_message(filters.chat(self.admin))
        async def admin_messsage(client: Client, m: Message):
            if m.reply_to_message and m.reply_to_message.forward_from.id == int(
                self.target1
            ):
                answer_id = self.messages[m.reply_to_message.id]
                source_message = await client.get_messages(self.target1, answer_id)
                inline = source_message.reply_markup.inline_keyboard

                await client.request_callback_answer(
                    self.target1,
                    answer_id,
                    inline[0][0].callback_data,
                )
                await asyncio.sleep(3)
                await m.forward(self.target1)

                del self.messages[m.reply_to_message.id]

        @self.app.on_message(filters.me)
        async def on_off(client: Client, m: Message):
            match m.text:
                case "ON":
                    self.on = True
                case "OFF":
                    self.on = False

        @self.app.on_message()
        async def new_message(client: Client, m: Message):
            if self.on and "inline_keyboard" in dir(m.reply_markup):
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
    # target1 = config["target1"]
    # app = Client("MineSweeperEngine", api_id=api_id, api_hash=api_hash)

    # async def main():
    #     async with app:
    #         async for dialog in app.get_dialogs():
    #             print(dialog.chat.title, dialog.chat.first_name, dialog.chat.id)

    # app.run(main())
