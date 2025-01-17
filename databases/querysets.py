from databases.models import *
from sqlalchemy import select, update



async def add_dishes(dish):                                                  
    async with async_session() as session:
        # dish = Dishes(image="images\besh-barmak.png", name="Беш-Бармак", description="Лапша с мясом и луком.", price=330)
        session.add(dish) 
        await session.commit()

async def add_side_dishes(side_dish):
    async with async_session() as session:
        # side_dish = SideDishes(image="images\ris-otvar.png", name="Рис отварной", description="Варнный на пару рис.", price=180)
        session.add(side_dish) 
        await session.commit()

async def add_salads(salad):
    async with async_session() as session:
        # salad = Salads(image="images\cezar.png", name="Цезарь", description="Салат с курицей, гренками, пармезаном и соусом Цезарь.", price=220)
        session.add(salad)
        await session.commit()

async def add_drinks(drink):
    async with async_session() as session:
        # drink = Drinks(image="images\cola.png", name="Coca-Cola", description="Газированный освежающий напиток.", price=120)
        session.add(drink) 
        await session.commit()

async def add_sauces(sauces):
    async with async_session() as session:
        # sauces = Sauces(image="images\tkemali.png", name="Ткемалли", description="Соус из слив, с чесноком, специями и зеленью.", price=80)
        session.add(sauces)
        await session.commit()

async def add_deserts(desert):
    async with async_session() as session:
        # desert = Deserts(image="images\pahlava.png", name="Пахлова", description="Традиционный сладкий десерт, приготовленный из теста фило с орехами и медом.", price=190)
        session.add(desert) 
        await session.commit()



# IN LINE BUTTONS
async def all_dishes():
    async with async_session() as session:
        result = await session.scalars(select(Dishes)) 
        return result 
    
async def all_sidedishes():
    async with async_session() as session:
        result = await session.scalars(select(SideDishes))
        return result

async def all_salads():
    async with async_session() as session:
        result = await session.scalars(select(Salads))
        return result 
    
async def all_drinks():
    async with async_session() as session:
        result = await session.scalars(select(Drinks))
        return result
    
async def all_sauces():
    async with async_session() as session:
        result = await session.scalars(select(Sauces))
        return result
    
async def all_deserts():
    async with async_session() as session:
        result = await session.scalars(select(Deserts)) 
        return result

# DISHES INFOS
async def get_dish_by_id(dish_id):
    async with async_session() as session:
        result = await session.scalar(select(Dishes).where(Dishes.id == dish_id))    
        return result 

async def get_sidedish_by_id(sidedish_id):
    async with async_session() as session:
        result = await session.scalar(select(SideDishes).where(SideDishes.id == sidedish_id)) 
        return result

async def get_salad_by_id(salad_id):
    async with async_session() as session:
        result = await session.scalar(select(Salads).where(Salads.id == salad_id)) 
        return result

async def get_drink_by_id(drink_id):
    async with async_session() as session:
        result = await session.scalar(select(Drinks).where(Drinks.id == drink_id)) 
        return result

async def get_sauce_by_id(sauce_id):
    async with async_session() as session:
        result = await session.scalar(select(Sauces).where(Sauces.id == sauce_id)) 
        return result

async def get_desert_by_id(desert_id):
    async with async_session() as session: 
        result = await session.scalar(select(Deserts).where(Deserts.id == desert_id)) 
        return result
    


# delete 
async def delete_dish(dish_id):
    async with async_session() as session:
        dish = await session.scalar(select(Dishes).where(Dishes.id == dish_id))
        await session.delete(dish)
        await session.commit()

async def delete_sidedish(sidedish_id):
    async with async_session() as session:
        sidedish = await session.scalar(select(SideDishes).where(SideDishes.id == sidedish_id))
        await session.delete(sidedish) 
        await session.commit()

async def delete_salad(salad_id):
    async with async_session() as session:
        salad = await session.scalar(select(Salads).where(Salads.id == salad_id))
        await session.delete(salad)
        await session.commit()

async def delete_drink(drink_id):
    async with async_session() as session:
        drink = await session.scalar(select(Drinks).where(Drinks.id == drink_id))
        await session.delete(drink) 
        await session.commit()

async def delete_sauce(sauce_id): 
    async with async_session() as session:
        sauce = await session.scalar(select(Sauces).where(Sauces.id == sauce_id))
        await session.delete(sauce)
        await session.commit()

async def remove_desert(desert_id):
    async with async_session() as session:
        desert = await session.scalar(select(Deserts).where(Deserts.id == desert_id))
        await session.delete(desert) 
        await session.commit() 



# search by DISH NAME 
async def get_all_dishes_by_name(n): 
    async with async_session() as session:
        dish = await session.scalars(select(Dishes).where(
            Dishes.name.ilike(f"%{n}%")))
            
        sidedish = await session.scalars(select(SideDishes).where(
            SideDishes.name.ilike(f"%{n}%")))
        
        salad = await session.scalars(select(Salads).where(
            Salads.name.ilike(f"%{n}%")))

        drink = await session.scalars(select(Drinks).where(
            Drinks.name.ilike(f"%{n}%")))

        sauce = await session.scalars(select(Sauces).where(
            Sauces.name.ilike(f"%{n}%"))) 

        desert = await session.scalars(select(Deserts).where(
            Deserts.name.ilike(f"%{n}%")))
            
        return dish.all()+sidedish.all()+salad.all()+drink.all()+sauce.all()+desert.all() 