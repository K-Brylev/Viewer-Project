from sqlalchemy import String, Integer, Float, Text, Boolean
from typing import Optional
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

class Base(DeclarativeBase):
    pass

class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    patch: Mapped[Optional[float]] = mapped_column(Float)
    category: Mapped[str] = mapped_column(String)
    icon: Mapped[str] = mapped_column(String)
    tradable: Mapped[bool] = mapped_column(Boolean)
    dyeable: Mapped[bool] = mapped_column(Boolean)
    tags: Mapped[str] = mapped_column(String)

    def __str__(self):
        return f"Item(id:{self.id},name:{self.name},description:{self.description},patch:{self.patch},category:{self.category},tradable:{self.tradable},dyeable:{self.dyeable},tags:{self.tags})"
    def __repr__(self):
        return f"Item(id:{self.id},name:{self.name},description:{self.description},patch:{self.patch},category:{self.category},icon:{self.icon},tradable:{self.tradable},dyeable:{self.dyeable},tags:{self.tags})"