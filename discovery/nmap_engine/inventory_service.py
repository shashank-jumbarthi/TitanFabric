from database.db import SessionLocal
from database.models.device import Device


class InventoryService:

    def save_discovered_devices(self, devices):

        db = SessionLocal()

        try:

            for item in devices:

                existing = (
                    db.query(Device)
                    .filter(
                        Device.ip_address == item["ip"]
                    )
                    .first()
                )

                if existing:
                    continue

                device = Device(
                    hostname=item["ip"],
                    ip_address=item["ip"],
                    vendor="Unknown",
                    model="Unknown",
                    serial_number="Unknown"
                )

                db.add(device)

            db.commit()

        finally:
            db.close()
