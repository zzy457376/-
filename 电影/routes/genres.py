from flask import Blueprint, request, jsonify, render_template
from routes.db import get_connection, close_connection

genres_bp = Blueprint('genres', __name__)

@genres_bp.route('/', methods=['GET'])
def genres_page():
    return render_template('genres.html')

@genres_bp.route('/list', methods=['GET'])
def list_genres():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Genre")
    genres = cursor.fetchall()
    cursor.close()
    close_connection(conn)
    return jsonify(genres)

@genres_bp.route('/add', methods=['POST'])
def add_genre():
    data = request.json
    name = data.get('name')
    if not name:
        return jsonify({'error': '类型名称不能为空'}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Genre (name) VALUES (%s)", (name,))
    conn.commit()
    cursor.close()
    close_connection(conn)
    return jsonify({'message': '类型添加成功'}), 201

@genres_bp.route('/<int:genre_id>', methods=['PUT'])
def update_genre(genre_id):
    data = request.json
    if not data:
        return jsonify({'error': '请求体不能为空'}), 400
    name = data.get('name')
    if not name:
        return jsonify({'error': '类型名称不能为空'}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Genre WHERE genre_id = %s", (genre_id,))
    if cursor.fetchone()[0] == 0:
        cursor.close()
        close_connection(conn)
        return jsonify({'error': '类型不存在'}), 404

    cursor.execute("UPDATE Genre SET name=%s WHERE genre_id=%s", (name, genre_id))
    conn.commit()
    cursor.close()
    close_connection(conn)
    return jsonify({'message': '类型信息更新成功'})

@genres_bp.route('/<int:genre_id>', methods=['DELETE'])
def delete_genre(genre_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Genre WHERE genre_id=%s", (genre_id,))
    conn.commit()
    cursor.close()
    close_connection(conn)
    return jsonify({'message': '类型删除成功'})

@genres_bp.route('/search', methods=['GET'])
def search_genre():
    keyword = request.args.get('keyword', '').strip()
    if not keyword:
        return jsonify([])

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    like_pattern = f"%{keyword}%"
    cursor.execute("SELECT * FROM Genre WHERE name LIKE %s", (like_pattern,))
    genres = cursor.fetchall()
    cursor.close()
    close_connection(conn)
    return jsonify(genres)




