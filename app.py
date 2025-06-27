# app.py - VERSÃO COM SINTAXE CORRIGIDA
import sqlite3
import os
from flask import Flask, jsonify, request, session, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from datetime import datetime

# --- Configuração do App ---
app = Flask(__name__, static_folder='static', template_folder='templates')
app.config.from_mapping(
    SECRET_KEY='uma-chave-final-muito-segura-e-diferente',
    DATABASE='database.db',
    UPLOAD_FOLDER='static/uploads'
)
CORS(app, supports_credentials=True)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# --- Funções de Banco de Dados ---
def get_db():
    db = sqlite3.connect(app.config['DATABASE'])
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    return db


def query_db(query, args=(), one=False):
    db = get_db()
    cur = db.execute(query, args)
    rv = cur.fetchall()
    db.commit()
    cur.close()
    db.close()
    return (rv[0] if rv else None) if one else rv


# --- Rota Principal ---
@app.route('/')
def index():
    return render_template('index.html')


# --- Rotas de Autenticação ---
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password: return jsonify({'message': 'Usuário e senha são obrigatórios'}), 400
    if query_db('SELECT * FROM users WHERE username = ?', [username], one=True): return jsonify(
        {'message': 'Nome de usuário já existe'}), 409
    hashed_password = generate_password_hash(password)
    query_db('INSERT INTO users (username, password_hash) VALUES (?, ?)', [username, hashed_password])
    return jsonify({'message': 'Usuário registrado com sucesso!'}), 201


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = query_db('SELECT * FROM users WHERE username = ?', [username], one=True)
    if user and check_password_hash(user['password_hash'], password):
        session['user_id'] = user['id']
        session['username'] = user['username']
        return jsonify({'message': 'Login bem-sucedido', 'username': user['username']}), 200
    return jsonify({'message': 'Usuário ou senha inválidos'}), 401


@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logout bem-sucedido'}), 200


@app.route('/api/session')
def check_session():
    if 'user_id' in session:
        user_id = session['user_id']
        owner_pending_count_res = query_db(
            "SELECT COUNT(*) as count FROM loans WHERE owner_id = ? AND status = 'pending'", [user_id], one=True)
        owner_notifications = owner_pending_count_res['count'] if owner_pending_count_res else 0
        requester_unseen_count_res = query_db(
            "SELECT COUNT(*) as count FROM loans WHERE requester_id = ? AND status IN ('approved', 'denied') AND requester_seen = 0",
            [user_id], one=True)
        requester_notifications = requester_unseen_count_res['count'] if requester_unseen_count_res else 0
        total_notifications = owner_notifications + requester_notifications
        return jsonify(
            {'isLoggedIn': True, 'username': session['username'], 'pending_notifications': total_notifications}), 200
    return jsonify({'isLoggedIn': False}), 200


# --- Rotas de Livros (CRUD) ---
@app.route('/api/books', methods=['GET'])
def get_books():
    status_filter = request.args.get('filter', 'all')
    category_filter = request.args.get('category', 'all')
    search_term = request.args.get('search', '').strip()
    base_query = "SELECT b.*, u.username as owner FROM books b JOIN users u ON b.owner_id = u.id"
    conditions, params = [], []
    if status_filter == 'available':
        conditions.append("b.available = 1")
    elif status_filter == 'unavailable':
        conditions.append("b.available = 0")
    if category_filter != 'all':
        conditions.append("b.category = ?")
        params.append(category_filter)
    if search_term:
        conditions.append("(b.title LIKE ? OR b.author LIKE ?)")
        params.extend([f"%{search_term}%", f"%{search_term}%"])
    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)
    books = [dict(row) for row in query_db(base_query, params)]
    return jsonify(books), 200


@app.route('/api/my-books', methods=['GET'])
def get_my_books():
    if 'user_id' not in session: return jsonify([]), 200
    user_id = session['user_id']
    books_data = query_db(
        "SELECT b.*, u.username as owner FROM books b JOIN users u ON b.owner_id = u.id WHERE b.owner_id = ?",
        [user_id])
    return jsonify([dict(row) for row in books_data]), 200


