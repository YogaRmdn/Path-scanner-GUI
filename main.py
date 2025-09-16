import requests
import threading
import time
import tkinter as tk
from tkinter import scrolledtext, filedialog

# ===== Variabel global =====
stop_flag = False  # Flag untuk menghentikan scan

# ===== Fungsi Path Scanner =====
def path_scan(target, wordlist_file, user_agent, output_widget):
    global stop_flag
    stop_flag = False

    # Clear output saat mulai scan baru
    output_widget.delete(1.0, tk.END)
    output_widget.insert(tk.END, f"[*] Memulai scanning pada {target}...\n", "green")
    output_widget.insert(tk.END, "-"*50 + "\n", "green")
    output_widget.see(tk.END)

    # Baca wordlist dari file
    try:
        with open(wordlist_file, "r") as f:
            wordlist = [line.strip() for line in f if line.strip()]
    except Exception as e:
        output_widget.insert(tk.END, f"[!] Gagal membaca file wordlist: {e}\n", "red")
        return

    headers = {"User-Agent": user_agent}

    for word in wordlist:
        if stop_flag:  # Cek flag berhenti
            output_widget.insert(tk.END, "[!] Scan dihentikan oleh user\n", "red")
            output_widget.see(tk.END)
            break

        try:
            url = f"https://{target}/{word}"
            response = requests.get(url, headers=headers, timeout=5)
            status = response.status_code

            if status < 400:
                output_widget.insert(tk.END, f"[{status}] {url}\n", "green")
            else:
                output_widget.insert(tk.END, f"[{status}] {url}\n", "red")
            
            output_widget.see(tk.END)
            time.sleep(0.3)

        except requests.RequestException:
            output_widget.insert(tk.END, f"[-] {url} Tidak dapat diakses\n", "red")
            output_widget.see(tk.END)
        except KeyboardInterrupt:
            output_widget.insert(tk.END, "[!] Tools dibatalkan\n", "red")
            output_widget.see(tk.END)
            break

    output_widget.insert(tk.END, "[*] Scanning selesai\n", "green")
    output_widget.see(tk.END)

# ===== Fungsi tombol scan =====
def start_scan():
    target = entry_target.get().strip()
    wordlist_file = entry_wordlist.get().strip()
    user_agent = entry_useragent.get().strip()

    if not target or not wordlist_file:
        return

    threading.Thread(
        target=path_scan, 
        args=(target, wordlist_file, user_agent, output_text), 
        daemon=True
    ).start()

# ===== Fungsi tombol stop =====
def stop_scan():
    global stop_flag
    stop_flag = True

# ===== Fungsi pilih file wordlist =====
def browse_file():
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filename:
        entry_wordlist.delete(0, tk.END)
        entry_wordlist.insert(0, filename)

# ===== GUI =====
root = tk.Tk()
root.title("Path Scanner by : Bang yog")
root.geometry("700x500")
root.configure(bg="black")

# Label & Entry Target
tk.Label(
    root, text="Masukkan target:", 
    bg="black", fg="lime", font=("Courier", 12, "bold")
).pack(pady=5)
entry_target = tk.Entry(
    root, width=60, bg="black", fg="lime", 
    insertbackground="lime", font=("Courier", 12, "bold")
)
entry_target.pack(pady=5)

# Label & Entry Wordlist
tk.Label(
    root, text="Pilih file Wordlist (.txt):", 
    bg="black", fg="lime", font=("Courier", 12, "bold")
).pack(pady=5)
frame_wordlist = tk.Frame(root, bg="black")
frame_wordlist.pack(pady=5)
entry_wordlist = tk.Entry(
    frame_wordlist, width=50, bg="black", fg="lime", 
    insertbackground="lime", font=("Courier", 12, "bold")
)
entry_wordlist.pack(side=tk.LEFT, padx=5)
tk.Button(
    frame_wordlist, text="Browse", command=browse_file, 
    bg="black", fg="lime", font=("Courier", 10, "bold")
).pack(side=tk.LEFT)

# Label & Entry User-Agent
tk.Label(
    root, text="Custom User-Agent (optional):", 
    bg="black", fg="lime", font=("Courier", 12, "bold")
).pack(pady=5)
entry_useragent = tk.Entry(
    root, width=60, bg="black", fg="lime", 
    insertbackground="lime", font=("Courier", 12, "bold")
)
entry_useragent.insert(0, "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
entry_useragent.pack(pady=5)

# Tombol Scan & Stop
frame_buttons = tk.Frame(root, bg="black")
frame_buttons.pack(pady=5)
tk.Button(
    frame_buttons, text="Scan", command=start_scan, 
    bg="black", fg="lime", font=("Courier", 12, "bold"), relief="ridge"
).pack(side=tk.LEFT, padx=10)
tk.Button(
    frame_buttons, text="Stop", command=stop_scan, 
    bg="black", fg="red", font=("Courier", 12, "bold"), relief="ridge"
).pack(side=tk.LEFT, padx=10)

# Output scrollable
output_text = scrolledtext.ScrolledText(
    root, width=85, height=20, 
    bg="black", fg="lime", font=("Courier", 12, "bold")
)
output_text.pack(pady=10)
output_text.tag_config("green", foreground="lime")
output_text.tag_config("red", foreground="red")

root.mainloop()
