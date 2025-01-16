from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import mysql.connector
import os, time
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_wtf.csrf import CSRFProtect
from flag_generate import create_discount_code
FLAG = os.getenv('FLAG') or "FLAG{BUY1000OFF}"
app = Flask(__name__)
app.secret_key = os.urandom(24)

# 資料庫連接重試函數
def get_db_connection(max_retries=10, delay_seconds=5):
    for attempt in range(max_retries):
        try:
            return mysql.connector.connect(
                    host=os.getenv('MYSQL_HOST'),
                    user=os.getenv('MYSQL_USER') or "shop_user",
                    password=os.getenv('MYSQL_PASSWORD') or "shop_password123",
                    database=os.getenv('MYSQL_DATABASE') or "laptop_shop",
                    charset='utf8mb4',
                    collation='utf8mb4_unicode_ci'
                )
        except mysql.connector.Error as err:
            if attempt == max_retries - 1:
                raise
            print(f"資料庫連接失敗，{delay_seconds} 秒後重試... (嘗試 {attempt + 1}/{max_retries})")
            print(f"錯誤: {err}")
            time.sleep(delay_seconds)

# 在啟動 Flask 前建立折扣碼
try:
    db = get_db_connection()
    cursor = db.cursor()
    # 使用 flag.py 中的函數建立折扣碼
    if create_discount_code(cursor, FLAG):
        print("成功建立折扣碼")
        db.commit()
    else:
        print("建立折扣碼失敗")
        
except Exception as e:
    print(f"初始化折扣碼時發生錯誤: {e}")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'db' in locals() and db.is_connected():
        db.close()



# 初始化資料庫連接
try:
    db = get_db_connection()
except Exception as e:
    print(f"無法連接到資料庫: {e}")
    db = None


