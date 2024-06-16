import tkinter as tk
from VLSM_Calculator import VLSMCalculator

class VLSMCalculatorApp():
    def __init__(self):
        self.vlsm_calc = VLSMCalculator()
        self.window = tk.Tk()
        self.window.title("Calculadora de VLSM")

        # Validaciones de entrada
        vcmd_ip = (self.window.register(self.validate_ip), '%P')
        vcmd_num = (self.window.register(self.validate_num), '%P')

        self.title_label = tk.Label(self.window, text="Calculadora de VLSM", font=("Helvetica", 16, "bold")).pack()

        self.frame = tk.Frame(self.window)
        self.frame.pack()

        # Calculadora de Red
        self.vlsm_info_frame = tk.LabelFrame(self.frame, text="Calculadora VLSM", font=("Helvetica", 8, "bold"))
        self.vlsm_info_frame.grid(row=0, column=0, padx=20, pady=10)

        self.ip_address_label = tk.Label(self.vlsm_info_frame, text="Ingresa la dirección IP:", font=("Helvetica", 8, "bold"))
        self.ip_address_label.grid(row=0, column=0, sticky='W', pady=5)
        self.ip_address_entry = tk.Entry(self.vlsm_info_frame, validate='key', validatecommand=vcmd_ip)
        self.ip_address_entry.grid(row=0, column=1, sticky='W')

        self.cidr_label = tk.Label(self.vlsm_info_frame, text="CIDR(/):", font=("Helvetica", 8, "bold"))
        self.cidr_label.grid(row=0, column=2, sticky='E')
        self.cidr_entry = tk.Entry(self.vlsm_info_frame, validate='key', validatecommand=vcmd_num)
        self.cidr_entry.grid(row=0, column=3, sticky='E')

        self.subnet_num_label = tk.Label(self.vlsm_info_frame, text="Núm. Subredes", font=("Helvetica", 8, "bold"))
        self.subnet_num_label.grid(row=0, column=4, sticky='E', padx=15)
        self.subnet_num_spinbox = tk.Spinbox(self.vlsm_info_frame, from_=1, to=99, validatecommand=vcmd_num)
        self.subnet_num_spinbox.grid(row=0, column=5, sticky='E')

        self.apply_button = tk.Button(self.vlsm_info_frame, text="Aplicar", font=("Helvetica", 8, "bold"), command=self.update_rows)
        self.apply_button.grid(row=0, column=6, padx=15, pady=10)

        self.calculate_vlsm_button = tk.Button(self.vlsm_info_frame, text="Calcular VLSM", font=("Helvetica", 8, "bold"), command=self.calculate_vlsm)
        self.message_label = tk.Label(self.vlsm_info_frame, text="", font=("Helvetica", 8, "bold"), fg="red")

        self.current_rows = 0
        self.titles_added = False
        self.entries = []
        self.labels = []

        self.window.mainloop()

    def add_titles(self):
        titles = [
            "Host deseados", "Host direccionables", "Dirección de Red", 
            "CIDR", "Máscara de Subred", "Rango IP", "Dirección de Broadcast"
        ]
        for i, title in enumerate(titles):
            label = tk.Label(self.vlsm_info_frame, text=title, font=("Arial", 10, "bold"))
            label.grid(row=1, column=i, padx=5, pady=5)
        self.current_rows = 2
        self.titles_added = True

    def update_rows(self):
        if not self.titles_added:
            self.add_titles()

        # Get the number of rows from the spinbox
        num_rows = int(self.subnet_num_spinbox.get()) + 2

        # Add or remove rows to match the desired number
        while self.current_rows < num_rows:
            self.add_row()
            self.current_rows += 1
        while self.current_rows > num_rows:
            self.remove_row()
            self.current_rows -= 1

        self.calculate_vlsm_button.grid(row=self.current_rows, column=0, sticky='W')
        self.message_label.grid(row=self.current_rows, column=1, sticky= 'W', pady = 5,columnspan=3)
        self.message_label.config(text=f"")
    
    def add_row(self):
        # Create a new row with one Entry and six Labels
        entry = tk.Entry(self.vlsm_info_frame)
        entry.grid(row=self.current_rows, column=0, padx=5, pady=5)
        self.entries.append(entry)
        
        label_row = []
        for i in range(1, 7):
            label = tk.Label(self.vlsm_info_frame, text=f"---")
            label.grid(row=self.current_rows, column=i, padx=5, pady=5)
            label_row.append(label)
        self.labels.append(label_row)
    
    def remove_row(self):
        # Remove the last row, ensuring we don't remove the title row
        for widget in self.vlsm_info_frame.grid_slaves(row=self.current_rows - 1):
            widget.grid_forget()
        self.entries.pop()
        self.labels.pop()
    
    def calculate_vlsm(self):
        ip_address = self.ip_address_entry.get()
        cidr = self.cidr_entry.get()
        hosts = ",".join(entry.get() for entry in self.entries)
        
        subnets, message, sorted_hosts = self.vlsm_calc.calculate_vlsm(ip_address, hosts, cidr)
        self.message_label.config(text=message)
        if not subnets:
            self.message_label.config(text=message)
            for i in range(len(self.labels)):
                self.labels[i][0].config(text="---")
                self.labels[i][1].config(text="---")
                self.labels[i][2].config(text="---")
                self.labels[i][3].config(text="---")
                self.labels[i][4].config(text="---")
                self.labels[i][5].config(text="---")
        else:
            for i, subnet in enumerate(subnets):
                entry = self.entries[i]
                entry.delete(0, tk.END)
                entry.insert(0, str(sorted_hosts[i]))
                self.labels[i][0].config(text=subnet["Hosts direccionables"])
                self.labels[i][1].config(text=subnet["Dirección de Red"])
                self.labels[i][2].config(text=subnet["CIDR"])
                self.labels[i][3].config(text=subnet["Máscara de Subred"])
                self.labels[i][4].config(text=subnet["Rango de IP"])
                self.labels[i][5].config(text=subnet["Dirección de Broadcast"])

    
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
    vlsm_calc = VLSMCalculatorApp()