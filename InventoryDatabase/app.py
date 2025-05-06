from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response
#from crud import showInventory, getItemByID, itemIDExists, busyHoursAnalytics, popularItemsAnalytics, addNewItem, removeItem, updateItem, buyItem, staffIDExists, addNewStaff, getItemOrigins, getItemCategories, getStaffByCredentials
from crud import *
import plotly.io as pio
from datetime import datetime
import os

import random

app = Flask(__name__)
app.secret_key = "your-secret-key"

@app.route('/')
def home():
    return render_template('LandingPage.html')

@app.route('/login', methods=['GET', 'POST'])
def staff_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        staff_id = getStaffByCredentials(username, password)
        if staff_id:
            session['staff_logged_in'] = True
            response = make_response(redirect('/staff'))
            response.set_cookie('staff_id', staff_id)
            return response
        else:
            return render_template('StaffLogin.html', error="Invalid username or password.")
    
    return render_template('StaffLogin.html')

@app.route('/staff')
def staff_view():
    if not session.get('staff_logged_in'):
        return redirect('/login')
    return render_template('StaffView.html')

@app.route('/logout')
def logout():
    session.pop('staff_logged_in', None)  # Log the user out
    return redirect('/student')  # Redirect to StudentView

@app.route('/student')
def student_view():
    return render_template('StudentView.html')

@app.route('/add_item')
def add_item_form():
    if not session.get('staff_logged_in'):
        return redirect('/login')
    return render_template('AddNewItem.html')


@app.route('/add_item', methods=['POST'])
def add_item():
    name = request.form.get('productName')
    item_id = request.form.get('itemID')
    price = request.form.get('price')
    weight = request.form.get('weight')
    description = request.form.get('description')
    available_quantity = int(request.form.get('availableQuantity') or 0)
    quantity_limit = int(request.form.get('quantityLimit') or 1)
    
    # Handle origin checkboxes
    origins = []
    for origin in ['Patel Brothers', 'MD Food Bank', 'Donated']:
        if origin in request.form:
            origins.append(origin)
    if 'otherOriginCheckbox' in request.form and request.form.get('otherOriginInput'):
        origins.append(request.form.get('otherOriginInput'))


    # Handle categories
    categories = request.form.getlist('category')  # if checkboxes have name="category"

    # Handle image upload
    image_file = request.files.get('logoImage')
    image_path = 'static/Logos/default.png'  # fallback
    if image_file and image_file.filename:
        image_path = os.path.join('static', 'Logos', item_id + '_' + image_file.filename)
        image_file.save(image_path)

    # Call database insert function
    #print(f"item id length {len(item_id)}")
    result = addNewItem(item_id, name, weight, available_quantity, price, description, quantity_limit, origins, categories, image_path)
    print(result)
    return redirect(url_for('staff_view'))


@app.route('/edit')
def edit_page():
    item_id = request.args.get('id')
    item = getItemByID(item_id)
    if not item:
        return "Item not found", 404

    origins = getItemOrigins(item_id)        # Create this helper to get list of origins
    categories = getItemCategories(item_id)  # Create this helper to get list of categories

    all_categories = []
    all_origins = ['Patel Brothers', 'MD Food Bank', 'Donated']

    return render_template(
        "EditExistingItem.html",
        item=item,
        selected_origins=origins,
        selected_categories=categories,
        all_categories=all_categories,
        all_origins=all_origins
    )


@app.route('/edit_item', methods=['POST'])
def edit_item():
    print("calling edit item")
    data = request.form

    staff_id = request.cookies.get('staff_id')  # or however you track login
    item_id = data['itemID']
    item_name = data['productName']
    weight = float(data.get('weight', 0))
    price = float(data.get('price', 0))
    description = data['description']
    available_quantity = int(data['availableQuantity'])
    quantity_limit = int(data['quantityLimit'])
    origins = data.getlist('origin')
    categories = data.getlist('category')
    image_str = data.get('image_str', '')  # this could be base64 or filename

    update_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    result = updateItem(staff_id, item_id, update_datetime, item_name, weight,
                        available_quantity, price, description, quantity_limit,
                        origins, categories, image_str)
    
    print(result)
    print(f"staff id {staff_id}")

    return render_template("StaffView.html", message=result)

@app.route('/checkout')
def checkout():
    return render_template('Checkout.html')

@app.route('/view')
def view_item():
    item_id = request.args.get('id')
    if not item_id:
        return "Item ID is required", 400

    item = getItemByID(item_id)
    if not item:
        return f"Item with ID {item_id} not found.", 404

    return render_template('ViewItem.html', item=item)

@app.route('/generate_unique_id')
def generate_unique_id():
    while True:
        new_id = random.randint(1000000000, 9999999999)
        if not itemIDExists(new_id):
            return {'item_id': new_id}

@app.route('/api/items')
def get_items():
    inventory = showInventory()
    formatted = [
        {
            'id': int(item_id),
            'name': data["Item name"],
            'image': 'static/Logos/default.png',
            'available_quantity': data.get("Quantity", 0),
            'quantity_limit': data.get("Quantity limit", 1),
            'categories': []
        }
        for item_id, data in inventory.items()
    ]
    return jsonify(formatted)

@app.route('/api/busy_hours')
def api_busy_hours():
    fig = busyHoursAnalytics()
    html = pio.to_html(fig, full_html=False)
    return jsonify({'plot_html': html})

@app.route('/api/popular_items')
def api_popular_items():
    fig = popularItemsAnalytics()
    html = pio.to_html(fig, full_html=False)
    return jsonify({'plot_html': html})

@app.route('/analytics')
def analytics_page():
    return render_template('AnalyticsView.html')

@app.route('/api/remove_item', methods=['POST'])
def remove_item():
    data = request.get_json()
    item_id = data.get('item_id')

    if not item_id:
        return jsonify({'success': False, 'message': 'Missing item ID'}), 400

    result = removeItem(item_id)
    success = result.startswith("✅")

    return jsonify({'success': success, 'message': result})

@app.route('/api/item/<item_id>')
def get_item_api(item_id):
    from crud import getItemByID
    item = getItemByID(item_id)
    if item:
        return jsonify(item)
    else:
        return jsonify({"error": "Item not found"}), 404
    
@app.route("/api/checkout", methods=["POST"])
def handle_checkout():
    data = request.get_json()

    if not data or "items" not in data:
        return jsonify({"error": "Invalid data"}), 400

    results = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for item in data["items"]:
        item_id = item.get("item_id")
        quantity = item.get("quantity")

        if not item_id or not isinstance(quantity, int):
            results.append({"item_id": item_id, "result": "Invalid input"})
            continue

        result = buyItem(item_id, now, quantity)
        results.append({"item_id": item_id, "result": result})

    return jsonify(results)

@app.route('/register', methods=['GET', 'POST'])
def staff_register():
    if request.method == 'POST':
        staff_id = request.form['staff_id']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        if password != confirm_password:
            return render_template('StaffRegister.html', error="❌ Passwords do not match.")

        if staffIDExists(staff_id):
            return render_template('StaffRegister.html', error=f"⚠️ Staff ID '{staff_id}' already exists.")

        result = addNewStaff(staff_id, first_name, last_name, username, password)

        if result.startswith("✅"):
            return redirect(url_for('staff_login'))
        else:
            return render_template('StaffRegister.html', error=result)

    return render_template('StaffRegister.html')

if __name__ == '__main__':
    app.run(debug=True)