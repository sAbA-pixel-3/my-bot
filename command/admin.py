from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram import F 
from command.keyboards import *
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from config import ADMIN_ID
from databases.querysets import *



admin_router = Router()

async def check_admin(message: Message):
    return message.from_user.id == ADMIN_ID

# ADDING DISHES
class AddDish(StatesGroup):
    d_name = State()
    d_image = State()
    d_description = State()
    d_price = State()

@admin_router.message(Command("add_dish")) 
async def add_dish_admin(message: Message, state: FSMContext):
    if not await check_admin(message):
        await message.answer("Это команда только для админа!") 
        return
    
    await message.answer("Введите название блюда: ")
    await state.set_state(AddDish.d_name)  
@admin_router.message(AddDish.d_name) 
async def add_dish_name(message: Message, state: FSMContext):
    await state.update_data(d_name=message.text) 

    await message.answer("Отправьте фото для блюда: ")
    await state.set_state(AddDish.d_image)  
@admin_router.message(AddDish.d_image)  
async def add_dish_image(message: Message, state: FSMContext):
    await state.update_data(d_image=message.photo[0].file_id)

    await message.answer("Введите описание блюда: ")
    await state.set_state(AddDish.d_description)  
@admin_router.message(AddDish.d_description)  
async def add_dish_description(message: Message, state: FSMContext):
    await state.update_data(d_description=message.text) 

    await message.answer("Введите цену блюда: ")
    await state.set_state(AddDish.d_price)
@admin_router.message(AddDish.d_price)   
async def add_dish_price(message: Message, state: FSMContext):
    await state.update_data(d_price=int(message.text)) 

    data = await state.get_data() 
    dish = Dishes(  
        name=data['d_name'],
        image=data['d_image'],  
        description=data['d_description'], 
        price=data['d_price'])    
    
    await add_dishes(dish)   
    await message.answer(f'Название блюда: {data.get("d_name")}\n'
                         f'Фото блюда: {data.get("d_image")}\n'
                         f'Описание блюда: {data.get("d_description")}\n' 
                         f'Цена блюда: {data.get("d_price")} сом\n' 
                         f'Блюдо добавлен')
    await state.clear() 



# ADDING SIDEDISHES
class AddSidedish(StatesGroup):
    sd_name = State()
    sd_image = State()
    sd_description = State()
    sd_price = State()

@admin_router.message(Command("add_sidedish")) 
async def add_sidedish_admin(message: Message, state: FSMContext):
    if not await check_admin(message):
        await message.answer("Это команда только для админа!") 
        return
    
    await message.answer("Введите название гарнира: ")
    await state.set_state(AddSidedish.sd_name)  
@admin_router.message(AddSidedish.sd_name) 
async def add_sidedish_name(message: Message, state: FSMContext):
    await state.update_data(sd_name=message.text) 

    await message.answer("Отправьте фото для гарнира: ")
    await state.set_state(AddSidedish.sd_image)  
@admin_router.message(AddSidedish.sd_image)  
async def add_sidedish_image(message: Message, state: FSMContext):
    await state.update_data(sd_image=message.photo[0].file_id)

    await message.answer("Введите описание гарнира: ")
    await state.set_state(AddSidedish.sd_description)  
@admin_router.message(AddSidedish.sd_description)  
async def add_sidedish_description(message: Message, state: FSMContext):
    await state.update_data(sd_description=message.text) 

    await message.answer("Введите цену гарнира: ")
    await state.set_state(AddSidedish.sd_price)
@admin_router.message(AddSidedish.sd_price)   
async def add_sidedish_price(message: Message, state: FSMContext):
    await state.update_data(sd_price=int(message.text)) 

    data = await state.get_data()
    sidedish = SideDishes(   
        name=data['sd_name'],
        image=data['sd_image'],  
        description=data['sd_description'], 
        price=data['sd_price'])    
    
    await add_side_dishes(sidedish)   
    await message.answer(f'Название гарнира: {data.get("sd_name")}\n'
                         f'Фото гарнира: {data.get("sd_image")}\n'
                         f'Описание гарнира: {data.get("sd_description")}\n' 
                         f'Цена гарнира: {data.get("sd_price")} сом\n' 
                         f'Гарнир добавлен')
    await state.clear() 



