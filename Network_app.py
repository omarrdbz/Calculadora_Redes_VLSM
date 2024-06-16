import tkinter as tk
from Network_Calculator import NetworkCalculator

class NetworkCalculatorApp():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title ("Calculadora de Redes")

        #Validaciones de entrada
        vcmd_ip = (self.window.register(self.validate_ip), '%P')
        vcmd_num = (self.window.register(self.validate_num), '%P')

        self.title_label = tk.Label(self.window, text="Calculadora de Redes", font=("Helvetica", 16, "bold")).pack()

        self.frame = tk.Frame(self.window)
        self.frame.pack()
################################################################################################################################################
        # Calculadora de Red
        self.network_info_frame = tk.LabelFrame(self.frame, text = "Calculadora de Red", font=("Helvetica", 8, "bold"),)
        self.network_info_frame.grid(row= 0, column = 0, padx=20, pady=10)

        self.ip_address_label = tk.Label(self.network_info_frame, text="Ingresa la dirección IP:", font=("Helvetica", 8, "bold"))
        self.ip_address_label.grid(row=0, column=0, sticky= 'W', pady = 5)
        self.ip_address_entry = tk.Entry(self.network_info_frame, validate='key', validatecommand=vcmd_ip)
        self.ip_address_entry.grid(row=0,column=1, sticky= 'W')

        self.cidr_label = tk.Label(self.network_info_frame, text="      CIDR(/):", font=("Helvetica", 8, "bold"))
        self.cidr_label.grid(row=0, column=2, sticky= 'E')
        self.cidr_entry = tk.Entry(self.network_info_frame, validate='key', validatecommand=vcmd_num)
        self.cidr_entry.grid(row=0,column=3, sticky= 'E')

        self.class_label = tk.Label(self.network_info_frame, text="Clase: -/-", font=("Helvetica", 8, "bold"))
        self.class_label.grid(row=0, column = 4, sticky= 'E', padx = 15)

        # Detalles de Red
        self.network_address = tk.Label(self.network_info_frame, text="Dirección IP:", font=("Helvetica", 8, "bold"), anchor = "w")
        self.network_address.grid(row=1, column=0, pady = 3, sticky= 'W')

        self.mask_label = tk.Label(self.network_info_frame, text="Máscara:", font=("Helvetica", 8, "bold"), anchor = "w")
        self.mask_label.grid(row=2, column=0, pady = 3, sticky= 'W')

        self.wild_card_mask_label = tk.Label(self.network_info_frame, text="Wild Card:", font=("Helvetica", 8, "bold"), anchor = "w")
        self.wild_card_mask_label.grid(row=3, column=0, pady = 3, sticky= 'W')
        
        self.network_id_label = tk.Label(self.network_info_frame, text="Dirección de Red:", font=("Helvetica", 8, "bold"),)
        self.network_id_label.grid(row=4, column=0, pady = 3, sticky= 'W')
        
        self.broadcast_label = tk.Label(self.network_info_frame, text="Dirección de Broadcast:", font=("Helvetica", 8, "bold"),)
        self.broadcast_label.grid(row=5, column=0, pady = 3, sticky= 'W')
        
        self.host_range_label = tk.Label(self.network_info_frame, text="Rango de Hosts:", font=("Helvetica", 8, "bold"),)
        self.host_range_label.grid(row=6, column=0, pady = 3, sticky= 'W')
        
        self.host_count_label = tk.Label(self.network_info_frame, text="Núm. Hosts Direccionables:", font=("Helvetica", 8, "bold"),)
        self.host_count_label.grid(row=7, column=0, pady = 3, sticky= 'W')
        
        self.subnet_count_label = tk.Label(self.network_info_frame, text="Núm. Subredes:", font=("Helvetica", 8, "bold"),)
        self.subnet_count_label.grid(row=8, column=0, pady = 3, sticky= 'W')

        self.calculate_network_button = tk.Button(self.network_info_frame, text="Calcular Red", font=("Helvetica", 8, "bold"),command=self.calculate_network)
        self.calculate_network_button.grid(row=9, column=4, padx= 15, pady = 10, sticky= 'E')

        self.network_message_error = tk.Label(self.network_info_frame, text="", font=("Helvetica", 8, "bold"), fg="red")
        self.network_message_error.grid(row=9, column=3, sticky= 'W', pady = 5)

        # Calcular Hosts
        self.calculator_host = tk.Label(self.network_info_frame, text="Calculadora de Host.", font=("Helvetica", 8, "bold"),)
        self.calculator_host.grid(row=10, column=0, sticky= 'W', pady=10)

        self.host_label = tk.Label(self.network_info_frame, text="Ingrese el Número de Host:", font=("Helvetica", 8, "bold"),)
        self.host_label.grid(row=11, column=0, sticky= 'W')
        self.host_entry = tk.Entry(self.network_info_frame, state="disabled", validate='key', validatecommand=vcmd_num)
        self.host_entry.grid(row=11,column=1, sticky= 'W')
        self.host = tk.Label(self.network_info_frame, text="Host:", font=("Helvetica", 8, "bold"),)
        self.host.grid(row=12, column=0, sticky= 'W')

        self.calculate_host_button = tk.Button(self.network_info_frame, text="Calcular Host de Red", font=("Helvetica", 8, "bold"),command=self.calculate_host, state="disabled")
        self.calculate_host_button.grid(row=13, column=4, padx= 15, pady = 10, sticky= 'E')

        self.host_message_error = tk.Label(self.network_info_frame, text="", font=("Helvetica", 8, "bold"), fg="red")
        self.host_message_error.grid(row=13, column=3, sticky= 'W', pady = 5)

        #Calcular Subred
        self.calculate_subnet_and_host = tk.Label(self.network_info_frame, text="Calculadora de Subred y Host de Subred.", font=("Helvetica", 8, "bold"),)
        self.calculate_subnet_and_host.grid(row=14, column=0, sticky= 'W', pady=10)

        self.subnet_label = tk.Label(self.network_info_frame, text="Ingrese el Número de Subred:", font=("Helvetica", 8, "bold"),)
        self.subnet_label.grid(row=15, column=0, sticky= 'W')
        self.subnet_entry = tk.Entry(self.network_info_frame, state="disabled", validate='key', validatecommand=vcmd_num)
        self.subnet_entry.grid(row=15,column=1, sticky= 'W')
        self.subnet = tk.Label(self.network_info_frame, text="Subred:", font=("Helvetica", 8, "bold"),)
        self.subnet.grid(row=16, column=0, sticky= 'W')

        self.calculate_subnet_button = tk.Button(self.network_info_frame, text="Calcular Subred", font=("Helvetica", 8, "bold"),command=self.calculate_subnet, state="disabled")
        self.calculate_subnet_button.grid(row=17, column=4, padx= 15, sticky= 'E')

        self.subnet_message_error = tk.Label(self.network_info_frame, text="", font=("Helvetica", 8, "bold"), fg="red")
        self.subnet_message_error.grid(row=17, column=3, sticky= 'W', pady = 5)

        #Calcular Host de Subred 
        self.subnet_host_label = tk.Label(self.network_info_frame, text="Ingrese el Número de Host de Subred:", font=("Helvetica", 8, "bold"),)
        self.subnet_host_label.grid(row=18, column=0, sticky= 'W')
        self.subnet_host_entry = tk.Entry(self.network_info_frame, state="disabled", validate='key', validatecommand=vcmd_num)
        self.subnet_host_entry.grid(row=18,column=1, sticky= 'W')
        self.subnet_host = tk.Label(self.network_info_frame, text="Host de Subred:", font=("Helvetica", 8, "bold"),)
        self.subnet_host.grid(row=19, column=0, sticky= 'W')

        self.calculate_subnet_host_button = tk.Button(self.network_info_frame, text="Calcular Host de Subred", font=("Helvetica", 8, "bold"),command=self.calculate_subnet_host, state="disabled")
        self.calculate_subnet_host_button.grid(row=20, column=4, padx= 15, pady = 10, sticky= 'E')

        self.subnet_host_message_error = tk.Label(self.network_info_frame, text="", font=("Helvetica", 8, "bold"), fg="red")
        self.subnet_host_message_error.grid(row=20, column=3, sticky= 'W', pady = 5)


        #Resultados
        self.network_address_result = tk.Label(self.network_info_frame, text="", anchor = "w")
        self.network_address_result.grid(row=1, column=1, pady = 3, sticky= 'W')
        
        self.mask_label_result = tk.Label(self.network_info_frame, text="", anchor = "w")
        self.mask_label_result.grid(row=2, column=1, pady = 3, sticky= 'W')

        self.wild_card_mask_result = tk.Label(self.network_info_frame, text="", anchor = "w")
        self.wild_card_mask_result.grid(row=3, column=1, pady = 3, sticky= 'W')
        
        self.network_id_label_result = tk.Label(self.network_info_frame, text="", anchor = "w")
        self.network_id_label_result.grid(row=4, column=1, pady = 3, sticky= 'W')
        
        self.broadcast_label_result = tk.Label(self.network_info_frame, text="", anchor = "w")
        self.broadcast_label_result.grid(row=5, column=1, pady = 3, sticky= 'W')

        self.host_range_label_result = tk.Label(self.network_info_frame, text="", anchor = "w")
        self.host_range_label_result.grid(row=6, column=1, pady = 3, sticky= 'W')

        self.host_count_label_result = tk.Label(self.network_info_frame, text="", anchor = "w")
        self.host_count_label_result.grid(row=7, column=1, pady = 3, sticky= 'W')

        self.subnet_count_label_result = tk.Label(self.network_info_frame, text="", anchor = "w")
        self.subnet_count_label_result.grid(row=8, column=1, pady = 3, sticky= 'W')

        self.host_result = tk.Label(self.network_info_frame, text="", anchor = "w")
        self.host_result.grid(row=12, column=1, pady = 3, sticky= 'W')

        self.subnet_result = tk.Label(self.network_info_frame, text="", anchor = "w")
        self.subnet_result.grid(row=16, column=1, pady = 3, sticky= 'W')

        self.subnet_host_result = tk.Label(self.network_info_frame, text="", anchor = "w")
        self.subnet_host_result.grid(row=19, column=1, pady = 3, sticky= 'W')
