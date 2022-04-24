from email_validator import validate_email, EmailNotValidError
from flask import (
    Flask,
    request,
    render_template,
    url_for,
    redirect,
    flash,
)
import logging
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "2AZSMss3p5QPbcY2hBsJ"
app.logger.setLevel(logging.DEBUG)
# リダイレクトを中断しない
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
toolbar = DebugToolbarExtension(app)


@app.route("/")
def index():
    return "Hello, FlaskApp"


@app.route("/hello/<name>", endpoint="hellow-endpoint")
def show_name(name):
    return render_template("index.html", name=name)


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    print("contact-complete")
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]

        is_valid = True

        if not username:
            flash("ユーザ名は必須です")
            is_valid = False

        if not email:
            flash("メールは必須です")
            is_valid = False

        try:
            validate_email(email)
        except EmailNotValidError:
            flash("メールアドレスの形式で入力してください")
            is_valid = False

        if not description:
            flash("問い合わせ内容は必須です")
            is_valid = False

        if not is_valid:
            return redirect(url_for("contact"))

        # send mail

        # Post -> Redirect -> Get
        flash("問い合わせあざした")
        return redirect(url_for("contact_complete"))

    return render_template("contact_complete.html")
