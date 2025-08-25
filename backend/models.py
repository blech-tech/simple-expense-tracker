import uuid
from sqlalchemy import Column, String, Float, UUID

from .database import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = Column(String)
    amount = Column(Float)