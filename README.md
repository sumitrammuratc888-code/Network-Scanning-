Network & Port Scanner (Windows 11)

📌 Project Description

This project is a Python-based Network & Port Scanner designed to run on Windows 11. It scans the local network to detect connected devices and identifies open ports on a target system.

The tool provides a simple and user-friendly GUI interface using Tkinter, making it easy for beginners to understand basic networking and cybersecurity concepts.

---

🎯 Features

- Scan local network (e.g., 192.168.x.x or 10.x.x.x)
- Detect active devices (IP Address, Status)
- Port scanning (1–1024 range)
- Display open/closed ports
- GUI-based interface (Tkinter)
- Save scan results to file
- Beginner-friendly code with comments

---

🛠️ Technologies Used

- Python
- Nmap
- Scapy
- Tkinter (for GUI)

---

⚙️ Installation & Setup

1. Clone the repository

git clone https://github.com/your-username/network-scanner.git
cd network-scanner

2. Install required libraries

pip install python-nmap
pip install scapy


3. Install Npcap

Download from:
https://npcap.com/#download

✔️ Enable "WinPcap compatibility mode" during installation.

---

▶️ How to Run

python network_scanner.py

---

🧪 How It Works

1. User enters a target IP or subnet (e.g., 192.168.1.0/24)
2. The tool scans the network using Scapy/Nmap
3. Active devices are detected
4. If port scanning is enabled, it scans ports (1–1024)
5. Results are displayed in the GUI and saved to a file

---

⚠️ Limitations

- Mobile hotspot networks may restrict device detection
- MAC addresses may not always be visible
- Requires administrator privileges for full functionality

---


📚 Learning Outcome

- Basics of network scanning
- Understanding IP addressing and subnets
- Introduction to cybersecurity tools
- Working with Python libraries like Nmap and Scapy

---

⚖️ Disclaimer

This tool is created for educational purposes only. Do not use it on networks without permission.

---

👨‍💻 Author

Sumit Chauhan
