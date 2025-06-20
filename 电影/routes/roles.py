from flask import Blueprint, request, jsonify, render_template
from routes.db import get_connection, close_connection

roles_bp = Blueprint('roles', __name__)

@roles_bp.route('/', methods=['GET'])
def roles_page():
    return render_template('roles.html')

@roles_bp.route('/list', methods=['GET'])
def list_roles():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.role_id, r.role_name, r.actor_id, r.movie_id,
               a.name AS actor_name, m.title AS movie_title
        FROM Role r
        LEFT JOIN Actor a ON r.actor_id = a.actor_id
        LEFT JOIN Movie m ON r.movie_id = m.movie_id
    """)
    roles = cursor.fetchall()
    cursor.close()
    close_connection(conn)
    return jsonify(roles)

@roles_bp.route('/add', methods=['POST'])
def add_role():
    data = request.json
    role_name = data.get('role_name')
    actor_id = data.get('actor_id')
    movie_id = data.get('movie_id')

    if not role_name:
        return jsonify({'error': '角色名称不能为空'}), 400
    if not actor_id or not movie_id:
        return jsonify({'error': '必须选择演员和电影'}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Role (role_name, actor_id, movie_id) VALUES (%s, %s, %s)", 
                   (role_name, actor_id, movie_id))
    conn.commit()
    cursor.close()
    close_connection(conn)
    return jsonify({'message': '角色添加成功'}), 201

@roles_bp.route('/<int:role_id>', methods=['PUT'])
def update_role(role_id):
    data = request.json
    role_name = data.get('role_name')
    actor_id = data.get('actor_id')
    movie_id = data.get('movie_id')

    if not role_name:
        return jsonify({'error': '角色名称不能为空'}), 400
    if not actor_id or not movie_id:
        return jsonify({'error': '必须选择演员和电影'}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Role SET role_name=%s, actor_id=%s, movie_id=%s WHERE role_id=%s",
        (role_name, actor_id, movie_id, role_id)
    )
    conn.commit()
    cursor.close()
    close_connection(conn)
    return jsonify({'message': '角色信息更新成功'})

@roles_bp.route('/<int:role_id>', methods=['DELETE'])
def delete_role(role_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Role WHERE role_id=%s", (role_id,))
    conn.commit()
    cursor.close()
    close_connection(conn)
    return jsonify({'message': '角色删除成功'})

@roles_bp.route('/search', methods=['GET'])
def search_roles():
    keyword = request.args.get('keyword', '').strip()
    if not keyword:
        return jsonify([])

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = """
        SELECT r.role_id, r.role_name, r.actor_id, r.movie_id,
               a.name AS actor_name, m.title AS movie_title
        FROM Role r
        LEFT JOIN Actor a ON r.actor_id = a.actor_id
        LEFT JOIN Movie m ON r.movie_id = m.movie_id
        WHERE r.role_name LIKE %s
    """
    like_pattern = f"%{keyword}%"
    cursor.execute(sql, (like_pattern,))
    roles = cursor.fetchall()
    cursor.close()
    close_connection(conn)
    return jsonify(roles)
