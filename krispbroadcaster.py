from __future__ import annotations

import asyncio
from typing import List, Union, Any
from contextlib import asynccontextmanager
from broadcaster import Broadcast, Event


class Unsubscribed(Exception):
    pass


class Subscriber:
    def __init__(self, queue):
        self._queue = queue

    async def __aiter__(self):
        try:
            while True:
                yield await self.get()
        except Unsubscribed:
            pass

    async def get(self) -> Event:
        item = await self._queue.get()
        if item is None:
            raise Unsubscribed()
        return item


"""
KrispBroadcast inherits broadcast and add features:
1. add topics
2. subscribe list of channels
"""


class KrispBroadcast(Broadcast):
    async def publish(
        self, channel: str, message: Any, topic: str = ""
    ) -> None:
        # import pdb;
        # pdb.set_trace()
        print("Publishing the message to the channel")
        print(message)
        print(channel)
        await self._backend.publish(f"{topic}:{channel}", message)

    @asynccontextmanager
    async def subscribe(
        self, channel: Union[List[str], str], topic: str = ""
    ) -> "Subscriber":
        queue: asyncio.Queue = asyncio.Queue()
        try:
            if isinstance(channel, str):
                _channel = f"{topic}:{channel}"
                if not self._subscribers.get(_channel):
                    await self._backend.subscribe(_channel)
                    self._subscribers[_channel] = set([queue])
                else:
                    self._subscribers[_channel].add(queue)

                yield Subscriber(queue)

                self._subscribers[_channel].remove(queue)
                if not self._subscribers.get(_channel):
                    del self._subscribers[_channel]
                    await self._backend.unsubscribe(_channel)
            elif isinstance(channel, list):
                for c in channel:
                    _channel = f"{topic}:{c}"
                    if not self._subscribers.get(_channel):
                        await self._backend.subscribe(_channel)
                        self._subscribers[_channel] = set([queue])
                    else:
                        self._subscribers[_channel].add(queue)
                yield Subscriber(queue)
                for c in channel:
                    self._subscribers[_channel].remove(queue)
                    if not self._subscribers.get(_channel):
                        del self._subscribers[_channel]
                        await self._backend.unsubscribe(_channel)
        finally:
            await queue.put(None)
