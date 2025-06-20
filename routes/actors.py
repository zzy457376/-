from flask import Blueprint, request, jsonify, render_template
from routes.db import get_connection, close_connection
import traceback

actors_bp = Blueprint('actors', __name__)

# 1. 演员管理页面
@actors_bp.route('/', methods=['GET'])
def actors_page():
    return render_template('actors.html')

# 2. 查询所有演员
@actors_bp.route('/list', methods=['GET'])
def list_actors():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Actor")
    actors = cursor.fetchall()
    cursor.close()
    close_connection(conn)
    return jsonify(actors)

# 3. 新增演员
@actors_bp.route('/add', methods=['POST'])
def add_actor():
    data = request.json
    name = data.get('name')
    dob = data.get('dob')  

    if not name:
        return jsonify({'error': '演员姓名不能为空'}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Actor (name, dob) VALUES (%s, %s)", (name, dob))
    conn.commit()
    cursor.close()
    close_connection(conn)
    return jsonify({'message': '演员添加成功'}), 201

# 4. 更新演员信息
@actors_bp.route('/<int:actor_id>', methods=['PUT'])
def update_actor(actor_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '请求体必须为JSON'}), 400

        name = data.get('name')
        dob = data.get('dob')
        if dob == '':
            dob = None

        if not name:
            return jsonify({'error': '演员姓名不能为空'}), 400

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Actor WHERE actor_id = %s", (actor_id,))
        if cursor.fetchone()[0] == 0:
            cursor.close()
            close_connection(conn)
            return jsonify({'error': '演员不存在'}), 404

        cursor.execute("UPDATE Actor SET name=%s, dob=%s WHERE actor_id=%s",
                       (name, dob, actor_id))
        conn.commit()
        cursor.close()
        close_connection(conn)
        return jsonify({'message': '演员信息更新成功'})

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': '服务器内部错误，请检查后端控制台'}), 500

# 5. 删除演员
@actors_bp.route('/<int:actor_id>', methods=['DELETE'])
def delete_actor(actor_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Actor WHERE actor_id=%s", (actor_id,))
    conn.commit()
    cursor.close()
    close_connection(conn)
    return jsonify({'message': '演员删除成功'})

# 6. 查询单个演员详情（含角色、旁白）
@actors_bp.route('/detail/<int:actor_id>', methods=['GET'])
def actor_detail(actor_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # 基本信息
    cursor.execute("SELECT * FROM Actor WHERE actor_id = %s", (actor_id,))
    actor = cursor.fetchone()

    # 角色信息
    cursor.execute("""
        SELECT R.role_id, R.role_name, M.movie_id, M.title
        FROM Role R
        JOIN Movie M ON R.movie_id = M.movie_id
        WHERE R.actor_id = %s
    """, (actor_id,))
    roles = cursor.fetchall()

    # 旁白信息
    cursor.execute("""
        SELECT N.narration_id, N.content, M.movie_id, M.title
        FROM Narration N
        JOIN Movie M ON N.movie_id = M.movie_id
        WHERE N.actor_id = %s
    """, (actor_id,))
    narrations = cursor.fetchall()

    cursor.close()
    close_connection(conn)

    if not actor:
        return jsonify({'error': '演员不存在'}), 404

    return jsonify({
        'actor': actor,
        'roles': roles,
        'narrations': narrations
    })

# 7. 模糊搜索演员（按姓名）
@actors_bp.route('/search', methods=['GET'])
def search_actor():
    keyword = request.args.get('keyword', '')
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    search_term = f"%{keyword}%"
    cursor.execute("SELECT * FROM Actor WHERE name LIKE %s", (search_term,))
    actors = cursor.fetchall()
    cursor.close()
    close_connection(conn)
    return jsonify(actors)














