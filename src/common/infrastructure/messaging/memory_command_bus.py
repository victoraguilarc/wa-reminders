# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Dict, List, Type, Optional

from src.common.domain.messaging.async_tasks import TaskScheduler
from src.common.domain.messaging.commands import Command, CommandBus, CommandHandler
from src.common.infrastructure.messaging._exceptions import (
    CommandAlreadyExistException,
    CommandHandlerDoesNotExistException,
)


@dataclass
class MemoryCommandBus(CommandBus):
    task_scheduler: Optional[TaskScheduler] = None

    def __post_init__(self):
        self._commands: Dict[Type[Command], CommandHandler] = {}

    def subscribe(self, command: Type[Command], handler: CommandHandler):
        if command in self._commands:
            raise CommandAlreadyExistException
        self._commands[command] = handler

    def dispatch_batch(
        self,
        commands: List[Command],
        is_async: bool = False,
    ):
        for command in commands:
            self.dispatch(command, is_async)

    def dispatch(
        self,
        command: Command,
        run_async: bool = False,
    ):
        if command.__class__ not in self._commands:
            raise CommandHandlerDoesNotExistException(command.__class__)

        if run_async and self.task_scheduler:
            self.task_scheduler.enqueue(command)
            return
        self._commands[command.__class__].execute(command)
