from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from databases.querysets import *



# Common Button
kb = ReplyKeyboardMarkup(keyboard=[ 
    [KeyboardButton(text='Блюда')],  
    [KeyboardButton(text='Гарниры')],
    [KeyboardButton(text='Салаты')],
    [KeyboardButton(text='Напитки')],
    [KeyboardButton(text='Соусы')],
    [KeyboardButton(text='Десерты')] 
], resize_keyboard=True, input_field_placeholder="Выберите категорию:") 



async def get_dishes_kb():   
    kb = InlineKeyboardBuilder()
    dishes = await all_dishes()
    for dish in dishes: 
        kb.add(InlineKeyboardButton(text=dish.name, 
            callback_data=f"dish_{dish.id}")) 
    return kb.adjust(2).as_markup()

async def get_sidedishes_kb():
    kb = InlineKeyboardBuilder()
    sidedishes = await all_sidedishes()
    for side in sidedishes:
        kb.add(InlineKeyboardButton(text=side.name,
            callback_data=f"sidedish_{side.id}"))
    return kb.adjust(2).as_markup() 

async def get_salads_kb():
    kb = InlineKeyboardBuilder()
    salads = await all_salads()
    for salad in salads: 
        kb.add(InlineKeyboardButton(text=salad.name,
            callback_data=f"salad_{salad.id}"))
    return kb.adjust(2).as_markup()

async def get_drinks_kb():
    kb = InlineKeyboardBuilder()
    drinks = await all_drinks() 
    for drink in drinks: 
        kb.add(InlineKeyboardButton(text=drink.name,
            callback_data=f"drink_{drink.id}"))
    return kb.adjust(2).as_markup()

async def get_sauces_kb(): 
    kb = InlineKeyboardBuilder()
    sauces = await all_sauces() 
    for sauce in sauces:
        kb.add(InlineKeyboardButton(text=sauce.name,
            callback_data=f"sauce_{sauce.id}"))
    return kb.adjust(2).as_markup()

async def get_deserts_kb(): 
    kb = InlineKeyboardBuilder()
    deserts = await all_deserts() 
    for desert in deserts:
        kb.add(InlineKeyboardButton(text=desert.name,
            callback_data=f"desert_{desert.id}"))
    return kb.adjust(2).as_markup()



# ORDER buttons
async def get_dish_order_keyboard(dish_id): 
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="В корзину", 
                callback_data=f"add_dish_{dish_id}")]])

async def get_sidedish_order_keyboard(sidedish_id): 
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="В корзину",
                callback_data=f"add_sidedish_{sidedish_id}")]])

async def get_salad_order_keyboard(salad_id): 
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="В корзину",
                callback_data=f"add_salad_{salad_id}")]])

async def get_drink_order_keyboard(drink_id): 
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="В корзину",
                callback_data=f"add_drink_{drink_id}")]])

async def get_sauce_order_keyboard(sauce_id): 
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="В корзину",
                callback_data=f"add_sauce_{sauce_id}")]])

async def get_desert_order_keyboard(desert_id): 
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="В корзину",
                callback_data=f"add_desert_{desert_id}")]]) 



# FOR DELETING
async def get_dishes_admin_kb():   
    kb = InlineKeyboardBuilder()
    dishes = await all_dishes()
    for dish in dishes: 
        kb.add(InlineKeyboardButton(text=dish.name, 
            callback_data=f"delete_dish_{dish.id}")) 
    return kb.adjust(2).as_markup()

async def get_sidedishes_admin_kb():   
    kb = InlineKeyboardBuilder()
    sidedishes = await all_sidedishes()
    for side in sidedishes: 
        kb.add(InlineKeyboardButton(text=side.name, 
            callback_data=f"delete_sidedish_{side.id}"))  
    return kb.adjust(2).as_markup()

async def get_salad_admin_kb():   
    kb = InlineKeyboardBuilder()
    salads = await all_salads()
    for salad in salads: 
        kb.add(InlineKeyboardButton(text=salad.name, 
            callback_data=f"delete_salad_{salad.id}")) 
    return kb.adjust(2).as_markup()

async def get_drink_admin_kb():   
    kb = InlineKeyboardBuilder()
    drinks = await all_drinks() 
    for drink in drinks: 
        kb.add(InlineKeyboardButton(text=drink.name, 
            callback_data=f"delete_drink_{drink.id}")) 
    return kb.adjust(2).as_markup()

async def get_sauce_admin_kb():   
    kb = InlineKeyboardBuilder()
    sauces = await all_sauces()
    for sauce in sauces: 
        kb.add(InlineKeyboardButton(text=sauce.name, 
            callback_data=f"delete_sauce_{sauce.id}")) 
    return kb.adjust(2).as_markup()

async def get_desert_admin_kb():   
    kb = InlineKeyboardBuilder()
    deserts = await all_deserts()
    for desert in deserts: 
        kb.add(InlineKeyboardButton(text=desert.name, 
            callback_data=f"delete_desert_{desert.id}")) 
    return kb.adjust(2).as_markup()