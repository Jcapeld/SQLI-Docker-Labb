import os
import time
import pymysql
from flask import Flask, request, make_response, render_template

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "sqli_lab")
DB_USER = os.getenv("DB_USER", "labuser")
DB_PASS = os.getenv("DB_PASS", "labpass")

def get_conn():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        charset="utf8mb4",
        autocommit=True,
    )

def db_query_unsafe(sql: str):
    # Intencionadamente inseguro: ejecuta SQL construido por concatenación.
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
        return rows, None
    except Exception as e:
        return None, str(e)
    finally:
        conn.close()

@app.get("/")
def index():
    # BLIND BOOLEAN-BASED (cookie)
    tracking = request.cookies.get("TrackingId", "abc123")

    # VULNERABLE: concatenación directa (blind boolean)
    sql = f"SELECT tracking_id FROM tracking WHERE tracking_id = '{tracking}'"
    rows, err = db_query_unsafe(sql)

    welcome = (rows is not None and len(rows) > 0)

    resp = make_response(render_template(
        "index.html",
        tracking=tracking,
        welcome=welcome,
        sql_preview=sql
    ))

    # Si no existe cookie, set inicial
    if "TrackingId" not in request.cookies:
        resp.set_cookie("TrackingId", "abc123", httponly=False)

    return resp

@app.get("/products")
def products():
    # UNION-BASED
    category = request.args.get("category", "Gifts")

    # 3 columnas para que UNION encaje fácil (id, name, price)
    sql = f"SELECT id, name, price FROM products WHERE category = '{category}'"
    rows, err = db_query_unsafe(sql)

    return render_template(
        "products.html",
        category=category,
        rows=rows,
        err=err,
        sql_preview=sql
    )

@app.get("/search")
def search():
    # BLIND TIME-BASED
    q = request.args.get("q", "")

    # VULNERABLE: concatenación directa.
    # Nota: la respuesta NO muestra resultados (para que sea blind).
    sql = f"SELECT id, name FROM products WHERE name LIKE '%{q}%'"
    t0 = time.time()
    _, err = db_query_unsafe(sql)
    dt = time.time() - t0

    return render_template(
        "search.html",
        q=q,
        elapsed=dt,
        err=err,
        sql_preview=sql
    )

@app.get("/account")
def account():
    # ERROR-BASED (muestra error de SQL)
    user_id = request.args.get("id", "1")

    # VULNERABLE: concatenación directa SIN comillas (para jugar con casts/funciones)
    sql = f"SELECT id, username, email FROM users WHERE id = {user_id}"
    rows, err = db_query_unsafe(sql)

    user = None
    if rows:
        # rows: tuple of tuples
        r = rows[0]
        user = {"id": r[0], "username": r[1], "email": r[2]}

    return render_template(
        "account.html",
        user_id=user_id,
        user=user,
        err=err,
        sql_preview=sql
    )

@app.get("/health")
def health():
    rows, err = db_query_unsafe("SELECT 1")
    if err:
        return {"ok": False, "error": err}, 500
    return {"ok": True}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
