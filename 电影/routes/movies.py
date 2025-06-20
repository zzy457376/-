from flask import Blueprint, request, jsonify, render_template
from routes.db import get_connection, close_connection
import traceback

movies_bp = Blueprint('movies', __name__)

@movies_bp.route('/', methods=['GET'])
def movies_page():
    return render_template('movies.html')

@movies_bp.route('/list', methods=['GET'])
def list_movies():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT m.movie_id, m.title, m.release_year, m.duration, m.synopsis,
               c.production_company_id, c.name AS company_name,
               GROUP_CONCAT(DISTINCT g.name) AS genres,
               GROUP_CONCAT(DISTINCT d.name) AS directors
        FROM Movie m
        LEFT JOIN Production_Company c ON m.production_company_id = c.production_company_id
        LEFT JOIN Movie_Genre mg ON m.movie_id = mg.movie_id
        LEFT JOIN Genre g ON mg.genre_id = g.genre_id
        LEFT JOIN Movie_Director md ON m.movie_id = md.movie_id
        LEFT JOIN Director d ON md.director_id = d.director_id
        GROUP BY m.movie_id
        ORDER BY m.movie_id
    ''')
    movies = cursor.fetchall()
    cursor.close()
    close_connection(conn)
    return jsonify(movies)

@movies_bp.route('/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT m.movie_id, m.title, m.release_year, m.duration, m.synopsis,
               c.production_company_id, c.name AS company_name,
               GROUP_CONCAT(DISTINCT g.genre_id) AS genre_ids,
               GROUP_CONCAT(DISTINCT g.name) AS genres,
               GROUP_CONCAT(DISTINCT d.director_id) AS director_ids,
               GROUP_CONCAT(DISTINCT d.name) AS directors
        FROM Movie m
        LEFT JOIN Production_Company c ON m.production_company_id = c.production_company_id
        LEFT JOIN Movie_Genre mg ON m.movie_id = mg.movie_id
        LEFT JOIN Genre g ON mg.genre_id = g.genre_id
        LEFT JOIN Movie_Director md ON m.movie_id = md.movie_id
        LEFT JOIN Director d ON md.director_id = d.director_id
        WHERE m.movie_id = %s
        GROUP BY m.movie_id
    ''', (movie_id,))
    movie = cursor.fetchone()
    cursor.close()
    close_connection(conn)
    if movie:
        return jsonify(movie)
    else:
        return jsonify({'error': '电影不存在'}), 404

@movies_bp.route('/add', methods=['POST'])
def add_movie():
    try:
        data = request.get_json()
        title = data.get('title')
        release_year = data.get('release_year')
        duration = data.get('duration')
        production_company_id = data.get('production_company_id')
        synopsis = data.get('synopsis')
        genres = data.get('genres', [])        # 期望为列表，元素是genre_id
        directors = data.get('directors', [])  # 期望为列表，元素是director_id

        if not title or not release_year or not duration or not production_company_id:
            return jsonify({'error': '缺少必要字段'}), 400

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Movie (title, release_year, duration, production_company_id, synopsis)
            VALUES (%s, %s, %s, %s, %s)
        ''', (title, release_year, duration, production_company_id, synopsis))
        movie_id = cursor.lastrowid

        # 插入电影类别关联
        for genre_id in genres:
            cursor.execute('INSERT INTO Movie_Genre (movie_id, genre_id) VALUES (%s, %s)', (movie_id, genre_id))

        # 插入电影导演关联
        for director_id in directors:
            cursor.execute('INSERT INTO Movie_Director (movie_id, director_id) VALUES (%s, %s)', (movie_id, director_id))

        conn.commit()
        cursor.close()
        close_connection(conn)
        return jsonify({'message': '电影添加成功', 'movie_id': movie_id}), 201
    except Exception:
        traceback.print_exc()
        return jsonify({'error': '服务器错误'}), 500

@movies_bp.route('/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    try:
        data = request.get_json()
        title = data.get('title')
        release_year = data.get('release_year')
        duration = data.get('duration')
        production_company_id = data.get('production_company_id')
        synopsis = data.get('synopsis')
        genres = data.get('genres', [])
        directors = data.get('directors', [])

        if not title or not release_year or not duration or not production_company_id:
            return jsonify({'error': '缺少必要字段'}), 400

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM Movie WHERE movie_id=%s', (movie_id,))
        if cursor.fetchone()[0] == 0:
            cursor.close()
            close_connection(conn)
            return jsonify({'error': '电影不存在'}), 404

        cursor.execute('''
            UPDATE Movie SET title=%s, release_year=%s, duration=%s, production_company_id=%s, synopsis=%s
            WHERE movie_id=%s
        ''', (title, release_year, duration, production_company_id, synopsis, movie_id))

        # 先删除旧的关联关系
        cursor.execute('DELETE FROM Movie_Genre WHERE movie_id=%s', (movie_id,))
        cursor.execute('DELETE FROM Movie_Director WHERE movie_id=%s', (movie_id,))

        # 插入新的关联关系
        for genre_id in genres:
            cursor.execute('INSERT INTO Movie_Genre (movie_id, genre_id) VALUES (%s, %s)', (movie_id, genre_id))
        for director_id in directors:
            cursor.execute('INSERT INTO Movie_Director (movie_id, director_id) VALUES (%s, %s)', (movie_id, director_id))

        conn.commit()
        cursor.close()
        close_connection(conn)
        return jsonify({'message': '电影信息更新成功'})
    except Exception:
        traceback.print_exc()
        return jsonify({'error': '服务器错误'}), 500

@movies_bp.route('/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Movie WHERE movie_id=%s', (movie_id,))
    conn.commit()
    cursor.close()
    close_connection(conn)
    return jsonify({'message': '电影删除成功'})

@movies_bp.route('/search', methods=['GET'])
def search_movies():
    keyword = request.args.get('keyword', '').strip()
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    like_pattern = f'%{keyword}%'
    cursor.execute('''
        SELECT m.movie_id, m.title, m.release_year, m.duration, m.synopsis,
               c.production_company_id, c.name AS company_name,
               GROUP_CONCAT(DISTINCT g.name) AS genres,
               GROUP_CONCAT(DISTINCT d.name) AS directors
        FROM Movie m
        LEFT JOIN Production_Company c ON m.production_company_id = c.production_company_id
        LEFT JOIN Movie_Genre mg ON m.movie_id = mg.movie_id
        LEFT JOIN Genre g ON mg.genre_id = g.genre_id
        LEFT JOIN Movie_Director md ON m.movie_id = md.movie_id
        LEFT JOIN Director d ON md.director_id = d.director_id
        WHERE m.title LIKE %s
        GROUP BY m.movie_id
    ''', (like_pattern,))
    movies = cursor.fetchall()
    cursor.close()
    close_connection(conn)
    return jsonify(movies)




