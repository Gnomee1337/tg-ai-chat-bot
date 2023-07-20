import random
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database.database import Database
import config
from config import TOKEN

import nest_asyncio

nest_asyncio.apply()

bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

db = Database()