# ADDING SALADS
class AddSalad(StatesGroup):
    s_name = State()
    s_image = State()
    s_description = State()
    s_price = State()

@admin_router.message(Command("add_salad")) 
async def add_salad_admin(message: Message, state: FSMContext):
    if not await check_admin(message):
        await message.answer("Это команда только для админа!") 
        return
    
    await message.answer("Введите название салата: ")
    await state.set_state(AddSalad.s_name)  
@admin_router.message(AddSalad.s_name) 
async def add_salad_name(message: Message, state: FSMContext):
    await state.update_data(s_name=message.text) 

    await message.answer("Отправьте фото для салата: ")
    await state.set_state(AddSalad.s_image)  
@admin_router.message(AddSalad.s_image)  
async def add_salad_image(message: Message, state: FSMContext):
    await state.update_data(s_image=message.photo[0].file_id)

    await message.answer("Введите описание салата: ")
    await state.set_state(AddSalad.s_description)  
@admin_router.message(AddSalad.s_description)  
async def add_salad_description(message: Message, state: FSMContext):
    await state.update_data(s_description=message.text) 

    await message.answer("Введите цену салата: ")
    await state.set_state(AddSalad.s_price)
@admin_router.message(AddSalad.s_price)   
async def add_salad_price(message: Message, state: FSMContext):
    await state.update_data(s_price=int(message.text)) 

    data = await state.get_data()
    salad = Salads(   
        name=data['s_name'],
        image=data['s_image'],  
        description=data['s_description'], 
        price=data['s_price'])    
    
    await add_salads(salad)    
    await message.answer(f'Название салата: {data.get("s_name")}\n'
                         f'Фото салата: {data.get("s_image")}\n'
                         f'Описание салата: {data.get("s_description")}\n' 
                         f'Цена салата: {data.get("s_price")} сом\n' 
                         f'Салат добавлен')
    await state.clear() 



# ADDING DRINKS
class AddDrink(StatesGroup):
    drink_name = State()
    drink_image = State()
    drink_description = State()
    drink_price = State()

@admin_router.message(Command("add_drink")) 
async def add_drink_admin(message: Message, state: FSMContext):
    if not await check_admin(message):
        await message.answer("Это команда только для админа!") 
        return
    
    await message.answer("Введите название напитка: ")
    await state.set_state(AddDrink.drink_name)  
@admin_router.message(AddDrink.drink_name) 
async def add_drink_name(message: Message, state: FSMContext):
    await state.update_data(drink_name=message.text) 

    await message.answer("Отправьте фото для напитка: ")
    await state.set_state(AddDrink.drink_image)  
@admin_router.message(AddDrink.drink_image)  
async def add_drink_image(message: Message, state: FSMContext):
    await state.update_data(drink_image=message.photo[0].file_id)

    await message.answer("Введите описание напитка: ")
    await state.set_state(AddDrink.drink_description)  
@admin_router.message(AddDrink.drink_description)  
async def add_drink_description(message: Message, state: FSMContext):
    await state.update_data(drink_description=message.text) 

    await message.answer("Введите цену напитка: ")
    await state.set_state(AddDrink.drink_price)
@admin_router.message(AddDrink.drink_price)   
async def add_drink_price(message: Message, state: FSMContext):
    await state.update_data(drink_price=int(message.text)) 

    data = await state.get_data()
    drink = Drinks(    
        name=data['drink_name'],
        image=data['drink_image'],  
        description=data['drink_description'], 
        price=data['drink_price'])    
    
    await add_drinks(drink)     
    await message.answer(f'Название напитка: {data.get("drink_name")}\n'
                         f'Фото напитка: {data.get("drink_image")}\n'
                         f'Описание напитка: {data.get("drink_description")}\n' 
                         f'Цена напитка: {data.get("drink_price")} сом\n' 
                         f'Напиткок добавлен')
    await state.clear() 



