import math
import ipaddress

class NetworkCalculator():
    def __init__(self, ip_address, cidr):
        self.ip_address_string = ip_address
        self.has_subnets = True
        try:
            self.first_octet = int(ip_address.split('.')[0])
            self.class_type = self._get_class_type()
            self.default_prefix = self._get_default_prefix()
            if cidr == "":
                self.cidr = self.default_prefix
            else:
                self.cidr = int(cidr)
            self.num_subnets = 2 ** (self.cidr - self.default_prefix)
            self.subnet_size = 2 ** (32 - self.cidr)
            self.directionable_hosts = self.subnet_size - 2
            self.message_error = self.validate_data()
            if self.message_error == "":
                self.network = ipaddress.ip_network(f"{self.ip_address_string}/{self.cidr}", strict=False)
                self.netmask = self.network.netmask
                self.network_address = self.network.network_address
                self.broadcast_address = self.network.broadcast_address
                self.wild_card = self.get_wildcard_mask()
        except ValueError:
            self.message_error ="IP inválida"

    def _get_class_type(self):
        if 1 <= self.first_octet < 128:
            return 'A'
        elif 128 <= self.first_octet < 192:
            return 'B'
        elif 192 <= self.first_octet < 224:
            return 'C'
        else:
            return 'Unknown'

    def _get_default_prefix(self):
        if self.class_type == 'A':
            return 8
        elif self.class_type == 'B':
            return 16
        elif self.class_type == 'C':
            return 24
        else:
            return 0

    def get_wildcard_mask(self):
        try:
            octets = list(map(int, str(self.network.netmask).split(".")))
        except ValueError:
            return  "IP inválida"
        
        for j in range(len(octets)):
            octets[j] = 255 - octets[j]

        return '.'.join(map(str, octets))
  
    def validate_data(self):
        try:
            octets = list(map(int, self.ip_address_string.split(".")))
        except ValueError:
            return  "IP inválida"

        for octet in octets:
            if octet > 255 or octet < 0:
                return "IP inválida"
        if self.cidr < 0 or self.cidr >32:
            return "CIDR inválido. Debe estar entre 0 y 32"
        if self.cidr < self.default_prefix:
            grouped_subnets = 1 / self.num_subnets
            self.num_subnets = f"Agrupa {int(grouped_subnets)} subredes de /{self.default_prefix}"
            self.has_subnets = False
        return ""
        
    def print_data(self):
        print(f"Calculating the IP range of {self.network}")
        print("==================================")
        print(f"Class Type: {self.class_type}")
        print(f"Default Prefix: {self.default_prefix}")
        print(f"Netmask: {self.netmask}")
        print(f"Network ID: {self.network_address}")
        print(f"Subnet Broadcast address: {self.network.broadcast_address}")
        print(f"Host range: {self.host_range()}")
        print(f"Max number of hosts: {self.subnet_size - 2}")
        print(f"Number of subnets: {self.num_subnets}")

    def host_range(self):
        hosts = list(self.network.hosts())
        return f"{hosts[0]} - {hosts[-1]}" if hosts else "No hosts"

    def get_subnet(self, subnet_index):
        if not (0 < subnet_index <= self.num_subnets):
            self.message_error = f"La subred debe estar entre 1 y {self.num_subnets}"
            return "Error"
        
        # Convert base network to an integer and calculate the subnet offset
        base_network_int = int(self.network.network_address)
        subnet_offset = (subnet_index - 1) * self.subnet_size

        # Calculate the new subnet's network address
        new_subnet_network_int = base_network_int + subnet_offset
        new_subnet_network = ipaddress.ip_network((new_subnet_network_int, self.network.prefixlen), strict=False)

        return str(new_subnet_network.network_address)

    def get_host(self, host_index):
        if not (0 < host_index <= self.subnet_size - 2):
            self.message_error = f"El host debe estar entre 1 y {self.subnet_size - 2}"
            return "Error"
        octets = list(map(int, str(self.network.network_address).split(".")))
        start = 0
        while host_index > 256:
            host_index /= 256
            start += 1
        times = start + 1
        hosts = [0,0,0,0]
        for i in range(0, times):
            hosts[3-start] = math.trunc(host_index)
            start -= 1
            host_index = 256 * (host_index % 1)
        for j in range(len(hosts)):
            hosts[j] = hosts[j] + octets[j]
        return '.'.join(map(str, hosts))

    def get_host_subnet(self, host_index, subnet_index):
        if not (0 < subnet_index <= self.num_subnets):
            self.message_error = f"La subred debe estar entre 1 y {self.num_subnets}"
            return "Error"
        if not (0 < host_index <= self.subnet_size - 2):
            self.message_error = f"El Host debe estar entre 1 y {self.subnet_size - 2}"
            return "Error"
        
        subnet_octets = list(map(int,self.get_subnet(subnet_index).split(".")))
        
        start = 0
        while host_index > 256:
            host_index /= 256
            start += 1
        
        times = start + 1
        hosts = [0,0,0,0]
        for i in range(0, times):
            hosts[3-start] = math.trunc(host_index)
            start -= 1
            host_index = 256 * (host_index % 1)

        for j in range(len(hosts)):
            hosts[j] = hosts[j] + subnet_octets[j]

        return '.'.join(map(str, hosts))