import sqlite3
import os
from flask import Flask, render_template, request, g, redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)

# CS50 db.execute. But remember to add .fetchone or .fetchall!
def get_db():
    db = getattr(g, "_database", None)
    if db == None:
        db = g._database = sqlite3.connect("animals.db")
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db != None:
        db.close()


# ==========================================
#  CHECKLIST DỰ ÁN FLASK - QUẢN LÝ SINH VẬT
# ==========================================

# [x] Làm index
# [ ] Làm thanh tìm kiếm
# [ ] Gợi ý các con vật khi mới vào trang

# [x] Làm Giới thiệu
# [x] Làm liên hệ
# [ ] Làm chuyển đổi ngôn ngữ
# [ ] Làm đầu mục sinh vật
# [x] Làm thêm sinh vật
# [ ] Làm sửa đổi sinh vật
# [ ] Làm sửa đổi thông tin sinh vật
# [ ] Làm xóa thông tin sinh vật

# apology if user is too dumb to type the word in correctly
def xin_loi(message):
    return render_template("vi/xin-loi.html", message=message)
def apology(message):
    return render_template("en/apology.html", message=message)

# Home
@app.route("/")
def index():
    return render_template("vi/index.html", language="vi")

# About me (or yeah, the website)!
@app.route("/gioi-thieu")
def gioi_thieu():
    return render_template("vi/gioi-thieu.html")

# contact me
@app.route("/lien-he")
def lien_he():
    return render_template("vi/lien-he.html")

# Wanna search? I need to build more on this one
@app.route("/search", methods=["GET"]) # Search tiếng việt nhé
def search():
    query = request.args.get("search", "").strip()
    if not query:
        return render_template("vi/tra-cuu.html", results=[])

    db = get_db()
    rows = db.execute("""
        SELECT creatures.id, translations.species, creatures.scientific_name
        FROM creatures
        JOIN translations ON translations.creature_id = creatures.id
        WHERE translations.language = 'vi' 
        AND translations.species LIKE ?
    """, (f"%{query}%",)).fetchall()

    return render_template("vi/tra-cuu.html", results=rows, query=query)


@app.route("/en/search", methods=["GET"]) # ENGLISH SEARCH
def search_en():
    query = request.args.get("search", "").strip()
    if not query:
        return render_template("en/search.html", results=[])

    db = get_db()
    rows = db.execute("""
        SELECT creatures.id, translations.species, creatures.scientific_name
        FROM creatures
        JOIN translations ON translations.creature_id = creatures.id
        WHERE translations.language = 'en' 
        AND translations.species LIKE ?
    """, (f"%{query}%",)).fetchall()

    return render_template("en/search.html", results=rows, query=query)

@app.route("/sinh-vat/<int:creature_id>") # VIETNAMESE RESULT
def creature_info(creature_id):
    db = get_db()

    creature = db.execute(""" SELECT creatures.*, translations.*, images.*
                                FROM creatures
                                JOIN translations ON translations.creature_id = creatures.id
                                JOIN images ON images.creature_id = creatures.id
                                WHERE creatures.id = ?
                                AND translations.language = 'vi'
                                """, (creature_id,)).fetchone()

    if not creature:
        return xin_loi("Không tìm thấy sinh vật")

    return render_template("vi/ket-qua.html", creature=creature)

@app.route("/en/sinh-vat/<int:creature_id>") # VIETNAMESE RESULT
def creature_info_en(creature_id):
    db = get_db()

    creature = db.execute(""" SELECT creatures.*, translations.*, images.*
                                FROM creatures
                                JOIN translations ON translations.creature_id = creatures.id
                                JOIN images ON images.creature_id = creatures.id
                                WHERE creatures.id = ?
                                AND translations.language = 'en'
                                """, (creature_id,)).fetchone()

    if not creature:
        return apology("Creature not found.")

    return render_template("en/result.html", creature=creature)