@app.route('/api/books', methods=['POST'])
def add_book():
    if 'user_id' not in session: return jsonify({'message': 'Acesso não autorizado'}), 401
    title = request.form.get('title')
    author = request.form.get('author')
    description = request.form.get('description')
    category = request.form.get('category')
    cover_file = request.files.get('cover')
    if not title or not author: return jsonify({'message': 'Título e autor são obrigatórios'}), 400
    cover_path = None
    if cover_file and cover_file.filename != '':
        filename = f"user_{session['user_id']}_{cover_file.filename}"
        full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        cover_file.save(full_path)
        cover_path = os.path.join('static', 'uploads', filename).replace("\\", "/")
    query_db(
        "INSERT INTO books (title, author, description, cover_image, available, category, owner_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
        [title, author, description, cover_path, 1, category, session['user_id']])
    return jsonify({'message': 'Livro adicionado com sucesso!'}), 201


@app.route('/api/books/<int:book_id>/update', methods=['POST'])
def update_book(book_id):
    if 'user_id' not in session: return jsonify({'message': 'Acesso não autorizado'}), 401
    book = query_db('SELECT owner_id, cover_image FROM books WHERE id = ?', [book_id], one=True)
    if not book: return jsonify({'message': 'Livro não encontrado'}), 404
    if book['owner_id'] != session['user_id']: return jsonify(
        {'message': 'Você não tem permissão para editar este livro'}), 403
    title = request.form.get('title')
    author = request.form.get('author')
    description = request.form.get('description')
    category = request.form.get('category')
    query = "UPDATE books SET title = ?, author = ?, description = ?, category = ? WHERE id = ?"
    params = [title, author, description, category, book_id]
    if 'cover' in request.files and request.files['cover'].filename != '':
        cover_file = request.files['cover']
        if book['cover_image']:
            try:
                os.remove(os.path.join(os.getcwd(), book['cover_image']))
            except Exception as e:
                print(f"Erro ao remover imagem antiga: {e}")
        filename = f"user_{session['user_id']}_{cover_file.filename}"
        full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        cover_file.save(full_path)
        cover_path = os.path.join('static', 'uploads', filename).replace("\\", "/")
        query = "UPDATE books SET title = ?, author = ?, description = ?, category = ?, cover_image = ? WHERE id = ?"
        params = [title, author, description, category, cover_path, book_id]
    query_db(query, params)
    updated_book = query_db(
        "SELECT b.*, u.username as owner FROM books b JOIN users u ON b.owner_id = u.id WHERE b.id = ?", [book_id],
        one=True)
    return jsonify(dict(updated_book)), 200


@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    if 'user_id' not in session: return jsonify({'message': 'Acesso não autorizado'}), 401
    book = query_db('SELECT owner_id, cover_image FROM books WHERE id = ?', [book_id], one=True)
    if not book: return jsonify({'message': 'Livro não encontrado'}), 404
    if book['owner_id'] != session['user_id']: return jsonify(
        {'message': 'Você não tem permissão para remover este livro'}), 403
    if book['cover_image']:
        try:
            os.remove(os.path.join(os.getcwd(), book['cover_image']))
        except Exception as e:
            print(f"Erro ao remover imagem de capa: {e}")
    query_db('DELETE FROM books WHERE id = ?', [book_id])
    return jsonify({'message': 'Livro removido com sucesso!'}), 200


