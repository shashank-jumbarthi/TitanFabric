from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    hostname: Mapped[str] = mapped_column(
        String(255)
    )

    ip_address: Mapped[str] = mapped_column(
        String(50),
        unique=True
    )

    vendor: Mapped[str] = mapped_column(
        String(100)
    )

    model: Mapped[str] = mapped_column(
        String(100)
    )

    serial_number: Mapped[str] = mapped_column(
        String(100)
    )
