from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from crud import showInventory, getItemByID, itemIDExists, addNewItem
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

        # You can replace this with a real DB check later
        if username == 'Staff2' and password == '1234':
            session['staff_logged_in'] = True
            return redirect('/staff')
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

    origin_str = ', '.join(origins)

    # Handle categories
    categories = request.form.getlist('category')  # if checkboxes have name="category"
    categories_str = ', '.join(categories)

    # Handle image upload
    image_file = request.files.get('logoInput')
    image_path = 'static/Logos/default.png'  # fallback
    if image_file and image_file.filename:
        image_path = os.path.join('static', 'Logos', item_id + '_' + image_file.filename)
        image_file.save(image_path)

    # Call database insert function
    result = addNewItem(item_id, name, weight, available_quantity, price, description, quantity_limit, origin_str, categories_str, image_path)
    print(result)
    return redirect(url_for('staff_view'))


@app.route('/edit')
def edit_item():
    item_id = request.args.get('id')
    if not item_id:
        return "Item ID is required", 400

    item = getItemByID(item_id)
    if not item:
        return f"Item with ID {item_id} not found.", 404

    return render_template('EditExistingItem.html', item=item)

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
            'categories': []
        }
        for item_id, data in inventory.items()
    ]
    return jsonify(formatted)

if __name__ == '__main__':
    app.run(debug=True)
