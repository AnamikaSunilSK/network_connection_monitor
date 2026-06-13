import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import platform
import re
import socket

class NetworkToolkit:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Toolkit")
        self.root.geometry("800x600")
        self.root.configure(bg='#1e1e1e')
        
        self.colors = {
            'bg': '#1e1e1e',
            'fg': '#d4d4d4',
            'accent': '#007acc',
            'success': '#4ec9b0',
            'error': '#f48771'
        }
        
        self.setup_ui()
        
    def setup_ui(self):
      
        title = tk.Label(self.root, text="🌐 Network Toolkit", 
                        font=("Arial", 16, "bold"),
                        bg=self.colors['bg'], fg=self.colors['accent'])
        title.pack(pady=10)

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: DNS Lookup
        self.dns_frame = tk.Frame(notebook, bg=self.colors['bg'])
        notebook.add(self.dns_frame, text="DNS Lookup")
        self.setup_dns_tab()
        
        # Tab 2: Ping Tool
        self.ping_frame = tk.Frame(notebook, bg=self.colors['bg'])
        notebook.add(self.ping_frame, text="Ping Tool")
        self.setup_ping_tab()
        
        # Tab 3: IP Info
        self.ip_frame = tk.Frame(notebook, bg=self.colors['bg'])
        notebook.add(self.ip_frame, text="Local Info")
        self.setup_ip_tab()
        
        # Tab 4: Port Checker (simple)
        self.port_frame = tk.Frame(notebook, bg=self.colors['bg'])
        notebook.add(self.port_frame, text="Quick Port Check")
        self.setup_port_tab()
        
    def setup_dns_tab(self):
        # Domain input
        tk.Label(self.dns_frame, text="Domain Name:", 
                bg=self.colors['bg'], fg=self.colors['fg']).pack(pady=5)
        self.domain_entry = tk.Entry(self.dns_frame, width=40,
                                     bg='#2d2d2d', fg=self.colors['fg'])
        self.domain_entry.pack(pady=5)
        self.domain_entry.insert(0, "google.com")
        
        tk.Button(self.dns_frame, text="Lookup IP", command=self.dns_lookup,
                 bg=self.colors['accent'], fg='white').pack(pady=5)
        
        self.dns_result = scrolledtext.ScrolledText(self.dns_frame, height=15,
                                                     bg='#2d2d2d', fg=self.colors['success'])
        self.dns_result.pack(fill=tk.BOTH, expand=True, pady=10)
        
    def setup_ping_tab(self):
        tk.Label(self.ping_frame, text="Host to Ping:", 
                bg=self.colors['bg'], fg=self.colors['fg']).pack(pady=5)
        self.ping_entry = tk.Entry(self.ping_frame, width=40,
                                   bg='#2d2d2d', fg=self.colors['fg'])
        self.ping_entry.pack(pady=5)
        self.ping_entry.insert(0, "google.com")
        
        tk.Button(self.ping_frame, text="Ping", command=self.ping_host,
                 bg=self.colors['accent'], fg='white').pack(pady=5)
        
        self.ping_result = scrolledtext.ScrolledText(self.ping_frame, height=15,
                                                      bg='#2d2d2d', fg=self.colors['success'])
        self.ping_result.pack(fill=tk.BOTH, expand=True, pady=10)
        
    def setup_ip_tab(self):
        info_text = tk.Text(self.ip_frame, height=10, bg='#2d2d2d', 
                           fg=self.colors['success'], font=("Consolas", 10))
        info_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Get local IP
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        
        info_text.insert(tk.END, f"Hostname: {hostname}\n")
        info_text.insert(tk.END, f"Local IP: {local_ip}\n")
        
        # Try to get public IP 
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            public_ip = s.getsockname()[0]
            s.close()
            info_text.insert(tk.END, f"Public IP: {public_ip}\n")
        except:
            info_text.insert(tk.END, "Public IP: Could not determine\n")
        
        info_text.insert(tk.END, f"\nSystem: {platform.system()} {platform.release()}\n")
        info_text.config(state=tk.DISABLED)
        
    def setup_port_tab(self):
        tk.Label(self.port_frame, text="Target IP:", 
                bg=self.colors['bg'], fg=self.colors['fg']).pack(pady=5)
        self.port_target = tk.Entry(self.port_frame, width=30,
                                    bg='#2d2d2d', fg=self.colors['fg'])
        self.port_target.pack(pady=5)
        self.port_target.insert(0, "127.0.0.1")
        
        tk.Label(self.port_frame, text="Port:", 
                bg=self.colors['bg'], fg=self.colors['fg']).pack(pady=5)
        self.port_number = tk.Entry(self.port_frame, width=10,
                                    bg='#2d2d2d', fg=self.colors['fg'])
        self.port_number.pack(pady=5)
        self.port_number.insert(0, "80")
        
        tk.Button(self.port_frame, text="Check Port", command=self.check_port,
                 bg=self.colors['accent'], fg='white').pack(pady=5)
        
        self.port_result = tk.Label(self.port_frame, text="", 
                                    bg=self.colors['bg'], font=("Arial", 10))
        self.port_result.pack(pady=10)
        
    def dns_lookup(self):
        domain = self.domain_entry.get().strip()
        if not domain:
            return
        
        self.dns_result.delete(1.0, tk.END)
        self.dns_result.insert(tk.END, f"Resolving {domain}...\n\n")
        
        try:
            ip = socket.gethostbyname(domain)
            self.dns_result.insert(tk.END, f"✅ IP Address: {ip}\n", "success")
            
            # Try to get all IPs
            try:
                addrinfo = socket.getaddrinfo(domain, None)
                ips = set()
                for addr in addrinfo:
                    ips.add(addr[4][0])
                
                if len(ips) > 1:
                    self.dns_result.insert(tk.END, f"\nAll IP addresses:\n", "info")
                    for ip_addr in ips:
                        self.dns_result.insert(tk.END, f"  • {ip_addr}\n")
            except:
                pass
                
        except socket.gaierror:
            self.dns_result.insert(tk.END, f"❌ Could not resolve {domain}\n", "error")
        
        # Configure tags
        self.dns_result.tag_config("success", foreground=self.colors['success'])
        self.dns_result.tag_config("error", foreground=self.colors['error'])
        self.dns_result.tag_config("info", foreground=self.colors['accent'])
        
    def ping_host(self):
        host = self.ping_entry.get().strip()
        if not host:
            return
        
        self.ping_result.delete(1.0, tk.END)
        self.ping_result.insert(tk.END, f"Pinging {host}...\n\n")
        
        # Use system ping command 
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '4', host]
        
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=10)
            self.ping_result.insert(tk.END, result.stdout)
            
            if result.returncode == 0:
                self.ping_result.insert(tk.END, "\n✅ Host is reachable", "success")
            else:
                self.ping_result.insert(tk.END, "\n❌ Host is not responding", "error")
        except subprocess.TimeoutExpired:
            self.ping_result.insert(tk.END, "❌ Ping timeout", "error")
        except Exception as e:
            self.ping_result.insert(tk.END, f"❌ Error: {str(e)}", "error")
        
        self.ping_result.tag_config("success", foreground=self.colors['success'])
        self.ping_result.tag_config("error", foreground=self.colors['error'])
        
    def check_port(self):
        target = self.port_target.get().strip()
        try:
            port = int(self.port_number.get())
        except:
            self.port_result.config(text="❌ Invalid port number", fg=self.colors['error'])
            return
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((target, port))
            sock.close()
            
            if result == 0:
                self.port_result.config(text=f"✅ Port {port} is OPEN", 
                                       fg=self.colors['success'])
            else:
                self.port_result.config(text=f"❌ Port {port} is CLOSED", 
                                       fg=self.colors['error'])
        except:
            self.port_result.config(text=f"❌ Could not connect to {target}", 
                                   fg=self.colors['error'])

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkToolkit(root)
    root.mainloop()
