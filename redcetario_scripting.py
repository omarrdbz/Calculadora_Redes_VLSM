class NerworkCalculator():
    def __init__(self, ip_address, cdir=24):
        if '/' in ip_address:
            self._address_val, self._cidr = ip_address.split('/')
            self._address = map(int, self._address_val.split('.'))
        else:
            self._address = map(int, ip_address.split('.'))
            self._cidr = cdir
        self.binary_IP = self._dec_to_binary(self._address)
        self.binary_Mask = None
        self.negation_Mask = None
        self.network = None
        self.broadcast = None

    def __printData__(self):
        print ("Calculating the IP range of %s/%s" % (".".join(map(str, self._address)), self._cidr))
        print ("==================================")
        print ("Netmask %s" % (".".join(map(str, self.net_mask()))))
        print ("Network ID %s" % (".".join(map(str, self.network_ip()))))
        print ("Subnet Broadcast address %s" % (".".join(map(str, self.broadcast_ip()))))
        print ("Host range %s" % (self.host_range()))
        print ("Max number of hosts %s" % (self.number_of_host()))

    def net_mask(self):
        mask = [0, 0, 0, 0]
        for i in range(int(self._cidr)):
            mask[i / 8] += 1 << (7 - i % 8)
        self.binary_Mask = self._dec_to_binary(mask)
        self.negation_Mask = self._dec_to_binary(self._negation_mask(mask))
        return mask

    def broadcast_ip(self):
        broadcast = list()
        for x, y in zip(self.binary_IP, self.negation_Mask):
            broadcast.append(int(x, 2) | int(y, 2))
        self.broadcast = broadcast
        return broadcast

    def network_ip(self):
        network = list()
        for x, y in zip(self.binary_IP, self.binary_Mask):
            network.append(int(x, 2) & int(y, 2))
        self.network = network
        return network

    def host_range(self):
        min_range = self.network
        min_range[-1] += 1
        max_range = self.broadcast
        max_range[-1] -= 1
        return "%s - %s" % (".".join(map(str, min_range)), ".".join(map(str, max_range)))

    def number_of_host(self):
        return (2 ** sum(map(lambda x: sum(c == '1' for c in x), self.negation_Mask))) - 2
    
    def calculate_vlsm(self, ip_address, string_of_hosts, prefix):
        subnets = []
        network_hosts = string_of_hosts.split(",")
        length_of_subnets = []

        if self._is_address_valid(ip_address) is False:
            return False
        

    def _dec_to_binary(ip_address):
        return map(lambda x: bin(x)[2:].zfill(8), ip_address)
    
    def _negation_mask(net_mask):
        wild = list()
        for i in net_mask:
            wild.append(255 - int(i))
        return wild
    
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
    
