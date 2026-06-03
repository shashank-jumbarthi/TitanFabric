import nmap


class NmapScanner:

    def __init__(self):
        self.scanner = nmap.PortScanner()

    def discover(self, subnet):

        self.scanner.scan(
            hosts=subnet,
            arguments="-sn"
        )

        devices = []

        for host in self.scanner.all_hosts():

            devices.append({
                "ip": host,
                "state": self.scanner[host].state()
            })

        return devices
