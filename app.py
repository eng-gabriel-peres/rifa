from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)
DB = "rifa.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db()
    numeros = conn.execute("SELECT * FROM numeros").fetchall()
    conn.close()
    return render_template("index.html", numeros=numeros)

@app.route("/reservar", methods=["POST"])
def reservar():
    data = request.json

    nome = data["nome"]
    cpf = data["cpf"]
    celular = data["celular"]
    numeros = data["numeros"]

    cpf_mask = "****" + cpf[-4:]
    cel_mask = "****" + celular[-4:]

    conn = get_db()
    for n in numeros:
        conn.execute("""
            UPDATE numeros
            SET nome=?, cpf=?, celular=?, reservado=1
            WHERE numero=? AND reservado=0
        """, (nome, cpf_mask, cel_mask, n))

    conn.commit()
    conn.close()

    return jsonify({"status": "ok"})

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS numeros (
            numero INTEGER PRIMARY KEY,
            nome TEXT,
            cpf TEXT,
            celular TEXT,
            reservado INTEGER DEFAULT 0
        )
    """)

    for i in range(1, 301):
        conn.execute(
            "INSERT OR IGNORE INTO numeros (numero) VALUES (?)", (i,)
        )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