################################################################################################################################################        
        self.window.mainloop()
    
    def calculate_network(self):
        ip = self.ip_address_entry.get()
        cidr = self.cidr_entry.get()
        self.network_calculator = NetworkCalculator(ip,cidr)
        
        self.host_result.config(text=f'')
        self.subnet_result.config(text=f'')
        self.subnet_host_result.config(text=f'')
        self.subnet_host_entry.config(state="disabled")
        self.calculate_subnet_host_button.config(state="disabled")

        if self.network_calculator.message_error != "":
            self.network_message_error.config(text=f"{self.network_calculator.message_error}")
            self.class_label.config(text=f"Clase: -/-")
            self.network_address_result.config(text=f"---")
            self.mask_label_result.config(text=f"---")
            self.wild_card_mask_result.config(text=f"---")
            self.network_id_label_result.config(text=f"---")
            self.broadcast_label_result.config(text=f"---")
            self.host_range_label_result.config(text=f"---")
            self.host_count_label_result.config(text=f"---")
            self.subnet_count_label_result.config(text=f'---')
            self.host_entry.config(state="disabled")
            self.subnet_entry.config(state="disabled")
            self.calculate_host_button.config(state="disabled")
            self.calculate_subnet_button.config(state="disabled")
            return
        
        # Network Details Output
        self.class_label.config(text=f"Clase: {self.network_calculator.class_type}/{self.network_calculator.default_prefix}")
        self.network_address_result.config(text=f"{self.network_calculator.ip_address_string}/{self.network_calculator.cidr}")
        self.wild_card_mask_result.config(text=f"{self.network_calculator.wild_card}")
        self.mask_label_result.config(text=f"{self.network_calculator.netmask}")
        self.network_id_label_result.config(text=f"{self.network_calculator.network_address}")
        self.broadcast_label_result.config(text=f"{self.network_calculator.broadcast_address}")
        self.host_range_label_result.config(text=f"{self.network_calculator.host_range()}")
        self.host_count_label_result.config(text=f"{self.network_calculator.directionable_hosts:,}")
        self.subnet_count_label_result.config(text=f'{self.network_calculator.num_subnets}')

        self.host_entry.config(state="normal")
        self.calculate_host_button.config(state="active")
        self.network_message_error.config(text=f"")

        if self.network_calculator.has_subnets == True:
            self.subnet_entry.config(state="normal")
            self.calculate_subnet_button.config(state="active")
        else:
            self.subnet_entry.config(state="disabled")
            self.calculate_subnet_button.config(state="disabled")

    def calculate_host(self):
        host = self.host_entry.get()
        result = self.network_calculator.get_host(int(host))
        if result == "Error":
            self.host_message_error.config(text=f"{self.network_calculator.message_error}")
            self.host_result.config(text=f"-")
            return
    
        self.host_message_error.config(text=f"")
        self.host_result.config(text=f"{result}")

    def calculate_subnet(self):
        subnet = self.subnet_entry.get()
        result = self.network_calculator.get_subnet(int(subnet))
        self.subnet_host_result.config(text=f"")
        if result == "Error":
            self.subnet_message_error.config(text=f"{self.network_calculator.message_error}")
            self.subnet_result.config(text=f"-")
            self.subnet_host.config(text=f"Host de Subred:")
            self.subnet_host_entry.config(state="disabled")
            self.calculate_subnet_host_button.config(state="disabled")
            return
    
        self.subnet_message_error.config(text=f"")
        self.subnet_result.config(text=f"{result}/{self.network_calculator.cidr}")
        self.subnet_host.config(text=f"Host de Subred #{subnet}:")
        self.subnet_host_entry.config(state="normal")
        self.calculate_subnet_host_button.config(state="normal")
    
    def calculate_subnet_host(self):
        subnet_host = self.subnet_host_entry.get()
        subnet = self.subnet_entry.get()
        result = self.network_calculator.get_host_subnet(int(subnet_host), int(subnet))
        if result == "Error":
            self.subnet_host_message_error.config(text=f"{self.network_calculator.message_error}")
            self.subnet_host_result.config(text=f"-")
            return
    
        self.subnet_host_message_error.config(text=f"")
        self.subnet_host_result.config(text=f"{result}")
    
    def validate_ip(self, value_if_allowed):
        # Permitir solo números y puntos
        allowed_chars = set("0123456789.")
        if all(char in allowed_chars for char in value_if_allowed):
            return True
        return False
    
    def validate_num(self, value_if_allowed):
        # Permitir solo números
        if value_if_allowed.isdigit() or value_if_allowed == "":
            return True
        return False


if __name__ == "__main__":
    app = NetworkCalculatorApp()