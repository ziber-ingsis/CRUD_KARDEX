from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# === INICIALIZAR TODAS LAS TABLAS ===
def init_db():
    conn = sqlite3.connect("kardex.db")
    cursor = conn.cursor()
    
    # Tabla PERSONAS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS personas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            telefono TEXT,
            fecha_nacimiento DATE NOT NULL
        )
    """)
    
    # Tabla CATEGORÍAS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            descripcion TEXT
        )
    """)
    
    # Tabla UNIDADES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS unidades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            sigla TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()

# ==================== PÁGINA DE INICIO ====================
@app.route("/")
def home():
    return render_template("index.html")

# ==================== PERSONAS ====================
@app.route("/personas")
def personas_index():
    conn = sqlite3.connect("kardex.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personas")
    personas = cursor.fetchall()
    conn.close()
    return render_template("personas/index.html", personas=personas)

@app.route("/personas/create")
def persona_create():
    return render_template("personas/create.html")

@app.route("/personas/store", methods=["POST"])
def personas_store():
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    telefono = request.form["telefono"]
    fecha_nacimiento = request.form["fecha_nacimiento"]
    conn = sqlite3.connect("kardex.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO personas (nombre, apellido, telefono, fecha_nacimiento) VALUES (?, ?, ?, ?)",
        (nombre, apellido, telefono, fecha_nacimiento)
    )
    conn.commit()
    conn.close()
    return redirect("/personas")

@app.route("/personas/edit/<int:id>")
def persona_edit(id):
    conn = sqlite3.connect("kardex.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personas WHERE id = ?", (id,))
    persona = cursor.fetchone()
    conn.close()
    return render_template("personas/edit.html", persona=persona)

@app.route("/personas/update", methods=["POST"])
def personas_update():
    id = request.form["id"]
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    telefono = request.form["telefono"]
    fecha_nacimiento = request.form["fecha_nacimiento"]
    conn = sqlite3.connect("kardex.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE personas SET nombre=?, apellido=?, telefono=?, fecha_nacimiento=? WHERE id=?",
        (nombre, apellido, telefono, fecha_nacimiento, id)
    )
    conn.commit()
    conn.close()
    return redirect("/personas")

@app.route("/personas/delete/<int:id>")
def personas_delete(id):
    conn = sqlite3.connect("kardex.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM personas WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/personas")

# ==================== CATEGORÍAS ====================
@app.route("/categorias")
def categorias_index():
    conn = sqlite3.connect("kardex.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categorias")
    categorias = cursor.fetchall()
    conn.close()
    return render_template("categorias/index.html", categorias=categorias)

@app.route("/categorias/create")
def categoria_create():
    return render_template("categorias/create.html")

@app.route("/categorias/store", methods=["POST"])
def categorias_store():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    conn = sqlite3.connect("kardex.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO categorias (nombre, descripcion) VALUES (?, ?)",
        (nombre, descripcion)
    )
    conn.commit()
    conn.close()
    return redirect("/categorias")

@app.route("/categorias/edit/<int:id>")
def categoria_edit(id):
    conn = sqlite3.connect("kardex.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categorias WHERE id = ?", (id,))
    categoria = cursor.fetchone()
    conn.close()
    return render_template("categorias/edit.html", categoria=categoria)

@app.route("/categorias/update", methods=["POST"])
def categorias_update():
    id = request.form["id"]
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    conn = sqlite3.connect("kardex.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE categorias SET nombre=?, descripcion=? WHERE id=?",
        (nombre, descripcion, id)
    )
    conn.commit()
    conn.close()
    return redirect("/categorias")

@app.route("/categorias/delete/<int:id>")
def categorias_delete(id):
    conn = sqlite3.connect("kardex.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categorias WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/categorias")

# ==================== UNIDADES ====================
@app.route("/unidades")
def unidades_index():
    conn = sqlite3.connect("kardex.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM unidades")
    unidades = cursor.fetchall()
    conn.close()
    return render_template("unidades/index.html", unidades=unidades)

@app.route("/unidades/create")
def unidad_create():
    return render_template("unidades/create.html")

@app.route("/unidades/store", methods=["POST"])
def unidades_store():
    nombre = request.form["nombre"]
    sigla = request.form["sigla"]
    conn = sqlite3.connect("kardex.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO unidades (nombre, sigla) VALUES (?, ?)",
        (nombre, sigla)
    )
    conn.commit()
    conn.close()
    return redirect("/unidades")

@app.route("/unidades/edit/<int:id>")
def unidad_edit(id):
    conn = sqlite3.connect("kardex.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM unidades WHERE id = ?", (id,))
    unidad = cursor.fetchone()
    conn.close()
    return render_template("unidades/edit.html", unidad=unidad)

@app.route("/unidades/update", methods=["POST"])
def unidades_update():
    id = request.form["id"]
    nombre = request.form["nombre"]
    sigla = request.form["sigla"]
    conn = sqlite3.connect("kardex.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE unidades SET nombre=?, sigla=? WHERE id=?",
        (nombre, sigla, id)
    )
    conn.commit()
    conn.close()
    return redirect("/unidades")

@app.route("/unidades/delete/<int:id>")
def unidades_delete(id):
    conn = sqlite3.connect("kardex.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM unidades WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/unidades")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)