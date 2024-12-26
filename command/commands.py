from aiogram import Router 
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram import F 
from command.keyboards import * 
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from collections import defaultdict 
from databases.querysets import *



command_router = Router() 
@command_router.message(Command('start')) 
async def start_handler(message: Message):
    await message.answer(f"Добро пожаловать в ресторан CossoBlanKo! \nЧто бы Вы хотели заказать?", reply_markup=kb)   



@command_router.message(F.text == "Блюда") 
async def dishes_handler(message: Message): 
    await message.answer(f"Блюда:", 
        reply_markup= await get_dishes_kb()) 

@command_router.message(F.text == "Гарниры")
async def sidedishes_handler(message: Message):
    await message.answer(f"Гарниры:",
        reply_markup= await get_sidedishes_kb())
    
@command_router.message(F.text == "Салаты")
async def salads_handler(message: Message):
    await message.answer(f"Салаты:",
        reply_markup= await get_salads_kb())
    
@command_router.message(F.text == "Напитки")
async def drinks_handler(message: Message):
    await message.answer(f"Напитки:",
        reply_markup= await get_drinks_kb())
    
@command_router.message(F.text == "Соусы")
async def sauces_handler(message: Message):
    await message.answer(f"Соусы:",
        reply_markup= await get_sauces_kb())
    
@command_router.message(F.text == "Десерты")
async def deserts_handler(message: Message):
    await message.answer(f"Десерты:",
        reply_markup= await get_deserts_kb()) 



# CALLBACKS
class OrderDish(StatesGroup):
    address = State() 
class OrderSidedish(StatesGroup):
    address = State()
class OrderSalad(StatesGroup):
    address = State()
class OrderDrink(StatesGroup):
    address = State()
class OrderSauce(StatesGroup):
    address = State()
class OrderDesert(StatesGroup):
    address = State() 

user_carts = defaultdict(list)

@command_router.callback_query(F.data.startswith('dish_'))
async def dish_detail_handler(callback: CallbackQuery): 
    dish_id = callback.data.split('_')[1] 
    dish = await get_dish_by_id(dish_id)
    album = MediaGroupBuilder(caption=f'Название: {dish.name}\n'
                                       f'Описание: {dish.description}\n'
                                       f'Цена: {dish.price} сом')  

    if dish.image.startswith('http') or dish.image.startswith('AgA'):
        album.add_photo(media=dish.image) 
    else:
        album.add_photo(media=FSInputFile(dish.image))
    await callback.message.answer_media_group(media=album.build())

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="В корзину", callback_data=f"add_dish_{dish_id}")]])
    await callback.message.answer("Добавить в корзину?\nДля просмотра корзины введите команду /cart", reply_markup=keyboard)

@command_router.callback_query(F.data.startswith("add_dish_"))
async def add_dish_to_cart(callback: CallbackQuery):
    dish_id = callback.data.split("_")[2]
    dish = await get_dish_by_id(dish_id)
    user_id = callback.from_user.id
    user_carts[user_id].append(dish)
    await callback.answer(f"'{dish.name}' добавлено в корзину!", show_alert=True)

@command_router.message(Command("cart")) 
async def view_cart(message: Message):
    user_id = message.from_user.id
    cart = user_carts[user_id]
    if not cart:
        await message.answer("Ваша корзина пуста.")
        return
    
    cart_details = "\n".join([f"{idx+1}. {item.name} - {item.price} сом" for idx, item in enumerate(cart)])
    total_price = sum(item.price for item in cart)
    await message.answer(f"Ваши заказы:\n{cart_details}\n\nОбщая сумма: {total_price} сом")
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Заказать", callback_data="checkout")]])
    await message.answer("Введите адрес для доставки или продолжайте выбирать.", reply_markup=keyboard)

