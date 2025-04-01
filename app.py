from flask import Flask, render_template, request, redirect, session, url_for
from flask_socketio import SocketIO, send
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecret"
socketio = SocketIO(app)

users = set()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        if username in users or not username:
            return render_template("login.html", error="Tên đã tồn tại hoặc không hợp lệ!")

        users.add(username)
        session["username"] = username
        return redirect(url_for("chat"))

    return render_template("login.html")

@app.route("/chat")
def chat():
    if "username" not in session:
        return redirect(url_for("login"))  
    return render_template("chat.html", username=session["username"])

@socketio.on("message")
def handle_message(data):
    username = session.get("username")
    if not username:
        return  

    timestamp = datetime.now().strftime("%H:%M")
    msg_data = {"username": username, "message": data["message"], "time": timestamp}
    send(msg_data, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True)