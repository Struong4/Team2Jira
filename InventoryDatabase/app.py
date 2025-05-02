from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from crud import showInventory, getItemByID, itemIDExists
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

@app.route('/add')
def add_item():
    return render_template('AddNewItem.html')

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
