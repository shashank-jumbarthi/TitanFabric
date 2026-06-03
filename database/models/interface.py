from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class Interface(Base):
    __tablename__ = "interfaces"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    device_id: Mapped[int] = mapped_column(
        ForeignKey("devices.id")
    )

    interface_name: Mapped[str] = mapped_column(
        String(100)
    )

    mac_address: Mapped[str] = mapped_column(
        String(50)
    )

    speed: Mapped[str] = mapped_column(
        String(50)
    )

    status: Mapped[str] = mapped_column(
        String(20)
    )