@command_router.callback_query(F.data == "checkout")
async def checkout_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    cart = user_carts[user_id]
    if not cart:
        await callback.message.answer("Ваша корзина пуста.")
        return

    await state.update_data(cart=cart)
    await callback.message.answer("Введите ваш адрес для доставки:")
    await state.set_state(OrderDish.address)

@command_router.message(OrderDish.address)
async def collect_address_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    cart = data.get("cart", [])
    address = message.text 
    cart_details = "\n".join([f"{item.name}" for item in cart])
    total_price = sum(item.price for item in cart)
    await message.answer(
        f"Спасибо за ваш заказ:\n{cart_details}\n\nОбщая сумма: {total_price} сом.\n"
        f"Доставка по адресу: {address} будет осуществлена в течение 1 часа!\n"
        f"Оплата осуществляется наличными или переводом.\nПолную сумму оплачиваете курьеру, после получения заказа!"
        f"Приятного аппетита")
    user_carts[message.from_user.id].clear()  
    await state.clear()



@command_router.callback_query(F.data.startswith('sidedish_'))
async def sidedish_detail_handler(callback: CallbackQuery): 
    sidedish_id = callback.data.split('_')[1] 
    sidedish = await get_sidedish_by_id(sidedish_id) 
    album = MediaGroupBuilder(caption=f'Название: {sidedish.name}\n'
                                        f'Описание: {sidedish.description}\n'
                                        f'Цена: {sidedish.price} сом')  
    
    if sidedish.image.startswith('http') or sidedish.image.startswith('AgA'):
        album.add_photo(media=sidedish.image) 
    else:
        album.add_photo(media=FSInputFile(sidedish.image))
    await callback.message.answer_media_group(media=album.build())

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="В корзину", callback_data=f"add_sidedish_{sidedish_id}")]])
    await callback.message.answer("Добавить в корзину?\nДля просмотра корзины введите команду /cart", reply_markup=keyboard)

@command_router.callback_query(F.data.startswith("add_sidedish_"))
async def add_sidedish_to_cart(callback: CallbackQuery):
    sidedish_id = callback.data.split("_")[2]
    sidedish = await get_sidedish_by_id(sidedish_id)
    user_id = callback.from_user.id
    user_carts[user_id].append(sidedish) 
    await callback.answer(f"'{sidedish.name}' добавлено в корзину!", show_alert=True)

@command_router.message(Command("cart")) 
async def view_cart(message: Message):
    user_id = message.from_user.id
    cart = user_carts[user_id]
    if not cart:
        await message.answer("Ваша корзина пуста.")
        return
    
    cart_details = "\n".join([f"{idx+1}. {item.name} - {item.price} сом" for idx, item in enumerate(cart)])
    total_price = sum(item.price for item in cart)
    await message.answer(f"Ваши заказы:\n{cart_details}\n\nОбщая сумма: {total_price} сом")
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Заказать", callback_data="checkout")]])
    await message.answer("Введите адрес для доставки или продолжайте выбирать.", reply_markup=keyboard)

@command_router.callback_query(F.data == "checkout")
async def checkout_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    cart = user_carts[user_id]
    if not cart:
        await callback.message.answer("Ваша корзина пуста.")
        return

    await state.update_data(cart=cart)
    await callback.message.answer("Введите ваш адрес для доставки:")
    await state.set_state(OrderSidedish.address) 

@command_router.message(OrderSidedish.address) 
async def collect_address_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    cart = data.get("cart", [])
    address = message.text 
    cart_details = "\n".join([f"{item.name}" for item in cart])
    total_price = sum(item.price for item in cart)
    await message.answer(
        f"Спасибо за ваш заказ:\n{cart_details}\n\nОбщая сумма: {total_price} сом.\n"
        f"Доставка по адресу: {address} будет осуществлена в течение 1 часа!\n"
        f"Оплата осуществляется наличными или переводом.\nПолную сумму оплачиваете курьеру, после получения заказа!"
        f"Приятного аппетита")
    user_carts[message.from_user.id].clear()  
    await state.clear()



