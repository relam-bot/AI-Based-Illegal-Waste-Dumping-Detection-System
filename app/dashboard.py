from flask import Flask, render_template_string, send_from_directory, redirect, url_for
import os
from datetime import datetime
import shutil

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EVIDENCE_DIR = os.path.join(BASE_DIR, "..", "evidence")

# ---------------- HOME PAGE ----------------
HOME_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Illegal Dump Dashboard</title>
    <style>
        body { font-family: Arial; margin:0; background:#f3f4f6; }
        header { background:#111827; color:white; padding:20px; text-align:center; }
        .container {
            display:grid;
            grid-template-columns:repeat(auto-fill,minmax(300px,1fr));
            gap:20px;
            padding:20px;
        }
        .card {
            background:white;
            border-radius:12px;
            box-shadow:0 4px 12px rgba(0,0,0,0.1);
            padding:20px;
            text-align:center;
            cursor:pointer;
            transition:0.2s;
        }
        .card:hover { transform:scale(1.03); }
        a { text-decoration:none; color:black; }
    </style>
</head>
<body>

<header>
    <h1>🚨 Illegal Dump Detection Dashboard</h1>
    <p>Total Cases: {{ total_cases }}</p>
</header>

<div class="container">
{% for case in cases %}
    <a href="/case/{{case.folder}}">
        <div class="card">
            <h3>{{case.folder}}</h3>
            <p>{{case.time}}</p>
        </div>
    </a>
{% endfor %}
</div>

</body>
</html>
"""

# ---------------- CASE PAGE ----------------
CASE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Case Report</title>
    <style>
        body { font-family: Arial; margin:0; background:#f3f4f6; }
        header { background:#111827; color:white; padding:20px; text-align:center; }
        .container { padding:20px; max-width:1100px; margin:auto; }

        .images {
            display:flex;
            gap:20px;
            justify-content:center;
            margin-bottom:20px;
        }

        .images img {
            width:48%;
            border-radius:10px;
            box-shadow:0 4px 12px rgba(0,0,0,0.1);
        }

        .info {
            background:white;
            padding:15px;
            border-radius:10px;
            box-shadow:0 4px 12px rgba(0,0,0,0.1);
            margin-bottom:20px;
            text-align:center;
        }

        .btn {
            padding:10px 15px;
            border:none;
            border-radius:6px;
            cursor:pointer;
            font-weight:bold;
            margin-right:10px;
        }

        .delete { background:#ef4444; color:white; }
        .back { background:#2563eb; color:white; }
    </style>
</head>
<body>

<header>
    <h1>Case {{folder}}</h1>
</header>

<div class="container">

    <div class="info">
        <p><strong>Time:</strong> {{time}}</p>
    </div>

    <div class="images">
        <img src="/evidence/{{folder}}/person.jpg">
        <img src="/evidence/{{folder}}/waste.jpg">
    </div>

    <div style="text-align:center;">
        <a href="/"><button class="btn back">Back</button></a>
        <a href="/delete/{{folder}}">
            <button class="btn delete">Delete Case</button>
        </a>
    </div>

</div>

</body>
</html>
"""

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    if not os.path.exists(EVIDENCE_DIR):
        return "No evidence folder found."

    folders = sorted(os.listdir(EVIDENCE_DIR), reverse=True)
    cases = []

    for folder in folders:
        folder_path = os.path.join(EVIDENCE_DIR, folder)
        if not os.path.isdir(folder_path):
            continue

        try:
            ts = folder.split("_")[1]
            time_str = datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d %H:%M:%S")
        except:
            time_str = "Unknown time"

        cases.append({
            "folder": folder,
            "time": time_str
        })

    return render_template_string(
        HOME_HTML,
        cases=cases,
        total_cases=len(cases)
    )

@app.route("/case/<folder>")
def case_detail(folder):
    folder_path = os.path.join(EVIDENCE_DIR, folder)
    if not os.path.exists(folder_path):
        return "Case not found."

    try:
        ts = folder.split("_")[1]
        time_str = datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d %H:%M:%S")
    except:
        time_str = "Unknown time"

    return render_template_string(
        CASE_HTML,
        folder=folder,
        time=time_str
    )

@app.route("/delete/<folder>")
def delete_case(folder):
    folder_path = os.path.join(EVIDENCE_DIR, folder)
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    return redirect(url_for("home"))

@app.route("/evidence/<path:folder>/<path:filename>")
def evidence(folder, filename):
    return send_from_directory(
        os.path.join(EVIDENCE_DIR, folder),
        filename
    )

if __name__ == "__main__":
    app.run(debug=True)