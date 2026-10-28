from flask import Flask,render_template_string,redirect,url_for

app = Flask(__name__)
main_online = True
backup_online = True
active_server = "Main Server"
message = "All systems operational."

main_records = [
    {"id": "P001", "name": "Patient A",
     "department": "Emergency"},
    {"id": "P002", "name": "Patient B",
     "department": "Cardiology"},
    {"id": "P003", "name": "Patient C",
     "department": "General"}
]

backup_records = [
    {"id": "P001", "name": "Patient A",
     "department": "Emergency"},
    {"id": "P002", "name": "Patient B",
     "department": "Cardiology"},
    {"id": "P003", "name": "Patient C",
     "department": "General"}
]

@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>Hospital Continuity System</title>
    </head>
    <body style="font-family: Arial; text-align: center;
                 background-color: #eaf7ff; padding: 50px;">

        <h1>Hospital Continuity System</h1>
        <form action="/simulate-failure" method="post">
    <button type="submit"
        style="background-color: red; color: white; padding: 12px;">
        Simulate Main Server Failure
    </button>
</form>
        <h2>Keeping Hospital Services Running</h2>

        <p id="centre">Main Data Centre: Online</p>
<p id="records">Patient Records: Available</p>
<p id="mode">Emergency Mode: Inactive</p>

<button onclick="activateEmergency()">
    Activate Emergency Mode
</button>
<a href="/patients">View Dummy Patient Records</a>

<script>
function activateEmergency() {
    document.getElementById("centre").innerText =
        "Main Data Centre: Offline (Simulated)";

    document.getElementById("records").innerText =
        "Patient Records: Available via Recovery Demo";

    document.getElementById("mode").innerText =
        "Emergency Mode: Active (Simulated)";

    alert("Simulated failure detected. Recovery demo activated!");
}
</script>
"""
PATIENTS_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Dummy Patient Records</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f1f5f9;
            padding: 30px;
            color: #1e293b;
        }
        .container {
            max-width: 900px;
            margin: auto;
        }
        h1 { color: #0f766e; }
        .card {
            background: white;
            padding: 20px;
            border-radius: 12px;
            margin-top: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            text-align: left;
            padding: 12px;
            border-bottom: 1px solid #ddd;
        }
        th { background: #ccfbf1; }
        a {
            display: inline-block;
            background: #0f766e;
            color: white;
            padding: 10px 15px;
            border-radius: 6px;
            text-decoration: none;
        }
        .note {
            color: #b45309;
            margin-top: 15px;
        }
    </style>
</head>
<body>
<div class="container">
    <h1>Dummy Patient Records</h1>
    <p>Hospital Continuity Management System</p>

    <div class="card">
        <h3>Active Data Source: {{ active_server }}</h3>

        {% if records %}
        <table>
            <tr>
                <th>Patient ID</th>
                <th>Dummy Name</th>
                <th>Department</th>
            </tr>
            {% for patient in records %}
            <tr>
                <td>{{ patient.id }}</td>
                <td>{{ patient.name }}</td>
                <td>{{ patient.department }}</td>
            </tr>
            {% endfor %}
        </table>
        {% else %}
        <p>No records available from the active data source.</p>
        {% endif %}

        <p class="note">
            Educational demo only. All patient records are fictional.
        </p>
        <a href="/">Back to Dashboard</a>
    </div>
</div>
</body>
</html>
"""


@app.route("/patients")
def patients_page():
    if active_server == "Main Server" and main_online:
        records = main_records
    elif active_server == "Backup Server" and backup_online:
        records = backup_records
    else:
        records = []

    return render_template_string("""
        <h1>Dummy Patient Records</h1>
    <h3>Active Server: {{ active_server }}</h3>

    <table border="1" cellpadding="10">
        <tr>
            <th>Patient ID</th>
            <th>Name</th>
            <th>Department</th>
        </tr>
        {% for patient in records %}
        <tr>
            <td>{{ patient.id }}</td>
            <td>{{ patient.name }}</td>
            <td>{{ patient.department }}</td>
        </tr>
        {% endfor %}
    </table>

    <p><a href="/">Back to Dashboard</a></p>
    <p>Educational demo using fictional data only.</p>
    """,records=records,active_server=active_server)

@app.route("/simulate-failure", methods=["POST"])
def simulate_failure():
    global main_online, active_server, message

    main_online = False

    if backup_online:
        active_server = "Backup Server"
        message = "Main server failed. Backup server activated!"
    else:
        active_server = "No Server Available"
        message = "Both servers are unavailable!"

    return redirect(url_for("home"))

if __name__=="__main__":
    app.run(debug=True)