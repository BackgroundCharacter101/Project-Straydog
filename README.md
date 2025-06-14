# Project-Straydog
Project Name: Straydog: Remote Access Framework for Personal Use
Description:

Straydog is a Python-based remote access tool (RAT) designed for ethical and educational use, enabling users to control and monitor their own machines over LAN or the internet. The system consists of a lightweight agent (client.py) installed on the target PC and a Flask-powered web server (server.py) that acts as the command-and-control (C2) interface.

Straydog allows remote command execution, real-time feedback, screenshot capture, webcam snapshots, keylogging, and log retrieval—all from a secure, password-protected web interface. The system uses a secret API key for agent authentication and supports background execution with minimal system visibility.

Key Features:

🔐 Secure login interface with session timeout and API key-based agent validation

💻 Remote shell command execution with live output updates

🖼️ Screenshot and webcam image capture

⌨️ Background keylogger and log delivery system

📁 File system exploration capabilities (optional future phase)

🌐 Works over LAN or internet via cloud hosting or secure tunnels (e.g., Tailscale, Ngrok, Cloudflare Tunnel)

⚙️ Built-in persistence and stealth options (agent auto-start, silent execution, etc.)

Use Case:
Designed for developers, cybersecurity students, and researchers to learn about remote administration, client-server communication, and post-exploitation simulation in a controlled, private environment.

Disclaimer:
This tool is intended strictly for educational and ethical use on systems you own or have explicit permission to manage.

________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

## 📂 Project Structure
Straydog/
├── client.py           # Agent script that runs on target device
├── server.py           # Flask-based control panel
├── run_straydog.bat    # makes client run on the pc every time you reboot

⚙️ How It Works
client.py runs silently in the background and polls the server for commands

server.py hosts a Flask-based web interface for sending commands and receiving output

Communication secured using a custom API key

Optional webcam/screenshot, keylogger, and file explorer capabilities

🔧 Setup Instructions
1. Install Dependencies
flask
requests
opencv-python
pynput
pyautogui

3. Start the Server (Control Panel)
python server.py

Access the panel at:
http://<your-ip>:5000

4. Deploy the Agent
Edit client.py:

SERVER_URL = "http://<server-ip>:5000"
API_KEY = "YourCustomAPIKey"

Then run:
python client.py


☁️ Deploy to the Internet
You can make the control panel accessible globally by:

Using Ngrok (ngrok http 5000)

Hosting on a VPS like Azure, Oracle, or EC2

Using Tailscale or Cloudflare Tunnel for secure private access

🔐 Security Tips
Change the API_KEY, USERNAME, and PASSWORD in server.py

Use a firewall to restrict unwanted access

Avoid deploying on public IP without extra authentication layers

🛡️ Legal Notice
This tool is provided for educational and personal use only. Any misuse or unauthorized deployment is strictly prohibited.

