import asyncio
from aiogram import Bot, Dispatcher
import sys, logging
from config import TOKEN
from command.commands import command_router
from command.admin import *

  

async def main():
    bot = Bot(token=TOKEN) 
    dp = Dispatcher() 
    dp.include_routers(command_router, admin_router)
    await dp.start_polling(bot) 

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main()) 