@command_router.callback_query(F.data.startswith('salad_'))
async def salad_detail_handler(callback: CallbackQuery): 
    salad_id = callback.data.split('_')[1] 
    salad = await get_salad_by_id(salad_id) 
    album = MediaGroupBuilder(caption=f'Название: {salad.name}\n'
                                        f'Описание: {salad.description}\n'
                                        f'Цена: {salad.price} сом')  
    
    if salad.image.startswith('http') or salad.image.startswith('AgA'):
        album.add_photo(media=salad.image) 
    else:
        album.add_photo(media=FSInputFile(salad.image))
    await callback.message.answer_media_group(media=album.build())

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="В корзину", callback_data=f"add_salad_{salad_id}")]])
    await callback.message.answer("Добавить в корзину?\nДля просмотра корзины введите команду /cart", reply_markup=keyboard)

@command_router.callback_query(F.data.startswith("add_salad_"))
async def add_salad_to_cart(callback: CallbackQuery):
    salad_id = callback.data.split("_")[2]
    salad = await get_salad_by_id(salad_id) 
    user_id = callback.from_user.id 
    user_carts[user_id].append(salad)  
    await callback.answer(f"'{salad.name}' добавлено в корзину!", show_alert=True)

@command_router.message(Command("cart")) 
async def view_cart(message: Message):
    user_id = message.from_user.id
    cart = user_carts[user_id]
    if not cart:
        await message.answer("Ваша корзина пуста.")
        return
    
    cart_details = "\n".join([f"{idx+1}. {item.name} - {item.price} сом" for idx, item in enumerate(cart)])
    total_price = sum(item.price for item in cart)
    await message.answer(f"Ваши заказы:\n{cart_details}\n\nОбщая сумма: {total_price} сом")
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Заказать", callback_data="checkout")]])
    await message.answer("Введите адрес для доставки или продолжайте выбирать.", reply_markup=keyboard)

@command_router.callback_query(F.data == "checkout")
async def checkout_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    cart = user_carts[user_id]
    if not cart:
        await callback.message.answer("Ваша корзина пуста.")
        return

    await state.update_data(cart=cart)
    await callback.message.answer("Введите ваш адрес для доставки:")
    await state.set_state(OrderSalad.address) 

@command_router.message(OrderSalad.address) 
async def collect_address_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    cart = data.get("cart", [])
    address = message.text 
    cart_details = "\n".join([f"{item.name}" for item in cart])
    total_price = sum(item.price for item in cart)
    await message.answer(
        f"Спасибо за ваш заказ:\n{cart_details}\n\nОбщая сумма: {total_price} сом.\n"
        f"Доставка по адресу: {address} будет осуществлена в течение 1 часа!\n"
        f"Оплата осуществляется наличными или переводом.\nПолную сумму оплачиваете курьеру, после получения заказа!"
        f"Приятного аппетита")
    user_carts[message.from_user.id].clear()  
    await state.clear()



@command_router.callback_query(F.data.startswith('drink_'))
async def drink_detail_handler(callback: CallbackQuery): 
    drink_id = callback.data.split('_')[1] 
    drink = await get_drink_by_id(drink_id)  
    album = MediaGroupBuilder(caption=f'Название: {drink.name}\n'
                                        f'Описание: {drink.description}\n'
                                        f'Цена: {drink.price} сом')  
    
    if drink.image.startswith('http') or drink.image.startswith('AgA'):
        album.add_photo(media=drink.image) 
    else:
        album.add_photo(media=FSInputFile(drink.image))
    await callback.message.answer_media_group(media=album.build())

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="В корзину", callback_data=f"add_drink_{drink_id}")]])
    await callback.message.answer("Добавить в корзину?\nДля просмотра корзины введите команду /cart", reply_markup=keyboard)

