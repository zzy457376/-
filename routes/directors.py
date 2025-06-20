from flask import Blueprint, request, jsonify, render_template
from routes.db import get_connection, close_connection
import traceback

directors_bp = Blueprint('directors', __name__)

# 1. 导演管理页面
@directors_bp.route('/', methods=['GET'])
def directors_page():
    return render_template('directors.html')


# 2. 获取所有导演
@directors_bp.route('/list', methods=['GET'])
def list_directors():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('''
            SELECT d.director_id, d.name, d.dob,
                   GROUP_CONCAT(DISTINCT m.title) AS movies,
                   GROUP_CONCAT(DISTINCT m.movie_id) AS movie_ids
            FROM Director d
            LEFT JOIN Movie_Director md ON d.director_id = md.director_id
            LEFT JOIN Movie m ON md.movie_id = m.movie_id
            GROUP BY d.director_id
            ORDER BY d.director_id
        ''')
        directors = cursor.fetchall()
    finally:
        cursor.close()
        close_connection(conn)
    return jsonify(directors)


# 3. 获取单个导演信息
@directors_bp.route('/<int:director_id>', methods=['GET'])
def get_director(director_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('''
            SELECT d.director_id, d.name, d.dob,
                   GROUP_CONCAT(DISTINCT m.title) AS movies,
                   GROUP_CONCAT(DISTINCT m.movie_id) AS movie_ids
            FROM Director d
            LEFT JOIN Movie_Director md ON d.director_id = md.director_id
            LEFT JOIN Movie m ON md.movie_id = m.movie_id
            WHERE d.director_id = %s
            GROUP BY d.director_id
        ''', (director_id,))
        director = cursor.fetchone()
    finally:
        cursor.close()
        close_connection(conn)
    if director:
        return jsonify(director)
    else:
        return jsonify({'error': '导演不存在'}), 404


# 4. 添加导演
@directors_bp.route('/add', methods=['POST'])
def add_director():
    try:
        data = request.get_json()
        name = data.get('name')
        dob = data.get('dob')
        movies = data.get('movies', [])

        if not name:
            return jsonify({'error': '导演姓名不能为空'}), 400

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO Director (name, dob) VALUES (%s, %s)', (name, dob))
            director_id = cursor.lastrowid
            for movie_id in movies:
                cursor.execute('INSERT INTO Movie_Director (movie_id, director_id) VALUES (%s, %s)', (movie_id, director_id))
            conn.commit()
        finally:
            cursor.close()
            close_connection(conn)

        return jsonify({'message': '导演添加成功', 'director_id': director_id}), 201
    except Exception:
        traceback.print_exc()
        return jsonify({'error': '服务器内部错误'}), 500


# 5. 更新导演
@directors_bp.route('/<int:director_id>', methods=['PUT'])
def update_director(director_id):
    try:
        data = request.get_json()
        name = data.get('name')
        dob = data.get('dob')
        movies = data.get('movies', [])

        if not name:
            return jsonify({'error': '导演姓名不能为空'}), 400

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT COUNT(*) FROM Director WHERE director_id=%s', (director_id,))
            if cursor.fetchone()[0] == 0:
                return jsonify({'error': '导演不存在'}), 404

            cursor.execute('UPDATE Director SET name=%s, dob=%s WHERE director_id=%s', (name, dob, director_id))
            cursor.execute('DELETE FROM Movie_Director WHERE director_id=%s', (director_id,))
            for movie_id in movies:
                cursor.execute('INSERT INTO Movie_Director (movie_id, director_id) VALUES (%s, %s)', (movie_id, director_id))
            conn.commit()
        finally:
            cursor.close()
            close_connection(conn)

        return jsonify({'message': '导演信息更新成功'})
    except Exception:
        traceback.print_exc()
        return jsonify({'error': '服务器内部错误'}), 500


# 6. 删除导演
@directors_bp.route('/<int:director_id>', methods=['DELETE'])
def delete_director(director_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM Director WHERE director_id=%s', (director_id,))
        conn.commit()
    finally:
        cursor.close()
        close_connection(conn)
    return jsonify({'message': '导演删除成功'})


# 7. 模糊搜索导演
@directors_bp.route('/search', methods=['GET'])
def search_director():
    keyword = request.args.get('keyword', '').strip()
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        like_pattern = f'%{keyword}%'
        cursor.execute('''
            SELECT d.director_id, d.name, d.dob,
                   GROUP_CONCAT(DISTINCT m.title) AS movies,
                   GROUP_CONCAT(DISTINCT m.movie_id) AS movie_ids
            FROM Director d
            LEFT JOIN Movie_Director md ON d.director_id = md.director_id
            LEFT JOIN Movie m ON md.movie_id = m.movie_id
            WHERE d.name LIKE %s
            GROUP BY d.director_id
        ''', (like_pattern,))
        directors = cursor.fetchall()
    finally:
        cursor.close()
        close_connection(conn)
    return jsonify(directors)