# Build this one as well
# Change the database !!!!!!!!
@app.route("/sua-doi")
def sua_doi():
    return render_template("vi/change-database/sua-doi.html") #done

@app.route("/sua-doi/them-sinh-vat", methods=["GET", "POST"])
def them_sinh_vat():
    if request.method == "POST":
        species_vi = request.form.get("species_vi")
        quick_summary_vi = request.form.get("quick_summary_vi")
        if not species_vi or not quick_summary_vi:
            return xin_loi("Tên loài và tóm tắt nhanh bằng tiếng Việt là bắt buộc")

        species_en = request.form.get("species_en")
        quick_summary_en = request.form.get("quick_summary_en")

        if not species_en or not quick_summary_en:
            return xin_loi("Tên loài và tóm tắt nhanh bằng tiếng Anh là bắt buộc")

        allowed_categories = {"animal", "plant", "fungus"}
        allowed_era = {"modern", "ancient"}
        category = request.form.get("category")
        if category not in allowed_categories:
            return xin_loi("Loài sinh vật không hợp lệ")
        era = request.form.get("era")
        if era not in allowed_era:
            return xin_loi("Thời đại không hợp lệ")

        scientific_name = request.form.get("scientific_name")
        taxonomic_domain = request.form.get("taxonomic_domain")
        taxonomic_kingdom = request.form.get("taxonomic_kingdom")
        taxonomic_phylum = request.form.get("taxonomic_phylum")
        taxonomic_class = request.form.get("taxonomic_class")
        taxonomic_order = request.form.get("taxonomic_order")
        taxonomic_family = request.form.get("taxonomic_family")
        taxonomic_genus = request.form.get("taxonomic_genus")

        db = get_db()
        cursor = db.execute("INSERT INTO creatures (category, era, scientific_name, taxonomic_domain, taxonomic_kingdom, taxonomic_phylum, taxonomic_class, taxonomic_order, taxonomic_family, taxonomic_genus) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                   (category, era, scientific_name, taxonomic_domain, taxonomic_kingdom, taxonomic_phylum, taxonomic_class, taxonomic_order, taxonomic_family, taxonomic_genus))
        creature_id = cursor.lastrowid

        #Tiếng việt
        db.execute("INSERT INTO translations (creature_id, language, species, quick_summary) VALUES (?, ?, ? ,?)",
                       (creature_id, "vi", species_vi, quick_summary_vi))

        #Tiếng anh
        db.execute("INSERT INTO translations (creature_id, language, species, quick_summary) VALUES (?, ?, ? ,?)",
                       (creature_id, "en", species_en, quick_summary_en))

        author = request.form.get("author")
        license = request.form.get("license")
        source = request.form.get("source")
        alt_text = request.form.get("alt_text")
        alt_text_en = request.form.get("alt_text_en")

        image = request.files.get("upload-img")
        filename = secure_filename(image.filename)
        image_path = os.path.join("images", "creatures", filename)
        image.save(image_path)

        db.execute("INSERT INTO images (creature_id, photo, author, license, source, alt_text, alt_text_en) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (creature_id, image_path, author, license, source, alt_text, alt_text_en))

        db.commit()

        return redirect("/")
    
    return render_template("vi/change-database/them-sinh-vat.html")

@app.route("/sua-doi/cap-nhat", methods=["GET", "POST"])
def cap_nhat_du_lieu():
    return xin_loi("Chưa xong đâu má")

@app.route("/sua-doi/xoa", methods=["GET", "POST"])
def xoa_du_lieu():
    return xin_loi("Chưa xong đâu má")
    
###############################################
#                                             #
#                English version              #
#                                             #
###############################################
@app.route("/en")
def index_en():
    return render_template("en/index-en.html", language="en")

@app.route("/en/about")
def about():
    return render_template("en/about.html")

@app.route("/en/contact")
def contact():
    return render_template("en/contact.html")


# Something else, just for fun.
@app.route("/troll")
def troll():
    return render_template("vi/troll.html")



if __name__ == '__main__':
    app.run(debug=True)