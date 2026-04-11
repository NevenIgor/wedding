from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from database import get_db, init_db
from schemas import GuestCreate, GuestResponse, GuestListResponse, StatsResponse
from crud import create_guest, get_all_guests, get_stats, delete_guest
from bot import send_new_guest_notification

app = FastAPI(
    title="Wedding Invitation API",
    description="API для управления гостями свадьбы Антона и Вероники",
    version="1.0.0"
)

# CORS middleware для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене укажите конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Инициализация базы данных при запуске"""
    await init_db()


@app.get("/")
async def root():
    return {
        "message": "Wedding Invitation API",
        "docs": "/docs",
        "endpoints": {
            "guests": "/api/guests",
            "stats": "/api/stats"
        }
    }


@app.post("/api/guests", response_model=GuestResponse, status_code=status.HTTP_201_CREATED)
async def add_guest(guest: GuestCreate, db: AsyncSession = Depends(get_db)):
    """Добавляет нового гостя в базу данных"""
    db_guest = await create_guest(db, guest)
    
    # Отправляем уведомление в Telegram
    await send_new_guest_notification(
        guest_name=guest.name,
        will_attend=guest.will_attend,
        drink_preference=guest.drink_preference
    )
    
    return db_guest


@app.get("/api/guests", response_model=GuestListResponse)
async def list_guests(db: AsyncSession = Depends(get_db)):
    """Получает список всех гостей"""
    guests = await get_all_guests(db)
    return {
        "guests": guests,
        "total": len(guests)
    }


@app.get("/api/guests/{guest_id}", response_model=GuestResponse)
async def get_guest(guest_id: int, db: AsyncSession = Depends(get_db)):
    """Получает информацию о конкретном госте"""
    from crud import get_guest_by_id
    guest = await get_guest_by_id(db, guest_id)
    
    if not guest:
        raise HTTPException(status_code=404, detail="Гость не найден")
    
    return guest


@app.delete("/api/guests/{guest_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_guest(guest_id: int, db: AsyncSession = Depends(get_db)):
    """Удаляет гостя из базы данных"""
    deleted = await delete_guest(db, guest_id)
    
    if not deleted:
        raise HTTPException(status_code=404, detail="Гость не найден")


@app.get("/api/stats", response_model=StatsResponse)
async def get_statistics(db: AsyncSession = Depends(get_db)):
    """Получает статистику по гостям"""
    stats = await get_stats(db)
    return stats


@app.get("/health")
async def health_check():
    """Проверка здоровья сервиса"""
    return {"status": "healthy"}
