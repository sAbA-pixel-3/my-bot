import asyncio
from aiogram import Bot, Dispatcher
# from databases.models import *
import sys, logging
from config import TOKEN
from command.commands import command_router
from databases.models import create_tables
from databases.querysets import *
from command.admin import *



async def main():

    # await create_tables() 

    # await add_dishes() 
    # await add_side_dishes()
    # await add_salads()
    # await add_drinks()
    # await add_sauces()
    # await add_deserts() 

    bot = Bot(token=TOKEN) 
    dp = Dispatcher() 
    dp.include_routers(command_router, admin_router)
    await dp.start_polling(bot) 

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main()) 