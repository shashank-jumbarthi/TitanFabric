from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class Link(Base):
    __tablename__ = "links"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    source_device: Mapped[int] = mapped_column(
        ForeignKey("devices.id")
    )

    destination_device: Mapped[int] = mapped_column(
        ForeignKey("devices.id")
    )

    source_port: Mapped[str] = mapped_column(
        String(100)
    )

    destination_port: Mapped[str] = mapped_column(
        String(100)
    )
