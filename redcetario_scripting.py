import math
from textwrap import wrap
import ipaddress

class NetworkCalculator2():
    def __init__(self, ip_address, cidr):
        self._address = list(map(int, ip_address.split('.')))
        self._cidr = int(cidr) if cidr else 24
        self.binary_IP = self._dec_to_binary(self._address)
        self._binary_mask = None
        self._negation_mask = None
        self._network = None
        self._broadcast = None

    def print_data(self):
        print(f"Calculating the IP range of {'.'.join(map(str, self._address))}/{self._cidr}")
        print("==================================")
        print(f"Netmask {'.'.join(map(str, self.net_mask))}")
        print(f"Network ID {'.'.join(map(str, self.network_ip))}")
        print(f"Subnet Broadcast address {'.'.join(map(str, self.broadcast_ip))}")
        print(f"Host range {self.host_range}")
        print(f"Max number of hosts {self.number_of_hosts}")

    @property
    def net_mask(self):
        if self._binary_mask is None:
            mask = [0, 0, 0, 0]
            for i in range(self._cidr):
                mask[i // 8] += 1 << (7 - i % 8)
            self._binary_mask = self._dec_to_binary(mask)
            self._negation_mask = self._dec_to_binary(self._calculate_negation_mask(mask))
        return mask

    @property
    def broadcast_ip(self):
        if self._broadcast is None:
            self._broadcast = [
                int(x, 2) | int(y, 2) for x, y in zip(self.binary_IP, self._negation_mask)
            ]
        return self._broadcast

    @property
    def network_ip(self):
        if self._network is None:
            self._network = [
                int(x, 2) & int(y, 2) for x, y in zip(self.binary_IP, self._binary_mask)
            ]
        return self._network

    @property
    def host_range(self):
        min_range = self.network_ip[:]
        min_range[-1] += 1
        max_range = self.broadcast_ip[:]
        max_range[-1] -= 1
        return f"{'.'.join(map(str, min_range))} - {'.'.join(map(str, max_range))}"

    @property
    def number_of_hosts(self):
        return (2 ** sum(x.count('1') for x in self._negation_mask)) - 2

    def _dec_to_binary(self, ip_address):
        return [bin(octet)[2:].zfill(8) for octet in ip_address]

    def _calculate_negation_mask(self, net_mask):
        return [255 - octet for octet in net_mask]

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
            return "CIDR inválido"
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
    
class VLSMCalculator():
    def calculate_vlsm(self, ip_address, string_of_hosts, prefix):
        subnets = []
        network_hosts = string_of_hosts.split(",")
        length_of_subnets = []

        if self._is_address_valid(ip_address) is False:
            return False
        
        if self.is_prefix_correct(prefix) is False:
            return False
        
        if self.is_host_number_correct(string_of_hosts) is False:
            return False
        
        for hosts in network_hosts:
            hosts = int(hosts) + 2
            length_of_subnets.append(self.calculate_nearest_upper_length_subnet(int(hosts)))
        
        length_of_subnets.sort(reverse = True)
        sum_all_hosts = sum(length_of_subnets)

        if prefix == "":
            first_octet = int(ip_address.split(".")[0])
            max_hosts, error_message = self.get_max_hosts(first_octet)
            if max_hosts:
                self.check_and_inject(ip_address, sum_all_hosts)
        else:
            max_hosts = pow(2, 32 - int(prefix))
            error_message = "The number of hosts exceeds the maximum limit for the specified prefix length."
            self.check_and_inject(ip_address, sum_all_hosts, max_hosts, error_message, length_of_subnets, subnets)

        return subnets       

    def get_max_hosts(self, first_octet):
        if 1 <= first_octet < 128:
            return pow(2, 24), "El maximo de host excede el limite para una Red de Clase A (The number of hosts exceeds the maximum limit for Class A network.)"
        elif 128 <= first_octet < 192:
            return pow(2, 16), "El maximo de host excede el limite para una Red de Clase B (The number of hosts exceeds the maximum limit for Class B network.)"
        elif 192 <= first_octet < 224:
            return pow(2, 8), "El maximo de host excede el limite para una Red de Clase C (The number of hosts exceeds the maximum limit for Class C network.)"
        return None, None
    
    def check_and_inject(self, ip_address, sum_all_hosts, max_hosts, error_message, length_of_subnets, subnets):
        if sum_all_hosts <= max_hosts:
            self.inject_data_to_dict(ip_address, length_of_subnets, subnets)
        else:
            print(error_message)
    
    # Function to inject calculated data into a dictionary
    def inject_data_to_dict(self, ip_address, length_of_subnets, subnets):
        for network in length_of_subnets:
            # Calculate the number of host bits and prefix
            hostbits = int(log2(network))
            prefix = 32 - hostbits
            # Calculate subnet mask
            mask = self.get_mask_from_prefix(prefix)

            # Append the subnet information to the list
            subnets.append({
                "Network Address": ip_address,
                "IP Range": f"{self.get_first_addressable_ip(ip_address)} - {self.get_last_addressable_ip(network_ip, mask)}",
                "Broadcast Address": self.get_broadcast_ip(ip_address, mask),
                "Subnet Mask": mask,
                "Prefix": f"/{prefix}",
                "Addressable Hosts": pow(2, hostbits) - 2
            })
            # Get the IP address of the next network
            network_ip = self.get_next_network_ip(ip_address, mask)
    
    def get_mask_from_prefix(self, prefix):
        subnet_mask_dec = ""
        for octet in wrap(("0" * (32 - prefix)).rjust(32, "1"), 8):
            subnet_mask_dec += f"{int(octet, 2)}."
        return subnet_mask_dec[:-1]
    
    def get_first_addressable_ip(self, network_ip):
        first_addressable_ip_bin_32bit = bin(int(self.get_32bit_format(network_ip), 2) +
                                            int("1", 2)).replace("0b", "").rjust(32, "0")
        return self.get_ip_from_32bit_format(first_addressable_ip_bin_32bit)


    def get_last_addressable_ip(self, network_ip, mask):
        broadcast_ip_32bit = self.get_32bit_format(self.get_broadcast_ip(network_ip, mask))
        last_addressable_ip_bin_32bit = bin(int(broadcast_ip_32bit, 2) -
                                            int("1", 2)).replace("0b", "").rjust(32, "0")
        return self.get_ip_from_32bit_format(last_addressable_ip_bin_32bit)
    
    def get_ip_from_32bit_format(self, format_32bit):
        ip_dec = ""
        for octet in wrap(format_32bit, 8):
            ip_dec += f"{int(octet, 2)}."
        return ip_dec[:-1]
    
    def get_32bit_format(ip_address):
        format_32bit = ""
        for octet in ip_address.split("."):
            format_32bit += f'{bin(int(octet)).replace("0b", "").rjust(8, "0")}'
        return format_32bit
    
    def get_broadcast_ip(self, network_ip, mask):
        broadcast_ip_32bit = f"{self.get_32bit_format(network_ip)[:-self.get_32bit_format(mask).count('0')]}" \
                            f"{'1' * self.get_32bit_format(mask).count('0')}"
        return self.get_ip_from_32bit_format(broadcast_ip_32bit)

    def calculate_nearest_upper_length_subnet(number_of_host):
        return 2 ** (number_of_host-1).bit_length()
    
    def _is_address_valid(self, address):
        if address == "":
            return False
        octets = address.split(".")
        if len(octets) != 4:
            return False
        for octet in octets:
            if not octet.isdigit() or int(octet) < 0 or int(octet) > 255:
                return False 
        
        return True
    
    def is_prefix_correct(self, prefix):
        if not prefix.isdigit() or int(prefix) < 0 or int(prefix) > 255:
            return False
        return True
    
    def is_host_number_correct(self, string_of_hosts):
        list_of_hosts = string_of_hosts.split(",")
        for host in list_of_hosts:
            if not host.isdigit() or int(host) <= 0:
                return False
        return True
