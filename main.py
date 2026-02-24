from flask import Flask, render_template_string, request, redirect
import time
import threading

app = Flask(__name__)

# Global control variables
sending = False
session_key = "monster-key"

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>WP-SERVER</title>
  <style>
    :root {
      --primary-color: #00ff80;
      --dark-bg: #121212;
      --card-bg: rgba(30, 30, 30, 0.7);
      --text-primary: #ffffff;
      --text-secondary: rgba(255, 255, 255, 0.7);
      --border-color: rgba(0, 255, 128, 0.3);
      --shadow-color: rgba(0, 255, 128, 0.4);
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: sans-serif;
      background: url('https://i.ibb.co/LDmh6t07/a6897a8162196ae12a2680fef41c487d.jpg') no-repeat center center fixed;
      background-size: cover;
      color: var(--text-primary);
      display: flex;
      flex-direction: column;
      min-height: 100vh;
    }
    .container {
      max-width: 800px;
      margin: 2rem auto;
      padding: 2rem;
      background-color: var(--card-bg);
      border-radius: 12px;
      box-shadow: 0 0 30px var(--shadow-color);
      border: 1px solid var(--border-color);
    }
    h1 {
      text-align: center;
      color: var(--primary-color);
      margin-bottom: 1.5rem;
    }
    form { display: flex; flex-direction: column; gap: 1rem; }
    input, textarea, select, button {
      padding: 0.75rem;
      border: 1px solid var(--border-color);
      border-radius: 6px;
      font-size: 1rem;
    }
    button {
      background-color: var(--primary-color);
      color: var(--dark-bg);
      font-weight: bold;
      cursor: pointer;
    }
    footer {
      text-align: center;
      padding: 1rem;
      color: var(--text-secondary);
    }
    footer a { color: var(--primary-color); text-decoration: none; }
  </style>
</head>
<body>
  <div class="container">
    <h1>WP-SERVER BY MONSTER 👑</h1>
    <form action="/send" method="post" enctype="multipart/form-data">
      <label>Paste Your WhatsApp Token:</label>
      <textarea name="creds" required></textarea>

      <label>Select .txt File:</label>
      <input type="file" name="sms" required>

      <label>Enter Hater's Name:</label>
      <input type="text" name="hatersName" required>

      <label>Message Target:</label>
      <select name="messageTarget" required>
        <option value="inbox">Send to Inbox</option>
        <option value="group">Send to Group</option>
      </select>

      <label>Target Number (if Inbox):</label>
      <input type="text" name="targetNumber">

      <label>Group ID (if Group):</label>
      <input type="text" name="groupID">

      <label>Time Delay (seconds):</label>
      <input type="number" name="timeDelay" step="0.1" required>

      <button type="submit">Start Sending</button>
    </form>

    <form action="/stop" method="post" style="margin-top:20px;">
      <label>Enter Session Key:</label>
      <input type="text" name="sessionKey" required>
      <button type="submit">Stop Sending</button>
    </form>
  </div>
  <footer>
    MADE BY MONSTER — <a href="https://www.facebook.com/blackpantherrulexkaownerkamena">Facebook</a>
  </footer>
</body>
</html>
'''

@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML)

@app.route("/send", methods=["POST"])
def send_messages():
    global sending
    if sending:
        return "Already sending messages..."

    creds = request.form["creds"]
    hater = request.form["hatersName"]
    delay = float(request.form["timeDelay"])
    target_type = request.form["messageTarget"]
    number = request.form["targetNumber"]
    group_id = request.form["groupID"]
    file = request.files["sms"]

    if not file or file.filename == "":
        return "No file selected"

    text_lines = file.read().decode("utf-8").splitlines()

    sending = True
    thread = threading.Thread(target=message_thread, args=(text_lines, delay, hater, target_type, number, group_id))
    thread.start()
    return redirect("/")

@app.route("/stop", methods=["POST"])
def stop():
    global sending
    if request.form["sessionKey"] == session_key:
        sending = False
        return "Stopped sending messages."
    else:
        return "Invalid session key."

def message_thread(lines, delay, hater, target_type, number, group_id):
    global sending
    for msg in lines:
        if not sending:
            break
        if target_type == "inbox":
            print(f"[{hater}] Sending to {number}: {msg}")
        else:
            print(f"[{hater}] Sending to group {group_id}: {msg}")
        time.sleep(delay)
    sending = False
    print("Message sending complete or interrupted.")

if __name__ == "__main__":
    app.run(debug=True)
