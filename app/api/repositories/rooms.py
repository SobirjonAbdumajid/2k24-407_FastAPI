import uuid
import time

from fastapi import Depends, HTTPException

from sqlalchemy import text, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.core.database.config import get_general_session, get_sync_session_maker

from app.api.schemas.rooms import RoomsSchema
from app.api.models.rooms import Rooms


class RoomsRepository:
    def __init__(
            self,
            sync_session: Session = Depends(get_sync_session_maker),
            session: AsyncSession = Depends(get_general_session)
    ):
        self.session = session
        self.sync_session = sync_session

    async def get_all_rooms(self):
        raw_sql = text("""
        SELECT m.room_number, s.title as room_type, m.price, f.title as status
        FROM rooms as m
        JOIN rooms_status as f ON m.status = f.id
        JOIN rooms_type as s ON m.room_type = s.id
        """)
        stmt = await self.session.execute(raw_sql)
        return [RoomsSchema.model_validate(map_res) for map_res in stmt.mappings().all()]

    async def get_room(self, room_id: int):
        raw_sql = text("""
        SELECT m.room_number, s.title as room_type, m.price, f.title as status
        FROM rooms as m
        JOIN rooms_status as f ON m.status = f.id
        JOIN rooms_type as s ON m.room_type = s.id
        where m.id = :room_id
        """).bindparams(room_id=room_id)

        stmt = await self.session.execute(raw_sql)
        res = stmt.mappings().first()
        if res is None:
            raise HTTPException(status_code=404, detail="Room not found")
        return RoomsSchema.model_validate(res)

    async def create_room(
            self,
            room_number: int,
            room_type: int,
            price: float,
            status: int
    ):
        celery_tasks_uuid = uuid.uuid4()
        stmt = insert(Rooms).values(
            room_number=room_number,
            room_type=room_type,
            price=price,
            status=status,
            celery_tasks=celery_tasks_uuid,
            tasks_status="PENDING"
        )
        await self.session.execute(stmt)
        await self.session.commit()
        return celery_tasks_uuid

    def update_room(
            self,
            task_id: str
    ):
        time.sleep(10)
        self.sync_session.execute(
            update(Rooms).where(Rooms.celery_tasks == task_id).values(tasks_status="PROCESSING")
        )
        self.sync_session.commit()
        time.sleep(20)
        self.sync_session.execute(
            update(Rooms).where(Rooms.celery_tasks == task_id).values(tasks_status="DONE")
        )
        self.sync_session.commit()
