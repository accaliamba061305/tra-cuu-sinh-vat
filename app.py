import sqlite3
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, g, redirect, url_for, session
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
load_dotenv()

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
# [x] Làm thanh tìm kiếm
# [x] Gợi ý các con vật khi mới vào trang

# [x] Làm Giới thiệu
# [x] Làm liên hệ
# [x] Làm chuyển đổi ngôn ngữ
# [x] Làm đầu mục sinh vật
# [x] Làm thêm sinh vật
# [x] Làm sửa đổi sinh vật
# [x] Làm sửa đổi thông tin sinh vật
# [x] Làm xóa thông tin sinh vật

#BONUS: SECURITY.

# apology if user is too dumb to type the word in correctly
def xin_loi(message):
    return render_template("vi/xin-loi.html", message=message)
def apology(message):
    return render_template("en/apology.html", message=message)

# Home
@app.route("/")
def index():
    db = get_db()

    creatures = db.execute("""SELECT creatures.id, translations.species, creatures.scientific_name, images.photo, images.alt_text
                                FROM creatures
                                JOIN translations ON translations.creature_id = creatures.id
                                JOIN images ON images.creature_id = creatures.id
                                WHERE translations.language = 'vi'
                                ORDER BY RANDOM() LIMIT 10""").fetchall()

    return render_template("vi/index.html", creatures=creatures)

