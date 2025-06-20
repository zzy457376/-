from flask import Blueprint, request, jsonify, render_template
from routes.db import get_connection, close_connection

companies_bp = Blueprint('companies', __name__)

@companies_bp.route('/', methods=['GET'])
def companies_page():
    return render_template('companies.html')

@companies_bp.route('/list', methods=['GET'])
def list_companies():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Production_Company")
    companies = cursor.fetchall()
    cursor.close()
    close_connection(conn)
    return jsonify(companies)

@companies_bp.route('/add', methods=['POST'])
def add_company():
    data = request.json
    name = data.get('name')
    city = data.get('city')
    if not name:
        return jsonify({'error': '公司名称不能为空'}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Production_Company (name, city) VALUES (%s, %s)", (name, city))
    conn.commit()
    cursor.close()
    close_connection(conn)
    return jsonify({'message': '公司添加成功'}), 201

@companies_bp.route('/<int:production_company_id>', methods=['PUT'])
def update_company(production_company_id):
    data = request.json
    name = data.get('name')
    city = data.get('city')
    if not name:
        return jsonify({'error': '公司名称不能为空'}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Production_Company SET name=%s, city=%s WHERE production_company_id=%s", (name, city, production_company_id))
    conn.commit()
    cursor.close()
    close_connection(conn)
    return jsonify({'message': '公司信息更新成功'})

@companies_bp.route('/<int:production_company_id>', methods=['DELETE'])
def delete_company(production_company_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Production_Company WHERE production_company_id=%s", (production_company_id,))
    conn.commit()
    cursor.close()
    close_connection(conn)
    return jsonify({'message': '公司删除成功'})
@companies_bp.route('/search', methods=['GET'])
def search_companies():
    keyword = request.args.get('keyword', '').strip()
    if not keyword:
        # 如果keyword空，返回空列表或者所有公司，这里返回空列表
        return jsonify([])

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    # 模糊查询，使用LIKE，注意防止SQL注入，参数化查询
    sql = "SELECT * FROM Production_Company WHERE name LIKE %s"
    like_pattern = f"%{keyword}%"
    cursor.execute(sql, (like_pattern,))
    companies = cursor.fetchall()
    cursor.close()
    close_connection(conn)
    return jsonify(companies)