# --- Rotas do Sistema de Empréstimos ---
@app.route('/api/books/<int:book_id>/request', methods=['POST'])
def request_loan(book_id):
    if 'user_id' not in session: return jsonify({'message': 'Você precisa estar logado.'}), 401
    data = request.get_json()
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    if not start_date or not end_date: return jsonify({'message': 'Selecione as datas de início e fim.'}), 400
    book = query_db('SELECT owner_id, available FROM books WHERE id = ?', [book_id], one=True)
    if not book: return jsonify({'message': 'Livro não encontrado.'}), 404
    if not book['available']: return jsonify({'message': 'Este livro já está emprestado.'}), 409
    if book['owner_id'] == session['user_id']: return jsonify(
        {'message': 'Você não pode solicitar seu próprio livro.'}), 403
    existing_loan = query_db(
        "SELECT * FROM loans WHERE book_id = ? AND requester_id = ? AND status IN ('pending', 'approved')",
        [book_id, session['user_id']], one=True)
    if existing_loan: return jsonify({'message': 'Você já tem uma solicitação para este livro.'}), 409
    query_db(
        "INSERT INTO loans (book_id, requester_id, owner_id, status, start_date, end_date) VALUES (?, ?, ?, ?, ?, ?)",
        [book_id, session['user_id'], book['owner_id'], 'pending', start_date, end_date])
    return jsonify({'message': 'Solicitação de empréstimo enviada!'}), 201


@app.route('/api/loans/dashboard')
def loan_dashboard():
    if 'user_id' not in session: return jsonify({'my_requests': [], 'received_requests': []}), 401
    user_id = session['user_id']
    my_requests_q = "SELECT l.*, b.title, b.cover_image, u.username as owner_name FROM loans l JOIN books b ON l.book_id = b.id JOIN users u ON l.owner_id = u.id WHERE l.requester_id = ? ORDER BY l.request_date DESC"
    my_requests = [dict(row) for row in query_db(my_requests_q, [user_id])]
    received_requests_q = "SELECT l.*, b.title, b.cover_image, u.username as requester_name FROM loans l JOIN books b ON l.book_id = b.id JOIN users u ON l.requester_id = u.id WHERE l.owner_id = ? ORDER BY l.request_date DESC"
    received_requests = [dict(row) for row in query_db(received_requests_q, [user_id])]
    return jsonify({'my_requests': my_requests, 'received_requests': received_requests}), 200


@app.route('/api/loans/<int:loan_id>/<action>', methods=['POST'])
def handle_loan_action(loan_id, action):
    if 'user_id' not in session: return jsonify({'message': 'Acesso não autorizado.'}), 401
    loan = query_db("SELECT * FROM loans WHERE id = ?", [loan_id], one=True)
    if not loan: return jsonify({'message': 'Solicitação não encontrada.'}), 404
    if loan['owner_id'] != session['user_id']: return jsonify(
        {'message': 'Você não tem permissão para esta ação.'}), 403
    now = datetime.utcnow()
    if action == 'approve' or action == 'deny':
        if loan['status'] != 'pending': return jsonify({'message': 'Esta solicitação já foi respondida.'}), 409
        new_status = 'approved' if action == 'approve' else 'denied'
        query_db("UPDATE loans SET status = ?, decision_date = ?, requester_seen = 0 WHERE id = ?",
                 [new_status, now, loan_id])
        if new_status == 'approved':
            query_db("UPDATE books SET available = 0 WHERE id = ?", [loan['book_id']])
            query_db("UPDATE loans SET status = 'denied', requester_seen = 0 WHERE book_id = ? AND status = 'pending'",
                     [loan['book_id']])
        return jsonify({'message': f'Solicitação respondida com "{new_status}"!'}), 200
    elif action == 'return':
        if loan['status'] != 'approved': return jsonify({'message': 'Este livro não está atualmente emprestado.'}), 409
        query_db("UPDATE loans SET status = 'returned', return_date = ?, requester_seen = 0 WHERE id = ?",
                 [now, loan_id])
        query_db("UPDATE books SET available = 1 WHERE id = ?", [loan['book_id']])
        return jsonify({'message': 'Livro marcado como devolvido.'}), 200
    return jsonify({'message': 'Ação inválida.'}), 400


@app.route('/api/loans/mark-seen', methods=['POST'])
def mark_notifications_seen():
    if 'user_id' not in session: return jsonify({'message': 'Acesso não autorizado.'}), 401
    user_id = session['user_id']
    query_db(
        "UPDATE loans SET requester_seen = 1 WHERE requester_id = ? AND status IN ('approved', 'denied') AND requester_seen = 0",
        [user_id])
    return jsonify({'message': 'Notificações marcadas como vistas.'}), 200


# --- Execução do App ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)
