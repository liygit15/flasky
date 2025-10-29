from ..db import db
from sqlalchemy.orm import Mapped, mapped_column


class Dog(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name :Mapped[str]
    breed: Mapped[str]
    color: Mapped[str]
    personality: Mapped[str]