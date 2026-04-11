from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models import Guest
from schemas import GuestCreate


async def create_guest(db: AsyncSession, guest_data: GuestCreate) -> Guest:
    db_guest = Guest(
        name=guest_data.name,
        will_attend=guest_data.will_attend,
        drink_preference=guest_data.drink_preference
    )
    db.add(db_guest)
    await db.commit()
    await db.refresh(db_guest)
    return db_guest


async def get_all_guests(db: AsyncSession) -> list[Guest]:
    result = await db.execute(select(Guest).order_by(Guest.created_at.desc()))
    return result.scalars().all()


async def get_guest_by_id(db: AsyncSession, guest_id: int) -> Guest | None:
    result = await db.execute(select(Guest).where(Guest.id == guest_id))
    return result.scalar_one_or_none()


async def get_stats(db: AsyncSession) -> dict:
    total = await db.execute(select(func.count(Guest.id)))
    total_count = total.scalar()
    
    attending = await db.execute(select(func.count(Guest.id)).where(Guest.will_attend == True))
    attending_count = attending.scalar()
    
    not_attending = await db.execute(select(func.count(Guest.id)).where(Guest.will_attend == False))
    not_attending_count = not_attending.scalar()
    
    return {
        "total_guests": total_count or 0,
        "attending": attending_count or 0,
        "not_attending": not_attending_count or 0
    }


async def delete_guest(db: AsyncSession, guest_id: int) -> bool:
    guest = await get_guest_by_id(db, guest_id)
    if guest:
        await db.delete(guest)
        await db.commit()
        return True
    return False
