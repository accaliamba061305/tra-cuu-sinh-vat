import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

def get_db():
    connection = sqlite3.connect("animals.db")
    connection.row_factory = sqlite3.Row
    return connection

def xin_loi(message):
    return render_template("vi/xin-loi.html", message=message)
def apology(message):
    return render_template("en/apology.html", message=message)

@app.route("/")
def index():
    return render_template("vi/index.html")

@app.route("/gioi-thieu")
def gioi_thieu():
    return render_template("vi/gioi-thieu.html")

@app.route("/lien-he")
def lien_he():
    return render_template("vi/lien-he.html")

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("search")
    if not query:
        return xin_loi("Không tìm thấy kết quả")
    elif query:
        return render_template("vi/tra-cuu.html")




@app.route("/them-sinh-vat", methods=["GET", "POST"])
def them_sinh_vat():
    if request.method == "POST":
        return 'Form đã được gửi!'
    return render_template("vi/them-sinh-vat.html")
    
@app.route("/en")
def index_en():
    return render_template("en/index-en.html")

@app.route("/en/about")
def about():
    return render_template("en/about.html")

@app.route("/en/contact")
def contact():
    return render_template("en/contact.html")



@app.route("/troll")
def troll():
    return render_template("vi/troll.html")



if __name__ == '__main__':
    app.run(debug=True)