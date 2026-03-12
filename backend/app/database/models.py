from sqlalchemy import String, Integer, Float, Text, Boolean, Computed
from sqlalchemy.dialects.postgresql import TSVECTOR
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
    sub_category: Mapped[Optional[str]] = mapped_column(String)
    icon: Mapped[str] = mapped_column(String)
    outdoor:Mapped[bool] = mapped_column(Boolean)
    tradeable: Mapped[bool] = mapped_column(Boolean)
    dyeable: Mapped[bool] = mapped_column(Boolean)
    tags: Mapped[Optional[str]] = mapped_column(String)
    search_vector : Mapped[str] = mapped_column(
        TSVECTOR, 
        Computed(
            "setweight(to_tsvector('english', coalesce(name,'')), 'A') || "
            "setweight(to_tsvector('english', coalesce(description,'')), 'B') || "
            "setweight(to_tsvector('english', coalesce(tags,'')), 'C') || "
            "setweight(to_tsvector('english', coalesce(category,'')), 'D') || "
            "setweight(to_tsvector('english', coalesce(sub_category,'')), 'D')",
            persisted=True
        )
    )

    def __str__(self):
        return f"Item(id:{self.id},name:{self.name},description:{self.description},patch:{self.patch},category:{self.category},subCategory:{self.sub_category},tradable:{self.tradeable},dyeable:{self.dyeable},tags:{self.tags})"
    def __repr__(self):
        return f"Item(id:{self.id},name:{self.name},description:{self.description},patch:{self.patch},category:{self.category},subCategory:{self.sub_category},icon:{self.icon},tradable:{self.tradeable},dyeable:{self.dyeable},tags:{self.tags})"