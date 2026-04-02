# Network Scanning Project - Beginner Friendly
# Import zaruri libraries
import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import socket
import datetime
import os
from scapy.all import ARP, Ether, srp  # network device detect karne ke liye

class NetworkScannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Network & Port Scanner")
        self.root.geometry("750x600")
        self.root.configure(bg="#2b2b2b") # Dark Mode Background

        # Font settings - UI clean aur professional dikhne ke liye
        font_title = ("Segoe UI", 18, "bold")
        font_label = ("Segoe UI", 12)
        font_button = ("Segoe UI", 12, "bold")

        # Title Label
        title_label = tk.Label(root, text="Network & Port Scanner (Windows 11)", font=font_title, bg="#2b2b2b", fg="#ffffff")
        title_label.pack(pady=15)

        # Input Frame - IP range dalne ka box
        input_frame = tk.Frame(root, bg="#2b2b2b")
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Target IP / Subnet (e.g., 192.168.1.0/24):", bg="#2b2b2b", fg="#ffffff", font=font_label).grid(row=0, column=0, padx=10, pady=5)
        self.ip_entry = tk.Entry(input_frame, width=30, font=font_label)
        self.ip_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Ek default IP range set kar dete hain Windows routers ke liye
        self.ip_entry.insert(0, "192.168.1.0/24") 

        # Checkbox for Port Scan
        self.port_scan_var = tk.BooleanVar()
        self.port_scan_check = tk.Checkbutton(input_frame, text="Scan Ports (1-1024) [Time consuming!]", variable=self.port_scan_var, bg="#2b2b2b", fg="#ffffff", selectcolor="#444444", font=("Segoe UI", 11))
        self.port_scan_check.grid(row=1, column=0, columnspan=2, pady=5)

        # Start Button
        self.start_button = tk.Button(root, text="Start Scan", command=self.start_scan_thread, bg="#4CAF50", fg="white", font=font_button, width=20, relief=tk.FLAT)
        self.start_button.pack(pady=10)

        # Output Text Box (Scrolled Text result dikhane ke liye)
        self.result_box = scrolledtext.ScrolledText(root, width=80, height=18, font=("Consolas", 10), bg="#1e1e1e", fg="#00ff00")
        self.result_box.pack(pady=10, padx=20)

    def print_output(self, text):
        """ 
        GUI textbox me output show karega.
        Aur sath hi ek file (result.txt) me bhi save karega. 
        """
        # Textbox me likhna
        self.result_box.insert(tk.END, text + "\n")
        self.result_box.see(tk.END) # Auto scroll to end
        print(text) # Console me bhi dikhane ke liye
        
        # result.txt me append (jodna) karna
        try:
            with open("result.txt", "a") as f:
                f.write(text + "\n")
        except Exception as e:
            pass # Error handling agar file na bane

    def start_scan_thread(self):
        """ 
        Scanning ko naye Thread me dalta hai, taaki Tkinter UI freeze na ho.
        Agar hum direct call karenge, toh jab tak scan chalega aapki screen 'Not Responding' ho jayegi.
        """
        target_ip = self.ip_entry.get().strip()
        if not target_ip:
            messagebox.showerror("Error", "Please entering a valid IP or Network Range!")
            return

        # Starting state: button disable karo aur purana result clear karo
        self.start_button.config(state=tk.DISABLED, text="Scanning...", bg="#757575")
        self.result_box.delete(1.0, tk.END) 
        
        # Naya thread create karke start kar do
        scan_thread = threading.Thread(target=self.perform_scan, args=(target_ip,))
        scan_thread.daemon = True # Taaki agar hum app close kare, to background thread bhi rukk jaye
        scan_thread.start()

    def get_hostname(self, ip):
        """ Extra feature: IP address se Device ka naam (Hostname) nikalta hai """
        try:
            # gethostbyaddr IP ka host name wapas deta hai tuple me
            hostname, _, _ = socket.gethostbyaddr(ip)
            return hostname
        except socket.herror:
            return "Unknown"

    def scan_ports(self, target_ip):
        """
        Pure Python socket se ports 1-1024 scan karta hai.
        Koi extra software (Nmap) install karne ki zaroorat NAHI hai!
        """
        self.print_output(f"\n--- Port Scan start hua IP: {target_ip} ke liye ---")
        self.print_output("[i] Python socket se scan chal raha hai (ports 1-1024)... Thoda wait karein...")

        open_ports = []
        socket.setdefaulttimeout(0.5)  # Har port ke liye 0.5 sec wait

        for port in range(1, 1025):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((target_ip, port))
                if result == 0:
                    # Port open hai! Service name pata karne ki koshish
                    try:
                        service = socket.getservbyport(port)
                    except:
                        service = "unknown"
                    self.print_output(f"[*] Port {port:>5} OPEN  -> Service: {service}")
                    open_ports.append(port)
                sock.close()
            except Exception:
                pass

        if not open_ports:
            self.print_output("[i] Koi bhi open port nahi mila (1-1024 range mein).")
        else:
            self.print_output(f"\n[+] Total Open Ports mile: {len(open_ports)}")

        self.print_output(f"--- Port Scan finish ho gya! ---\n")

    def perform_scan(self, target_network):
        """ 
        Scapy ka use karke Local area network (LAN) me devices detect karta hai.
        """
        self.print_output(f"============================================================")
        self.print_output(f"Scan Starts at: {datetime.datetime.now()}")
        self.print_output(f"Target Subnet:  {target_network}\n")
        self.print_output(f"{'IP Address':<18} | {'MAC Address':<20} | {'Hostname':<20} | {'Status'}")
        self.print_output("-" * 75)

        try:
            # ARP packet banate hain devices detect karne ke liye
            arp_request = ARP(pdst=target_network)
            broadcast = Ether(dst="ff:ff:ff:ff:ff:ff") # ff:ff:ff:ff:ff:ff sabko msg bhejta hai
            packet = broadcast / arp_request # Dono ko jorh diya

            # Packet bhejna aur response lena (srp = send/receive packet)
            # timeout=2 ka mtlb hai 2 sec wait karega
            result = srp(packet, timeout=2, verbose=False)[0]

            devices_list = []
            for sent, received in result:
                # received.psrc = IP, received.hwsrc = MAC
                devices_list.append({'ip': received.psrc, 'mac': received.hwsrc})

            if not devices_list:
                self.print_output("No devices found! (Ya toh network range galat hai, ya administrator rights nahi hain)")
            else:
                # Jitne devices mile unko output me print karo
                for device in devices_list:
                    ip = device['ip']
                    mac = device['mac']
                    hostname = self.get_hostname(ip)
                    self.print_output(f"{ip:<18} | {mac:<20} | {hostname:<20} | UP")
                    
                    # Agar Port Scan checkbox par tick laga hua hai, tab port scan func. call hoga
                    if self.port_scan_var.get():
                        self.scan_ports(ip)

        except PermissionError:
            self.print_output("\nERROR: Permission denied.")
            self.print_output("Scapy ko chalane ke liye Windows pe Npcap install hona aavashyak hai.")
            self.print_output("Kripya command prompt ko 'Run as Administrator' karke open karein.")
        except Exception as e:
            self.print_output(f"\nOops! Ek network error aagya: {str(e)}")

        self.print_output("-" * 75)
        self.print_output(f"Scan Completed at: {datetime.datetime.now()}")
        self.print_output(f"============================================================")

        # Scanning ke baad button wapas enable karna
        self.start_button.config(state=tk.NORMAL, text="Start Scan", bg="#4CAF50")

if __name__ == "__main__":
    # Tkinter application ko initialize aur run karna
    root = tk.Tk()
    app = NetworkScannerGUI(root)
    root.mainloop()
