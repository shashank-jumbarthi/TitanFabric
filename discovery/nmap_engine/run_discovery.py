from discovery.nmap_engine.scanner import NmapScanner
from discovery.nmap_engine.inventory_service import InventoryService


scanner = NmapScanner()

devices = scanner.discover(
    "10.0.0.0/24"
)

print("Discovered:")
print(devices)

inventory = InventoryService()

inventory.save_discovered_devices(
    devices
)

print("Devices saved.")
