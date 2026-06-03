from discovery.nmap_engine.scanner import NmapScanner

scanner = NmapScanner()

results = scanner.discover(
    "127.0.0.1/32"
)

print(results)