@command_router.callback_query(F.data.startswith("add_drink_"))
async def add_drink_to_cart(callback: CallbackQuery):
    drink_id = callback.data.split("_")[2]
    drink = await get_drink_by_id(drink_id) 
    user_id = callback.from_user.id
    user_carts[user_id].append(drink)  
    await callback.answer(f"'{drink.name}' добавлено в корзину!", show_alert=True)

@command_router.message(Command("cart")) 
async def view_cart(message: Message):
    user_id = message.from_user.id
    cart = user_carts[user_id]
    if not cart:
        await message.answer("Ваша корзина пуста.")
        return
    
    cart_details = "\n".join([f"{idx+1}. {item.name} - {item.price} сом" for idx, item in enumerate(cart)])
    total_price = sum(item.price for item in cart)
    await message.answer(f"Ваши заказы:\n{cart_details}\n\nОбщая сумма: {total_price} сом")
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Заказать", callback_data="checkout")]])
    await message.answer("Введите адрес для доставки или продолжайте выбирать.", reply_markup=keyboard)

@command_router.callback_query(F.data == "checkout")
async def checkout_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    cart = user_carts[user_id]
    if not cart:
        await callback.message.answer("Ваша корзина пуста.")
        return

    await state.update_data(cart=cart)
    await callback.message.answer("Введите ваш адрес для доставки:")
    await state.set_state(OrderDrink.address) 

@command_router.message(OrderDrink.address)  
async def collect_address_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    cart = data.get("cart", [])
    address = message.text 
    cart_details = "\n".join([f"{item.name}" for item in cart])
    total_price = sum(item.price for item in cart)
    await message.answer(
        f"Спасибо за ваш заказ:\n{cart_details}\n\nОбщая сумма: {total_price} сом.\n"
        f"Доставка по адресу: {address} будет осуществлена в течение 1 часа!\n"
        f"Оплата осуществляется наличными или переводом.\nПолную сумму оплачиваете курьеру, после получения заказа!"
        f"Приятного аппетита")
    user_carts[message.from_user.id].clear()  
    await state.clear()



@command_router.callback_query(F.data.startswith('sauce_'))
async def sauce_detail_handler(callback: CallbackQuery): 
    sauce_id = callback.data.split('_')[1] 
    sauce = await get_sauce_by_id(sauce_id)  
    album = MediaGroupBuilder(caption=f'Название: {sauce.name}\n'
                                        f'Описание: {sauce.description}\n'
                                        f'Цена: {sauce.price} сом')  
    
    if sauce.image.startswith('http') or sauce.image.startswith('AgA'):
        album.add_photo(media=sauce.image) 
    else:
        album.add_photo(media=FSInputFile(sauce.image))
    await callback.message.answer_media_group(media=album.build())  

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="В корзину", callback_data=f"add_sauce_{sauce_id}")]])
    await callback.message.answer("Добавить в корзину?\nДля просмотра корзины введите команду /cart", reply_markup=keyboard)

@command_router.callback_query(F.data.startswith("add_sauce_"))
async def add_sauce_to_cart(callback: CallbackQuery):
    sauce_id = callback.data.split("_")[2]
    sauce = await get_sauce_by_id(sauce_id) 
    user_id = callback.from_user.id
    user_carts[user_id].append(sauce)  
    await callback.answer(f"'{sauce.name}' добавлено в корзину!", show_alert=True)

@command_router.message(Command("cart")) 
async def view_cart(message: Message):
    user_id = message.from_user.id
    cart = user_carts[user_id]
    if not cart:
        await message.answer("Ваша корзина пуста.")
        return
    
    cart_details = "\n".join([f"{idx+1}. {item.name} - {item.price} сом" for idx, item in enumerate(cart)])
    total_price = sum(item.price for item in cart)
    await message.answer(f"Ваши заказы:\n{cart_details}\n\nОбщая сумма: {total_price} сом")
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Заказать", callback_data="checkout")]])
    await message.answer("Введите адрес для доставки или продолжайте выбирать.", reply_markup=keyboard)

