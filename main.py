#!/usr/bin/python3

import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
from asyncio import new_event_loop, sleep
from asyncio import run_coroutine_threadsafe
from typing import Awaitable
from threading import Thread


DBusGMainLoop(set_as_default=True)

objpath = "/runner"
iface = "org.kde.krunner1"
loop = new_event_loop()
Thread(target=loop.run_forever, daemon=True).start()


def run_in_thread(coro: Awaitable):
    def callback(*args, **kwargs):
        return run_coroutine_threadsafe(coro(*args, *kwargs), loop).result()

    return callback


class Runner(dbus.service.Object):
    def __init__(self):
        dbus.service.Object.__init__(
            self, dbus.service.BusName("org.kde.its_mypic", dbus.SessionBus()), objpath
        )

    @run_in_thread
    async def test(self):
        print("test")
        await sleep(1)
        print("test done")

    @dbus.service.method(iface, in_signature="s", out_signature="a(sssida{sv})")
    def Match(self, query: str):
        """This method is used to get the matches and it returns a list of tupels"""
        if query == "helloo":
            print("Matched")
            self.test()
            # loop.run_until_complete(self.sleep_and_print())
            # data, text, icon, type (KRunner::QueryType), relevance (0-1), properties (subtext, category, multiline(bool) and urls)
            return [
                (
                    "Hello",
                    "Hello from its_mypic!",
                    "document-edit",
                    100,
                    1.0,
                    {"subtext": "Demo Subtext"},
                )
            ]
        return []

    @dbus.service.method(iface, out_signature="a(sss)")
    def Actions(self):
        # id, text, icon
        return [("id", "Tooltip", "planetkde")]

    @dbus.service.method(iface, in_signature="ss")
    def Run(self, data: str, action_id: str):
        print(data, action_id)


runner = Runner()
Gloop = GLib.MainLoop()
Gloop.run()
