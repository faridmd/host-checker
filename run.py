import socket
import ssl
import concurrent.futures

# ================= KONFIGURASI =================
SNI = "ray.faridanwar.my.id" 
HOST_HEADER = "ray.faridanwar.my.id"
PATH = "/xray-tunnel"
PORT = 443
TIMEOUT = 5
MAX_THREADS = 15
# ===============================================

# Kode Warna ANSI untuk Terminal
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

def check_host(host):
    host = host.strip()
    if not host:
        return None
        
    try:
        # 1. Buka Koneksi TCP
        sock = socket.create_connection((host, PORT), timeout=TIMEOUT)
        
        # 2. Bungkus dengan TLS & SNI
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        secure_sock = context.wrap_socket(sock, server_hostname=SNI)
        
        # 3. Kirim Request
        request = (
            f"GET {PATH} HTTP/1.1\r\n"
            f"Host: {HOST_HEADER}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n"
        )
        secure_sock.sendall(request.encode())
        
        # 4. Terima Balasan
        response = secure_sock.recv(1024).decode('utf-8', errors='ignore')
        secure_sock.close()
        
        # Mengambil hanya baris pertama dari balasan HTTP (contoh: "HTTP/1.1 101 Switching Protocols")
        if response:
            status_line = response.split('\r\n')[0]
        else:
            status_line = "Empty Response (Tidak ada balasan)"
        
        # 5. Cek Hasil
        if "HTTP/1.1 101" in response:
            return True, host, status_line
        else:
            return False, host, status_line
            
    # Menangkap pesan error spesifik jika gagal sebelum menerima balasan HTTP
    except socket.timeout:
        return False, host, "Timeout / RTO"
    except ssl.SSLError:
        return False, host, "SSL/SNI Ditolak Cloudflare"
    except ConnectionRefusedError:
        return False, host, "Koneksi Ditolak (Port Tertutup)"
    except Exception as e:
        # Membersihkan teks error panjang agar lebih rapi
        error_msg = str(e).split(']')[-1].strip() if ']' in str(e) else str(e)
        return False, host, f"Error: {error_msg}"

def main():
    try:
        with open("list.txt", "r") as f:
            # Membaca file dan menghapus duplikat
            hosts = list(dict.fromkeys([line.strip() for line in f if line.strip()]))
            
        # Menyimpan kembali list yang sudah difilter ke list.txt agar duplikat terhapus secara permanen
        with open("list.txt", "w") as f:
            for host in hosts:
                f.write(f"{host}\n")
                
    except FileNotFoundError:
        print("File list.txt tidak ditemukan! Buat dulu filenya.")
        return

    print(f"Memulai pengecekan {len(hosts)} host unik...")
    print("-" * 50)
    
    live_hosts = []
    dead_hosts = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = {executor.submit(check_host, h): h for h in hosts}
        
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result is None:
                continue
                
            is_live, host, status = result
            
            # Print hasil dengan menyertakan pesan status di sebelahnya
            if is_live:
                print(f"{GREEN}[LIVE] {host.ljust(20)} 👉 {status}{RESET}")
                live_hosts.append(host)
            else:
                print(f"{RED}[DEAD] {host.ljust(20)} 👉 {status}{RESET}")
                dead_hosts.append(host)
                
    # Tulis HANYA host yang LIVE ke result.txt
    with open("result.txt", "w") as f:
        for h in live_hosts:
            f.write(f"{h}\n")
            
    print("-" * 50)
    print(f"Pengecekan selesai! {GREEN}{len(live_hosts)} LIVE{RESET}, {RED}{len(dead_hosts)} DEAD{RESET}.")
    print("Host yang LIVE telah disimpan ke dalam file result.txt")

if __name__ == "__main__":
    main()
