from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from crud import showInventory, busyHoursAnalytics, popularItemsAnalytics
import plotly.io as pio

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
    return render_template('EditExistingItem.html')

@app.route('/checkout')
def checkout():
    return render_template('Checkout.html')

@app.route('/view')
def view_item():
    return render_template('ViewItem.html')


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

if __name__ == '__main__':
    app.run(debug=True)