@command_router.callback_query(F.data == "checkout")
async def checkout_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    cart = user_carts[user_id]
    if not cart:
        await callback.message.answer("Ваша корзина пуста.")
        return

    await state.update_data(cart=cart)
    await callback.message.answer("Введите ваш адрес для доставки:")
    await state.set_state(OrderSauce.address) 

@command_router.message(OrderSauce.address) 
async def collect_address_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    cart = data.get("cart", [])
    address = message.text 
    cart_details = "\n".join([f"{item.name}" for item in cart])
    total_price = sum(item.price for item in cart)
    await message.answer(
        f"Спасибо за ваш заказ:\n{cart_details}\n\nОбщая сумма: {total_price} сом.\n"
        f"Доставка по адресу: {address} будет осуществлена в течение 1 часа!\n"
        f"Оплата осуществляется наличными или переводом.\nПолную сумму оплачиваете курьеру, после получения заказа!"
        f"Приятного аппетита")
    user_carts[message.from_user.id].clear()  
    await state.clear()



@command_router.callback_query(F.data.startswith('desert_'))
async def desert_detail_handler(callback: CallbackQuery): 
    desert_id = callback.data.split('_')[1] 
    desert = await get_desert_by_id(desert_id)  
    album = MediaGroupBuilder(caption=f'Название: {desert.name}\n'
                                        f'Описание: {desert.description}\n'
                                        f'Цена: {desert.price} сом')  
    
    if desert.image.startswith('http') or desert.image.startswith('AgA'):
        album.add_photo(media=desert.image) 
    else:
        album.add_photo(media=FSInputFile(desert.image)) 
    await callback.message.answer_media_group(media=album.build())

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="В корзину", callback_data=f"add_desert_{desert_id}")]])
    await callback.message.answer("Добавить в корзину?\nДля просмотра корзины введите команду /cart", reply_markup=keyboard)

@command_router.callback_query(F.data.startswith("add_desert_"))
async def add_desert_to_cart(callback: CallbackQuery):
    desert_id = callback.data.split("_")[2]
    desert = await get_desert_by_id(desert_id)
    user_id = callback.from_user.id
    user_carts[user_id].append(desert)  
    await callback.answer(f"'{desert.name}' добавлено в корзину!", show_alert=True)

@command_router.message(Command("cart")) 
async def view_cart(message: Message):
    user_id = message.from_user.id
    cart = user_carts[user_id]
    if not cart:
        await message.answer("Ваша корзина пуста.")
        return
    
    cart_details = "\n".join([f"{idx+1}. {item.name} - {item.price} сом" for idx, item in enumerate(cart)])
    total_price = sum(item.price for item in cart)
    await message.answer(f"Ваши заказы:\n{cart_details}\n\nОбщая сумма: {total_price} сом")
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Заказать", callback_data="checkout")]])
    await message.answer("Введите адрес для доставки или продолжайте выбирать.", reply_markup=keyboard)

@command_router.callback_query(F.data == "checkout")
async def checkout_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    cart = user_carts[user_id]
    if not cart:
        await callback.message.answer("Ваша корзина пуста.")
        return

    await state.update_data(cart=cart)
    await callback.message.answer("Введите ваш адрес для доставки:")
    await state.set_state(OrderDesert.address) 

@command_router.message(OrderDesert.address)  
async def collect_address_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    cart = data.get("cart", [])
    address = message.text 
    cart_details = "\n".join([f"{item.name}" for item in cart])
    total_price = sum(item.price for item in cart)
    await message.answer(
        f"Спасибо за ваш заказ:\n{cart_details}\n\nОбщая сумма: {total_price} сом.\n"
        f"Доставка по адресу: {address} будет осуществлена в течение 1 часа!\n"
        f"Оплата осуществляется наличными или переводом.\nПолную сумму оплачиваете курьеру, после получения заказа!"
        f"Приятного аппетита")
    user_carts[message.from_user.id].clear()  
    await state.clear() 


