# 資料庫連接檢查裝飾器
def check_db_connection(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        global db
        try:
            if db is None or not db.is_connected():
                db = get_db_connection()
        except Exception as e:
            print(f"資料庫連接錯誤: {e}")
            flash('系統暫時無法使用，請稍後再試', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('請先登入', 'danger')
            return redirect(url_for('login'))
            
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT role FROM users WHERE id = %s", (session['user_id'],))
        user = cursor.fetchone()
        
        if not user or user['role'] != 'admin':
            flash('沒有權限訪問此頁面', 'danger')
            return redirect(url_for('home'))
            
        return f(*args, **kwargs)
    return decorated_function

# 初始化 CSRF 保護
csrf = CSRFProtect(app)



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/products')
@check_db_connection
def products():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    return render_template('index.html', products=products)


@app.route('/login', methods=['GET', 'POST'])
@check_db_connection
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # 檢查是否有空欄位
        if not username or not password:
            flash('請填寫所有欄位', 'danger')
            return render_template('login.html')
        
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            flash('登入成功！', 'success')
            return redirect(url_for('home'))
        else:
            flash('帳號或密碼錯誤', 'danger')
            
    return render_template('login.html')



@app.route('/register', methods=['GET', 'POST'])
@check_db_connection
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        if not username or not password or not email:
            flash('請填寫所有欄位', 'danger')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('密碼長度必須至少6個字元', 'danger')
            return render_template('register.html')
        
        try:
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                flash('使用者名稱已被使用', 'danger')
                return render_template('register.html')
            
            hashed_password = generate_password_hash(password)
            cursor.execute("""
            INSERT INTO users (username, password, email, role) 
            VALUES (%s, %s, %s, 'user')
            """, (username, hashed_password, email))
            db.commit()
            
            flash('註冊成功！請登入', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            db.rollback()
            flash('操作失敗，請稍後再試', 'danger')
            print(f"Error in register: {str(e)}")
            return render_template('register.html')
            
    return render_template('register.html')

@app.route('/cart')
@check_db_connection
def cart():
    if 'cart' not in session:
        session['cart'] = []
    return render_template('cart.html')

@app.route('/remove_from_cart/<int:product_id>')
@check_db_connection
def remove_from_cart(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:    
        cursor = db.cursor()
        cursor.execute("""
        DELETE FROM cart 
        WHERE user_id = %s AND product_id = %s
        """, (session['user_id'], product_id))
        db.commit()
    except Exception as e:
        db.rollback()
        flash('刪除失敗，請稍後再試', 'danger')
        print(f"Error in remove_from_cart: {str(e)}")
    
    return redirect(url_for('cart'))

@app.route('/update_cart_quantity', methods=['POST'])
@check_db_connection
@csrf.exempt
def update_cart_quantity():
    try:
        data = request.get_json()
        index = data.get('index')
        quantity = int(data.get('quantity'))
        
        if 'cart' in session and 0 <= index < len(session['cart']):
            session['cart'][index]['quantity'] = quantity
            session.modified = True
            return jsonify({'success': True})
    except Exception as e:
        print(f"Error in update_cart_quantity: {str(e)}")
    return jsonify({'success': False})

@app.route('/remove_cart_item', methods=['POST'])
@check_db_connection
@csrf.exempt
def remove_cart_item():
    try:
        data = request.get_json()
        index = data.get('index')
        
        if 'cart' in session and 0 <= index < len(session['cart']):
            session['cart'].pop(index)
            session.modified = True
            return jsonify({'success': True})
    except Exception as e:
        print(f"Error in remove_cart_item: {str(e)}")
    return jsonify({'success': False})

@app.route('/add_to_cart_custom/<int:product_id>', methods=['POST'])
@check_db_connection
def add_to_cart_custom(product_id):
    if 'cart' not in session:
        session['cart'] = []
    
    cursor = db.cursor(dictionary=True)
    
    try:
        # 獲取所有必要的組件類別
        cursor.execute("SELECT id, name FROM component_categories")
        required_categories = cursor.fetchall()
        
        # 檢查是否所有必要的組件都已選擇
        missing_components = []
        for category in required_categories:
            component_key = f'component_{category["id"]}'
            if component_key not in request.form or not request.form[component_key]:
                missing_components.append(category["name"])
        
        # 如果有未選擇的組件，返回錯誤
        if missing_components:
            missing_items = '、'.join(missing_components)
            flash(f'請選擇以下必要組件：{missing_items}', 'danger')
            return redirect(url_for('customize_product', product_id=product_id))
        
        # 獲取基礎產品信息
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()
        total_price = float(product['price'])
        
        # 收集所有選擇的組件
        custom_components = {}
        for category in required_categories:
            component_id = request.form[f'component_{category["id"]}']
            
            # 獲取組件信息
            cursor.execute("SELECT name, price FROM components WHERE id = %s", (component_id,))
            component = cursor.fetchone()
            
            custom_components[category['name']] = component['name']
            total_price += float(component['price'])
        
        # 創建購物車項目
        cart_item = {
            'id': product_id,
            'name': product['name'],
            'price': total_price,
            'quantity': 1,
            'type': 'custom',
            'custom_components': custom_components
        }
        
        session['cart'].append(cart_item)
        session.modified = True
        
        flash('自定義商品已成功加入購物車！', 'success')
        
    except Exception as e:
        flash('添加商品時出現錯誤，請重試。', 'danger')
        print(f"Error: {str(e)}")
    
    return redirect(url_for('cart'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/checkout')
def checkout():
    if 'cart' not in session or not session['cart']:
        flash('購物車是空的', 'warning')
        return redirect(url_for('cart'))
    
    # 計算總價
    total_price = sum(item['price'] * item['quantity'] for item in session['cart'])
    
    # 設定運費（可以根據需求調整運費計算邏輯）
    shipping_fee = 100 if total_price < 3000 else 0
    
    return render_template('checkout.html', 
                         total_price=total_price,
                         shipping_fee=shipping_fee)

@app.route('/place_order', methods=['POST'])
@check_db_connection
def place_order():
    if 'cart' not in session or not session['cart']:
        flash('購物車是空的', 'warning')
        return redirect(url_for('cart'))
    
    try:
        cursor = db.cursor(dictionary=True)
        
        # 計算訂單金額
        total_amount = sum(item['price'] * item['quantity'] for item in session['cart'])
        shipping_fee = 100 if total_amount < 3000 else 0
        discount_amount = 0
        
        # 處理折扣碼
        discount_code = request.form.get('discount_code')
        if discount_code:
            cursor.execute("""
                SELECT * FROM discount_codes 
                WHERE code = %s 
                AND is_active = TRUE 
                AND start_date <= NOW() 
                AND end_date >= NOW()
                AND (usage_limit IS NULL OR used_count < usage_limit)
            """, (discount_code,))
            
            discount = cursor.fetchone()
            if discount and total_amount >= discount['min_purchase']:
                if discount['discount_type'] == 'percentage':
                    discount_amount = total_amount * (discount['discount_value'] / 100)
                else:
                    discount_amount = discount['discount_value']
                
                # 更新折扣碼使用次數
                cursor.execute("""
                    UPDATE discount_codes 
                    SET used_count = used_count + 1 
                    WHERE id = %s
                """, (discount['id'],))
        
        final_amount = total_amount + shipping_fee - discount_amount
        
        # 創建訂單
        cursor.execute("""
        INSERT INTO orders (
            user_id, 
            total_amount,
            shipping_fee,
            recipient_name,
            recipient_phone,
            recipient_email,
            shipping_address,
            note,
            payment_method
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            session.get('user_id'),
            final_amount,
            shipping_fee,
            request.form.get('name'),
            request.form.get('phone'),
            request.form.get('email'),
            request.form.get('address'),
            request.form.get('note'),
            request.form.get('payment')
        ))
        
        order_id = cursor.lastrowid
        
        # 保存訂單項目
        for item in session['cart']:
            # 插入訂單項目
            cursor.execute("""
            INSERT INTO order_items (
                order_id,
                product_id,
                quantity,
                price,
                is_custom
            ) VALUES (%s, %s, %s, %s, %s)
            """, (
                order_id,
                item['id'],
                item['quantity'],
                item['price'],
                item['type'] == 'custom'
            ))
            
            # 獲取插入的訂單項目 ID
            item_id = cursor.lastrowid
            
            # 如果是客製化商品，保存配置
            if item['type'] == 'custom' and 'custom_components' in item:
                for category, component in item['custom_components'].items():
                    cursor.execute("""
                    INSERT INTO order_configurations (
                        order_item_id,
                        category_name,
                        component_name
                    ) VALUES (%s, %s, %s)
                    """, (
                        item_id,  # 使用正確的訂單項目 ID
                        category,
                        component
                    ))
        
        # 如果使用了折扣碼，記錄使用情況
        if discount_code and discount:
            cursor.execute("""
                INSERT INTO discount_usage (
                    discount_code_id, order_id, user_id
                ) VALUES (%s, %s, %s)
            """, (discount['id'], order_id, session['user_id']))
        
        db.commit()
        
        # 清空購物車
        session.pop('cart', None)
        
        flash('訂單已成功建立！', 'success')
        return redirect(url_for('order_complete', order_id=order_id))
        
    except Exception as e:
        db.rollback()
        flash('訂單建立失敗，請重試', 'danger')
        print(f"Error: {str(e)}")
        return redirect(url_for('checkout'))

@app.route('/customize/<product_id>')
@check_db_connection
@csrf.exempt
def customize_product(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    try:
        cursor = db.cursor(dictionary=True)
        
        # 獲取基礎產品信息
        cursor.execute(f"SELECT * FROM products WHERE id = {product_id}")
        product = cursor.fetchone()
        # while True:
        #     row = cursor.fetchone()
        #     if row is None:
        #         break

        if not product:
            return redirect(url_for('products'))
        
        # 獲取所有配件類別和選項
        cursor.execute("SELECT * FROM component_categories")
        categories = cursor.fetchall()
        
        components = {}
        for category in categories:
            cursor.execute("""
            SELECT c.*, pc.is_default 
            FROM components c 
            LEFT JOIN product_configurations pc 
            ON c.id = pc.component_id AND pc.base_product_id = %s
            WHERE c.category_id = %s
            """, (product_id, category['id']))
            components[category['id']] = cursor.fetchall()
        
        return render_template(
            'customize.html',
            product=product,
            categories=categories,
            components=components
        )

    except Exception as e:
        print(f"Error in customize_product: {str(e)}")
        return redirect(url_for('products'))
    

@app.route('/orders')
@check_db_connection
def orders():
    if 'user_id' not in session:
        flash('請先登入', 'danger')
        return redirect(url_for('login'))
    
    cursor = db.cursor(dictionary=True)
    
    # 獲取用戶的所有訂單
    cursor.execute("""
        SELECT orders.*, 
               COUNT(order_items.id) as item_count,
               SUM(order_items.quantity) as total_items
        FROM orders 
        LEFT JOIN order_items ON orders.id = order_items.order_id
        WHERE orders.user_id = %s 
        GROUP BY orders.id
        ORDER BY orders.created_at DESC
    """, (session['user_id'],))
    
    orders = cursor.fetchall()
    return render_template('orders.html', orders=orders)

@app.route('/order/<int:order_id>')
@check_db_connection
def order_detail(order_id):
    if 'user_id' not in session:
        flash('請先登入', 'danger')
        return redirect(url_for('login'))
    
    cursor = db.cursor(dictionary=True)
    
    # 獲取訂單基本信息
    cursor.execute("""
        SELECT * FROM orders 
        WHERE id = %s AND user_id = %s
    """, (order_id, session['user_id']))
    
    order = cursor.fetchone()
    if not order:
        flash('找不到此訂單', 'danger')
        return redirect(url_for('orders'))
    
    # 獲取訂單項目
    cursor.execute("""
        SELECT order_items.*, products.name as product_name 
        FROM order_items 
        JOIN products ON order_items.product_id = products.id
        WHERE order_items.order_id = %s
    """, (order_id,))
    
    items = cursor.fetchall()
    
    # 獲取客製化配置
    for item in items:
        if item['is_custom']:
            cursor.execute("""
                SELECT category_name, component_name 
                FROM order_configurations 
                WHERE order_item_id = %s
            """, (item['id'],))
            item['configurations'] = cursor.fetchall()
    
    return render_template('order_detail.html', order=order, items=items)

@app.route('/order_complete/<int:order_id>')
@check_db_connection
def order_complete(order_id):
    if 'user_id' not in session:
        flash('請先登入', 'danger')
        return redirect(url_for('login'))
    
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM orders 
        WHERE id = %s AND user_id = %s
    """, (order_id, session['user_id']))
    
    order = cursor.fetchone()
    if not order:
        flash('找不到此訂單', 'danger')
        return redirect(url_for('orders'))
    
    return render_template('order_complete.html', order=order)

@app.route('/admin/discount_codes')
@admin_required
def admin_discount_codes():
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT dc.*, u.username as created_by_name 
        FROM discount_codes dc 
        LEFT JOIN users u ON dc.created_by = u.id 
        ORDER BY dc.created_at DESC
    """)
    discount_codes = cursor.fetchall()
    return render_template('admin/discount_codes.html', discount_codes=discount_codes)

@app.route('/admin/discount_codes/create', methods=['GET', 'POST'])
@admin_required
def create_discount_code():
    if request.method == 'POST':
        try:
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO discount_codes (
                    code, discount_type, discount_value, min_purchase,
                    start_date, end_date, usage_limit, created_by
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                request.form['code'],
                request.form['discount_type'],
                float(request.form['discount_value']),
                float(request.form['min_purchase']),
                request.form['start_date'],
                request.form['end_date'],
                int(request.form['usage_limit']) if request.form['usage_limit'] else None,
                session['user_id']
            ))
            db.commit()
            flash('折扣碼創建成功', 'success')
            return redirect(url_for('admin_discount_codes'))
        except Exception as e:
            db.rollback()
            flash('創建失敗：' + str(e), 'danger')
    
    return render_template('admin/create_discount_code.html')

@app.route('/validate_discount', methods=['POST'])
@csrf.exempt
def validate_discount():
    try:
        data = request.get_json()
        code = data.get('discount_code')
        total_amount = (data.get('total_amount', 0))
        
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM discount_codes 
            WHERE code = %s 
            AND is_active = TRUE 
            AND start_date <= NOW() 
            AND end_date >= NOW()
            AND (usage_limit IS NULL OR used_count < usage_limit)
        """, (code,))
        
        discount = cursor.fetchone()
        
        if not discount:
            return jsonify({'valid': False, 'message': '無效的折扣碼'})
        
        if total_amount < discount['min_purchase']:
            return jsonify({
                'valid': False, 
                'message': f'訂單金額需要達到 ${discount["min_purchase"]} 才能使用此折扣碼'
            })
        
        discount_amount = 0
        if discount['discount_type'] == 'percentage':
            discount_amount = total_amount * (discount['discount_value'] / 100)
        else:
            discount_amount = discount['discount_value']
        
        return jsonify({
            'valid': True,
            'discount_amount': discount_amount,
            'message': '折扣碼有效'
        })
    except Exception as e:
        print(f"Error in validate_discount: {str(e)}")
        return jsonify({'valid': False, 'message': '折扣碼驗證失敗，請稍後再試'})

@app.route('/admin/orders')
@admin_required
def admin_orders():
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT orders.*, 
               users.username,
               COUNT(order_items.id) as item_count,
               SUM(order_items.quantity) as total_items
        FROM orders 
        LEFT JOIN users ON orders.user_id = users.id
        LEFT JOIN order_items ON orders.id = order_items.order_id
        GROUP BY orders.id
        ORDER BY orders.created_at DESC
    """)
    orders = cursor.fetchall()
    return render_template('admin/orders.html', orders=orders)

@app.route('/admin/order/<int:order_id>')
@admin_required
def admin_order_detail(order_id):
    cursor = db.cursor(dictionary=True)
    
    # 獲取訂單基本信息
    cursor.execute("""
        SELECT orders.*, users.username
        FROM orders 
        LEFT JOIN users ON orders.user_id = users.id
        WHERE orders.id = %s
    """, (order_id,))
    
    order = cursor.fetchone()
    if not order:
        flash('找不到此訂單', 'danger')
        return redirect(url_for('admin_orders'))
    
    # 獲取訂單項目
    cursor.execute("""
        SELECT order_items.*, products.name as product_name 
        FROM order_items 
        JOIN products ON order_items.product_id = products.id
        WHERE order_items.order_id = %s
    """, (order_id,))
    
    items = cursor.fetchall()
    
    # 獲取客製化配置
    for item in items:
        if item['is_custom']:
            cursor.execute("""
                SELECT category_name, component_name 
                FROM order_configurations 
                WHERE order_item_id = %s
            """, (item['id'],))
            item['configurations'] = cursor.fetchall()
    
    return render_template('admin/order_detail.html', order=order, items=items)

@app.route('/admin/order/update_status', methods=['POST'])
@admin_required
def update_order_status():
    try:
        order_id = request.form.get('order_id')
        new_status = request.form.get('status')
        admin_note = request.form.get('admin_note')
        
        cursor = db.cursor()
        cursor.execute("""
            UPDATE orders 
            SET status = %s, admin_note = %s
            WHERE id = %s
        """, (new_status, admin_note, order_id))
        
        db.commit()
        flash('訂單狀態已更新', 'success')
        
    except Exception as e:
        db.rollback()
        flash('更新失敗：' + str(e), 'danger')
        
    return redirect(url_for('admin_order_detail', order_id=order_id))

if __name__ == '__main__':
    app.run(debug=True)