# ADDING SAUCES
class AddSauce(StatesGroup): 
    sauce_name = State()
    sauce_image = State()
    sauce_description = State()
    sauce_price = State()

@admin_router.message(Command("add_sauce")) 
async def add_sauce_admin(message: Message, state: FSMContext):
    if not await check_admin(message):
        await message.answer("Это команда только для админа!") 
        return
    
    await message.answer("Введите название соуса: ")
    await state.set_state(AddSauce.sauce_name)  
@admin_router.message(AddSauce.sauce_name) 
async def add_sauce_name(message: Message, state: FSMContext):
    await state.update_data(sauce_name=message.text) 

    await message.answer("Отправьте фото для соуса: ")
    await state.set_state(AddSauce.sauce_image)  
@admin_router.message(AddSauce.sauce_image)  
async def add_sauce_image(message: Message, state: FSMContext):
    await state.update_data(sauce_image=message.photo[0].file_id)

    await message.answer("Введите описание соуса: ")
    await state.set_state(AddSauce.sauce_description)  
@admin_router.message(AddSauce.sauce_description)  
async def add_sauce_description(message: Message, state: FSMContext):
    await state.update_data(sauce_description=message.text) 

    await message.answer("Введите цену соуса: ")
    await state.set_state(AddSauce.sauce_price)
@admin_router.message(AddSauce.sauce_price)   
async def add_sauce_price(message: Message, state: FSMContext):
    await state.update_data(sauce_price=int(message.text)) 

    data = await state.get_data()
    sauce = Sauces(    
        name=data['sauce_name'],
        image=data['sauce_image'],  
        description=data['sauce_description'], 
        price=data['sauce_price'])    
    
    await add_sauces(sauce)      
    await message.answer(f'Название соуса: {data.get("sauce_name")}\n'
                         f'Фото соуса: {data.get("sauce_image")}\n'
                         f'Описание соуса: {data.get("sauce_description")}\n' 
                         f'Цена соуса: {data.get("sauce_price")} сом\n' 
                         f'Соус добавлен')
    await state.clear() 



# ADDING DESERTS
class AddDesert(StatesGroup):
    des_name = State()
    des_image = State()
    des_description = State()
    des_price = State()

@admin_router.message(Command("add_desert")) 
async def add_desert_admin(message: Message, state: FSMContext):
    if not await check_admin(message):
        await message.answer("Это команда только для админа!") 
        return
    
    await message.answer("Введите название десерта: ")
    await state.set_state(AddDesert.des_name)  
@admin_router.message(AddDesert.des_name) 
async def add_desert_name(message: Message, state: FSMContext):
    await state.update_data(des_name=message.text) 

    await message.answer("Отправьте фото для десерта: ")
    await state.set_state(AddDesert.des_image)  
@admin_router.message(AddDesert.des_image)  
async def add_desert_image(message: Message, state: FSMContext):
    await state.update_data(des_image=message.photo[0].file_id)

    await message.answer("Введите описание десерта: ")
    await state.set_state(AddDesert.des_description)  
@admin_router.message(AddDesert.des_description)  
async def add_desert_description(message: Message, state: FSMContext):
    await state.update_data(des_description=message.text) 

    await message.answer("Введите цену десерта: ")
    await state.set_state(AddDesert.des_price)
@admin_router.message(AddDesert.des_price)   
async def add_desert_price(message: Message, state: FSMContext):
    await state.update_data(des_price=int(message.text)) 

    data = await state.get_data()
    desert = Deserts(    
        name=data['des_name'],
        image=data['des_image'],  
        description=data['des_description'], 
        price=data['des_price'])    
    
    await add_deserts(desert)      
    await message.answer(f'Название десерта: {data.get("des_name")}\n'
                         f'Фото десерта: {data.get("des_image")}\n'
                         f'Описание десерта: {data.get("des_description")}\n' 
                         f'Цена десерта: {data.get("des_price")} сом\n' 
                         f'Десерт добавлен')
    await state.clear() 