from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# === INICIALIZAR TABLA ===
def init_db():
    conn = sqlite3.connect("kardex.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS personas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            telefono TEXT,
            fecha_nacimiento DATE NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# === LISTAR PERSONAS ===
@app.route("/personas")
def personas_index():
    conn = sqlite3.connect("kardex.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personas")
    personas = cursor.fetchall()
    conn.close()
    return render_template("personas/index.html", personas=personas)

# === FORMULARIO NUEVA PERSONA ===
@app.route("/personas/create")
def persona_create():
    return render_template("personas/create.html")

# === GUARDAR NUEVA PERSONA ===
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

# === FORMULARIO EDITAR ===
@app.route("/personas/edit/<int:id>")
def persona_edit(id):
    conn = sqlite3.connect("kardex.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personas WHERE id = ?", (id,))
    persona = cursor.fetchone()
    conn.close()
    return render_template("personas/edit.html", persona=persona)

# === ACTUALIZAR PERSONA ===
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

# === ELIMINAR PERSONA ===
@app.route("/personas/delete/<int:id>")
def personas_delete(id):
    conn = sqlite3.connect("kardex.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM personas WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/personas")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)