from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = 'secret123'

products = [
    {"id": 1, "name": "Wireless Headphones", "price": 79.99, "category": "Electronics",
     "description": "High-quality wireless headphones with noise cancellation and 30hr battery life."},
    {"id": 2, "name": "Leather Wallet", "price": 34.99, "category": "Accessories",
     "description": "Slim genuine leather wallet with RFID blocking protection."},
    {"id": 3, "name": "Running Shoes", "price": 119.99, "category": "Footwear",
     "description": "Lightweight running shoes built for all terrain and comfort."},
    {"id": 4, "name": "Coffee Maker", "price": 49.99, "category": "Kitchen",
     "description": "Brew the perfect cup every morning with programmable settings."},
    {"id": 5, "name": "Yoga Mat", "price": 29.99, "category": "Sports",
     "description": "Non-slip eco-friendly yoga mat with alignment guide lines."},
    {"id": 6, "name": "Sunglasses", "price": 59.99, "category": "Accessories",
     "description": "UV400 polarized sunglasses for stylish all-day comfort."},
]

def get_product_by_id(product_id):
    for p in products:
        if p["id"] == product_id:
            return p
    return None

@app.route('/')
def home():
    cart_count = sum(session.get('cart', {}).values())
    return render_template('index.html', products=products, cart_count=cart_count)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = {}
    cart = session['cart']
    key = str(product_id)
    cart[key] = cart.get(key, 0) + 1
    session['cart'] = cart
    return redirect(url_for('home'))

@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    cart_items = []
    total = 0
    for product_id, qty in cart.items():
        product = get_product_by_id(int(product_id))
        if product:
            subtotal = product['price'] * qty
            cart_items.append({**product, 'qty': qty, 'subtotal': subtotal})
            total += subtotal
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    key = str(product_id)
    if key in cart:
        del cart[key]
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session['cart'] = {}
    return redirect(url_for('cart'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