# Đầu mục sinh vật
@app.route("/sinh-vat/<category>")
def creature_category(category):
    allowed_categories = {
        "animal",
        "plant",
        "fungus",
        "insects"
    }

    if category not in allowed_categories:
        return xin_loi("Không có đầu mục sinh vật đó")

    db = get_db()
    creatures = db.execute("""SELECT creatures.id, translations.species, creatures.scientific_name, images.photo, images.alt_text
                                FROM creatures
                                JOIN translations ON translations.creature_id = creatures.id
                                JOIN images ON images.creature_id = creatures.id
                                WHERE creatures.category = ? AND translations.language = 'vi'
                                ORDER BY translations.species""", (category,)).fetchall()

    return render_template("vi/sinh-vat.html", creatures=creatures, category=category)

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
        SELECT creatures.id, translations.species, creatures.scientific_name, images.photo, images.alt_text
        FROM creatures
        JOIN translations ON translations.creature_id = creatures.id
        JOIN images ON images.creature_id = creatures.id
        WHERE translations.language = 'vi' 
        AND (translations.species LIKE ? OR creatures.scientific_name LIKE ?)
    """, (f"%{query}%", f"%{query}%")).fetchall()

    return render_template("vi/tra-cuu.html", results=rows, query=query)


@app.route("/en/search", methods=["GET"]) # ENGLISH SEARCH
def search_en():
    query = request.args.get("search", "").strip()
    if not query:
        return render_template("en/search.html", results=[])

    db = get_db()
    rows = db.execute("""
        SELECT creatures.id, translations.species, creatures.scientific_name, images.photo, images.alt_text_en
        FROM creatures
        JOIN translations ON translations.creature_id = creatures.id
        JOIN images ON images.creature_id = creatures.id
        WHERE translations.language = 'en' 
        AND (translations.species LIKE ? OR creatures.scientific_name LIKE ?)
    """, (f"%{query}%", f"%{query}%")).fetchall()

    return render_template("en/search.html", results=rows, query=query, language="en")

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

@app.route("/en/sinh-vat/<int:creature_id>") # ENGLISH RESULT
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

    return render_template("en/result.html", creature=creature, language="en")

# Build this one as well
# Change the database !!!!!!!!

@app.route("/xac-minh", methods=["GET", "POST"])
def xac_minh():
    if request.method == "POST":
        password = request.form.get("password", "")

        if password == os.environ.get("ADMIN_PASSWORD"):
            session["authenticated"] = True
            return redirect(url_for("sua_doi"))

        return xin_loi("Mật khẩu không chính xác. Ngươi sẽ không vào được đâu MUAHAHAHAHAHAHAHAHA =)")

    return render_template("vi/change-database/xac-minh.html")


@app.route("/sua-doi")
def sua_doi():
    if not session.get("authenticated"):
        return redirect(url_for("xac_minh"))
    
    return render_template("vi/change-database/sua-doi.html")

@app.route("/sua-doi/them-sinh-vat", methods=["GET", "POST"])
def them_sinh_vat():
    if not session.get("authenticated"):
        return redirect(url_for("xac_minh"))

    if request.method == "POST":
        species_vi = request.form.get("species_vi")
        quick_summary_vi = request.form.get("quick_summary_vi")
        if not species_vi or not quick_summary_vi:
            return xin_loi("Tên loài và tóm tắt nhanh bằng tiếng Việt là bắt buộc")

        species_en = request.form.get("species_en")
        quick_summary_en = request.form.get("quick_summary_en")

        if not species_en or not quick_summary_en:
            return xin_loi("Tên loài và tóm tắt nhanh bằng tiếng Anh là bắt buộc")

        allowed_categories = {"animal", "plant", "fungus", ""}
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
        image.save(os.path.join("static", image_path))

        db.execute("INSERT INTO images (creature_id, photo, author, license, source, alt_text, alt_text_en) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (creature_id, image_path, author, license, source, alt_text, alt_text_en))

        db.commit()

        return redirect("/")
    
    return render_template("vi/change-database/them-sinh-vat.html")

@app.route("/sua-doi/cap-nhat")
def cap_nhat_du_lieu():
    if not session.get("authenticated"):
        return redirect(url_for("xac_minh"))

    
    query = request.args.get("search", "").strip()
    if not query:
        return render_template("vi/change-database/sua-du-lieu.html", results=[], query="")

    db = get_db()
    rows = db.execute("""
        SELECT creatures.id, translations.species, creatures.scientific_name
        FROM creatures
        JOIN translations ON translations.creature_id = creatures.id
        WHERE translations.language = 'vi' 
        AND (translations.species LIKE ? OR creatures.scientific_name LIKE ?)
    """, (f"%{query}%", f"%{query}%")).fetchall()

    return render_template("vi/change-database/sua-du-lieu.html", query=query, results=rows)

@app.route("/sua-doi/cap-nhat/<int:creature_id>", methods=["GET", "POST"])
def sua_doi_du_lieu(creature_id):
    if not session.get("authenticated"):
        return redirect(url_for("xac_minh"))

    if request.method == "GET":
        db = get_db()
        creature = db.execute("SELECT * FROM creatures WHERE id = ? ", (creature_id, )).fetchone()
        translations_vi = db.execute("SELECT * FROM translations WHERE creature_id = ? AND language = 'vi'", (creature_id, )).fetchone()
        translations_en = db.execute("SELECT * FROM translations WHERE creature_id = ? AND language = 'en'", (creature_id, )).fetchone()
        images = db.execute("SELECT * FROM images WHERE creature_id = ?", (creature_id, )).fetchone()

        if not creature or not translations_vi or not translations_en or not images:
            return xin_loi("Không tìm thấy sinh vật")
        return render_template("vi/change-database/sua-du-lieu-form.html", creature=creature, translations_vi=translations_vi, translations_en=translations_en, image=images)

    if request.method == "POST":
        species_vi = request.form.get("species_vi")
        quick_summary_vi = request.form.get("quick_summary_vi")

        species_en = request.form.get("species_en")
        quick_summary_en = request.form.get("quick_summary_en")

        category = request.form.get("category")
        era = request.form.get("era")

        scientific_name = request.form.get("scientific_name")
        taxonomic_domain = request.form.get("taxonomic_domain")
        taxonomic_kingdom = request.form.get("taxonomic_kingdom")
        taxonomic_phylum = request.form.get("taxonomic_phylum")
        taxonomic_class = request.form.get("taxonomic_class")
        taxonomic_order = request.form.get("taxonomic_order")
        taxonomic_family = request.form.get("taxonomic_family")
        taxonomic_genus = request.form.get("taxonomic_genus")

        author = request.form.get("author")
        license = request.form.get("license")
        source = request.form.get("source")
        alt_text = request.form.get("alt_text")
        alt_text_en = request.form.get("alt_text_en")

        db = get_db()
        db.execute("""UPDATE creatures
                        SET category = ?,
                        era = ?,
                        scientific_name = ?,
                        taxonomic_domain = ?,
                        taxonomic_kingdom = ?,
                        taxonomic_phylum = ?,
                        taxonomic_class = ?,
                        taxonomic_order = ?,
                        taxonomic_family = ?,
                        taxonomic_genus = ?
                        WHERE id = ? """,
                        (
                            category, 
                            era, 
                            scientific_name, 
                            taxonomic_domain, 
                            taxonomic_kingdom, 
                            taxonomic_phylum, 
                            taxonomic_class, 
                            taxonomic_order, 
                            taxonomic_family, 
                            taxonomic_genus,
                            creature_id
                        ))
        db.execute("""UPDATE translations
                        SET species = ?,
                        quick_summary = ?
                        WHERE creature_id = ?
                        AND language = 'vi'""", 
                        (
                            species_vi, quick_summary_vi, creature_id
                        )) #VIETNAMESE
        db.execute("""UPDATE translations
                        SET species = ?,
                        quick_summary = ?
                        WHERE creature_id = ?
                        AND language = 'en'""", 
                        (
                            species_en, quick_summary_en, creature_id
                        )) #ENGLISH
        db.execute("""UPDATE images
                        SET author = ?,
                        license = ?,
                        source = ?,
                        alt_text = ?,
                        alt_text_en = ?
                        WHERE creature_id = ?""", 
                        (
                            author,
                            license,
                            source,
                            alt_text,
                            alt_text_en,
                            creature_id
                        ))
        db.commit()

        return redirect("/sua-doi")

@app.route("/sua-doi/xoa", methods=["GET"])
def xoa_du_lieu():
    if not session.get("authenticated"):
        return redirect(url_for("xac_minh"))

    if request.method == "GET":
        query = request.args.get("search", "").strip()
        if not query:
            return render_template("vi/change-database/xoa-du-lieu.html", results=[], query="")

        db = get_db()
        rows = db.execute("""
            SELECT creatures.id, translations.species, creatures.scientific_name
            FROM creatures
            JOIN translations ON translations.creature_id = creatures.id
            WHERE translations.language = 'vi' 
            AND (translations.species LIKE ? OR creatures.scientific_name LIKE ?)
        """, (f"%{query}%", f"%{query}%")).fetchall()

        return render_template("vi/change-database/xoa-du-lieu.html", query=query, results=rows)

# AI helped me debugging this frustrating function.
@app.route("/sua-doi/xoa/<int:creature_id>", methods=["POST"])
def xoa_sinh_vat(creature_id):
    if not session.get("authenticated"):
        return redirect(url_for("xac_minh"))

    print("Deleting creature:", creature_id)
    db = get_db()

    db.execute("DELETE FROM images WHERE creature_id = ?", (creature_id, ))
    db.execute("DELETE FROM translations WHERE creature_id = ?", (creature_id, ))
    db.execute("DELETE FROM creatures WHERE id = ?", (creature_id, ))

    db.commit()
    return redirect("/sua-doi")

@app.route("/dang-xuat", methods=["POST"]) #so that user can log out for security
def dang_xuat():
    session.pop("authenticated", None)
    return redirect(url_for("index"))


###############################################
#                                             #
#                English version              #
#                                             #
###############################################
@app.route("/en")
def index_en():
    db = get_db()

    creatures = db.execute("""SELECT creatures.id, translations.species, creatures.scientific_name, images.photo, images.alt_text
                                FROM creatures
                                JOIN translations ON translations.creature_id = creatures.id
                                JOIN images ON images.creature_id = creatures.id
                                WHERE translations.language = 'en'
                                ORDER BY RANDOM() LIMIT 10""").fetchall()

    return render_template("en/index-en.html", creatures=creatures, language="en")

# Đầu mục sinh vật
@app.route("/en/creature/<category>")
def creature_category_en(category):
    allowed_categories = {
        "animal",
        "plant",
        "fungus",
        "insects"
    }

    if category not in allowed_categories:
        return apology("Category not found.", language="en")

    db = get_db()
    creatures = db.execute("""SELECT creatures.id, translations.species, creatures.scientific_name, images.photo, images.alt_text_en
                                FROM creatures
                                JOIN translations ON translations.creature_id = creatures.id
                                JOIN images ON images.creature_id = creatures.id
                                WHERE creatures.category = ? AND translations.language = 'en'
                                ORDER BY translations.species""", (category,)).fetchall()

    return render_template("en/creature.html", creatures=creatures, category=category, language="en")

@app.route("/en/about")
def about():
    return render_template("en/about.html", language="en")

@app.route("/en/contact")
def contact():
    return render_template("en/contact.html", language="en")


# Something else, just for fun.
@app.route("/troll")
def troll():
    return render_template("vi/troll.html")



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)