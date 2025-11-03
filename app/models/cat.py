# class Cat:
#     def __init__(self, id, name, color, personality):
#         self.id = id
#         self.name = name
#         self.color = color
#         self.personality = personality


# cats = [
#     Cat(1, "Luna", "grey", "naughty"),
#     Cat(2, "Morty", "orange", "orange"),
#     Cat(3, "Mimi", "grey", "chill"),
#     Cat(4, "Binx", "black", "hungry")
# ]

from ..db import db
from sqlalchemy.orm import Mapped, mapped_column


class Cat(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] 
    color: Mapped[str] 
    personality: Mapped[str | None]

    def to_dict(self):
        return {
            "id":self.id,
            "name":self.name,
            "color":self.color,
            "personality":self.personality
        }
    @classmethod
    def from_dict(cls, cat_data):
        return cls(
            name=cat_data["name"],
            color=cat_data["color"],
            personality=cat_data["personality"]
        )
    
        # return (cls(cat_data["name"], 
        #     cat_data["color"], 
        #     cat_data["personality"])
        #     )