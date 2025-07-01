from flask import Flask, render_template, request, redirect, url_for, flash
from telegram_channel_viewer.channel import Channel
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "change-me")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        channel = request.form.get("channel", "").strip()
        if not channel:
            flash("Please enter a channel username or link.")
            return redirect(url_for("index"))
        return redirect(url_for("view_channel", name=channel.lstrip("@")))
    return render_template("index.html")

@app.route("/channel/<name>")
def view_channel(name):
    try:
        ch = Channel(name)
        info = {
            "name": ch.channel_name,
            "desc": ch.channel_description,
            "subs": ch.channel_subs,
            "photo": ch.channel_profile
        }
        messages = ch.messages
        return render_template("channel.html", info=info, messages=messages)
    except Exception as e:
        flash(f"Error fetching channel: {e}")
        return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
