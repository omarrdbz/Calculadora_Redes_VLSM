import math
from textwrap import wrap

class VLSMCalculator():

    def __init__(self):
        self.error_message= ""

    def calculate_vlsm(self, ip_address, string_of_hosts, prefix):
        subnets = []
        network_hosts = string_of_hosts.split(",")
        length_of_subnets = []

        if self._is_address_valid(ip_address) is False:
            return None, "Dirección IP Inválida.", None
        
        if self.is_prefix_correct(prefix) is False:
            return None, "CIDR Inválido.", None
        
        if self.is_host_number_correct(string_of_hosts) is False:
            return None, "Existen Hosts Inválidos.", None
        
        for hosts in network_hosts:
            hosts = int(hosts) + 2
            length_of_subnets.append(self.calculate_nearest_upper_length_subnet(int(hosts)))
        
        length_of_subnets.sort(reverse = True)
        network_hosts = list(map(int, network_hosts))
        network_hosts.sort(reverse=True)
        sum_all_hosts = sum(length_of_subnets)

        if prefix == "":
            first_octet = int(ip_address.split(".")[0])
            max_hosts, error_message = self.get_max_hosts(first_octet)
            if max_hosts and sum_all_hosts <= max_hosts:
                self.inject_data_to_dict(ip_address, length_of_subnets, subnets)
            else:
                return None, error_message, None
        else:
            max_hosts = pow(2, 32 - int(prefix))
            if sum_all_hosts <= max_hosts:
                self.inject_data_to_dict(ip_address, length_of_subnets, subnets)
            else:
                return None, "La cantidad de Hosts excede el límite especificado por el CIDR.", None
        return subnets , "VLSM Calculado Correctamente.", network_hosts  

    def get_max_hosts(self, first_octet):
        if 1 <= first_octet < 128:
            return pow(2, 24), "El maximo de host excede el límite para una Red de Clase A."
        elif 128 <= first_octet < 192:
            return pow(2, 16), "El maximo de host excede el límite para una Red de Clase B."
        elif 192 <= first_octet < 224:
            return pow(2, 8), "El maximo de host excede el límite para una Red de Clase C."
        return None, "Clase Inválida"
    
    # Function to inject calculated data into a dictionary
    def inject_data_to_dict(self, ip_address, length_of_subnets, subnets):
        for network in length_of_subnets:
            # Calculate the number of host bits and prefix
            hostbits = int(math.log2(network))
            prefix = 32 - hostbits
            # Calculate subnet mask
            mask = self.get_mask_from_prefix(prefix)

            # Append the subnet information to the list
            subnets.append({
                "Dirección de Red": ip_address,
                "Rango de IP": f"{self.get_first_addressable_ip(ip_address)} - {self.get_last_addressable_ip(ip_address, mask)}",
                "Dirección de Broadcast": self.get_broadcast_ip(ip_address, mask),
                "Máscara de Subred": mask,
                "CIDR": f"/{prefix}",
                "Hosts direccionables": pow(2, hostbits) - 2
            })
            # Get the IP address of the next network
            ip_address = self.get_next_network_ip(ip_address, mask)
    
    def get_mask_from_prefix(self, prefix):
        subnet_mask_dec = ""
        for octet in wrap(("0" * (32 - prefix)).rjust(32, "1"), 8):
            subnet_mask_dec += f"{int(octet, 2)}."
        return subnet_mask_dec[:-1]
    
    def get_next_network_ip(self, network_ip, mask):
        broadcast_ip_32bit = self.get_32bit_format(self.get_broadcast_ip(network_ip, mask))
        next_network_ip_32bit = bin(int(broadcast_ip_32bit, 2) +
                                    int("1", 2)).replace("0b", "").rjust(32, "0")
        return self.get_ip_from_32bit_format(next_network_ip_32bit)
    
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
    
    def get_32bit_format(self, ip_address):
        format_32bit = ""
        for octet in ip_address.split("."):
            format_32bit += f'{bin(int(octet)).replace("0b", "").rjust(8, "0")}'
        return format_32bit
    
    def get_broadcast_ip(self, network_ip, mask):
        broadcast_ip_32bit = f"{self.get_32bit_format(network_ip)[:-self.get_32bit_format(mask).count('0')]}" \
                            f"{'1' * self.get_32bit_format(mask).count('0')}"
        return self.get_ip_from_32bit_format(broadcast_ip_32bit)

    def calculate_nearest_upper_length_subnet(self, number_of_host):
        return 2 ** (number_of_host-1).bit_length()
    
    def _is_address_valid(self, address):
        if not address:
            return False
        octets = address.split(".")
        if len(octets) != 4:
            return False
        for octet in octets:
            if not octet.isdigit():
                return False
            num = int(octet)
            if num < 0 or num > 255:
                return False
        return True
    
    def is_prefix_correct(self, prefix):
        if not prefix.isdigit() or int(prefix) < 0 or int(prefix) > 255:
            return False
        return True
    
    def is_host_number_correct(self, string_of_hosts):
        list_of_hosts = string_of_hosts.split(",")
        for host in list_of_hosts:
            if not host.isdigit() or int(host) < 0:
                return False
        return True