from database.base import Base
from database.db import engine

from database.models.device import Device
from database.models.interface import Interface
from database.models.link import Link

Base.metadata.create_all(bind=engine)

print("TitanFabric tables created.")
