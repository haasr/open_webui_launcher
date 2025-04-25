import tkinter as tk
import subprocess
import time
import requests
import threading
import webbrowser


class WebUIServer:
    def __init__(self, master):
        self.master = master
        master.title("Open WebUI Server Control")
        master.config(background='#f5f4ed')

        self.server_process = None
        self.server_running = False
        self.toggle_button = None
        self.status_label = None

        # Get screen width and height
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        # Calculate the x and y coordinates for the top-right corner
        x = screen_width - 250
        y = 0

        # Set the geometry to position and size the window
        master.geometry(f"{250}x{116}+{x}+{y}") # Adjust width and height as needed

        self.create_widgets()
        self.update_status()

    def create_widgets(self):
        self.toggle_button = tk.Button(self.master,
                                       text="⏻ Start Server",
                                       background='#2d5bec',
                                       foreground='white',
                                       highlightbackground='#2d5bec',
                                       command=self.toggle_server)
        self.toggle_button.config(font=('Arial', 16))
        self.toggle_button.pack(pady=20)

        self.status_label = tk.Label(self.master, text="Server Status: Offline")
        self.status_label.config(font=('Arial', 16))
        self.status_label.config(foreground='black')
        self.status_label.pack()

    def toggle_server(self):
        if not self.server_running:
            self.start_server()
        else:
            self.stop_server()

    def start_server(self):
        def run_server():
            try:
                self.server_process = subprocess.Popen(["open-webui", "serve"])
                self.server_running = True
                self.update_status()

                # Wait for the server to be available
                time.sleep(5)  # Initial wait
                max_attempts = 20
                attempt = 0
                while attempt < max_attempts:
                    try:
                        response = requests.get("http://127.0.0.1:8080/")
                        if response.status_code == 200:
                            break  # Server is up
                    except requests.ConnectionError:
                        pass  # Server not yet available
                    time.sleep(2)
                    attempt += 1

                if attempt == max_attempts:
                    print("Server did not become available after multiple attempts.")
                else:
                    # Open browser only if server is up
                    webbrowser.open_new_tab("http://127.0.0.1:8080/")

            except FileNotFoundError:
                print("Error: 'open-webui' command not found.  Make sure it's installed and in your PATH.")
                self.server_running = False
                self.update_status()
            except Exception as e:
                print(f"Error starting server: {e}")
                self.server_running = False
                self.update_status()

        threading.Thread(target=run_server).start()  # Start server in a separate thread

    def stop_server(self):
        if self.server_process:
            try:
                self.server_process.terminate()
                self.server_process.wait()
            except:
                pass # handle errors if process doesn't terminate cleanly
            self.server_running = False
            self.update_status()

    def update_status(self):
        if self.server_running:
            self.status_label.config(text="Server Status: Online")
            self.toggle_button.config(text="⏻ Stop Server")
            self.toggle_button.config(background='#f46f58')
            self.toggle_button.config(highlightbackground='#f46f58')
        else:
            self.status_label.config(text="Server Status: Offline")
            self.toggle_button.config(text="⏻ Start Server")
            self.toggle_button.config(background='#2d5bec')
            self.toggle_button.config(highlightbackground='#2d5bec')


root = tk.Tk()
server_ui = WebUIServer(root)
root.mainloop()
