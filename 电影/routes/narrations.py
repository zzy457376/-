from flask import Blueprint, request, jsonify, render_template
from routes.db import get_connection, close_connection

narrations_bp = Blueprint('narrations', __name__)

@narrations_bp.route('/', methods=['GET'])
def narrations_page():
    return render_template('narrations.html')

@narrations_bp.route('/list', methods=['GET'])
def list_narrations():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    # 左连接演员和电影，方便前端显示名字
    sql = '''
        SELECT n.narration_id, n.content, n.actor_id, n.movie_id,
               a.name AS actor_name,
               m.title AS movie_title
        FROM Narration n
        LEFT JOIN Actor a ON n.actor_id = a.actor_id
        LEFT JOIN Movie m ON n.movie_id = m.movie_id
    '''
    cursor.execute(sql)
    narrations = cursor.fetchall()
    cursor.close()
    close_connection(conn)
    return jsonify(narrations)

@narrations_bp.route('/add', methods=['POST'])
def add_narration():
    data = request.json
    content = data.get('content')
    actor_id = data.get('actor_id')
    movie_id = data.get('movie_id')

    if not content:
        return jsonify({'error': '内容不能为空'}), 400
    if not movie_id:
        return jsonify({'error': '电影不能为空'}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Narration (content, actor_id, movie_id) VALUES (%s, %s, %s)",
        (content, actor_id, movie_id)
    )
    conn.commit()
    cursor.close()
    close_connection(conn)
    return jsonify({'message': '旁白添加成功'}), 201

@narrations_bp.route('/<int:narration_id>', methods=['PUT'])
def update_narration(narration_id):
    data = request.json
    content = data.get('content')
    actor_id = data.get('actor_id')
    movie_id = data.get('movie_id')

    if not content:
        return jsonify({'error': '内容不能为空'}), 400
    if not movie_id:
        return jsonify({'error': '电影不能为空'}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Narration SET content=%s, actor_id=%s, movie_id=%s WHERE narration_id=%s",
        (content, actor_id, movie_id, narration_id)
    )
    conn.commit()
    cursor.close()
    close_connection(conn)
    return jsonify({'message': '旁白更新成功'})

@narrations_bp.route('/<int:narration_id>', methods=['DELETE'])
def delete_narration(narration_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Narration WHERE narration_id=%s", (narration_id,))
    conn.commit()
    cursor.close()
    close_connection(conn)
    return jsonify({'message': '旁白删除成功'})

@narrations_bp.route('/search', methods=['GET'])
def search_narrations():
    keyword = request.args.get('keyword', '').strip()
    if not keyword:
        # 关键词空，返回空列表
        return jsonify([])

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = '''
        SELECT n.narration_id, n.content, n.actor_id, n.movie_id,
               a.name AS actor_name,
               m.title AS movie_title
        FROM Narration n
        LEFT JOIN Actor a ON n.actor_id = a.actor_id
        LEFT JOIN Movie m ON n.movie_id = m.movie_id
        WHERE n.content LIKE %s
    '''
    like_pattern = f"%{keyword}%"
    cursor.execute(sql, (like_pattern,))
    narrations = cursor.fetchall()
    cursor.close()
    close_connection(conn)
    return jsonify(narrations)



