from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from datetime import datetime
import random
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB limit

# Mock user database
USERS = {
    'admin': 'password123',
    'user': 'password123'
}

# Mock data for targeting
INTERESTS = [
    'Technology', 'Sports', 'Fashion', 'Travel', 'Food',
    'Health', 'Finance', 'Education', 'Entertainment', 'Automotive'
]

LOCATIONS = [
    'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
    'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose'
]

# In-memory "database" for campaigns
campaigns = []

def generate_ai_ad_copy(product_name):
    """Simulate AI-generated ad copy"""
    templates = [
        f"Discover amazing {product_name} that will change your life!",
        f"Limited time offer on premium {product_name} - don't miss out!",
        f"Everyone's talking about {product_name} - see why today!",
        f"Upgrade your experience with our {product_name} collection.",
        f"{product_name.capitalize()} - because you deserve the best!"
    ]
    return random.choice(templates)

def simulate_analytics():
    """Generate fake analytics data"""
    return {
        'impressions': random.randint(1000, 10000),
        'clicks': random.randint(50, 500),
        'ctr': round(random.uniform(0.5, 5.0), 2),
        'spend': round(random.uniform(50, 500), 2)
    }

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in USERS and USERS[username] == password:
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/campaigns')
def list_campaigns():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('campaigns.html', campaigns=campaigns)

@app.route('/create', methods=['GET', 'POST'])
def create_campaign():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        campaign_name = request.form.get('campaign_name')
        banner_type = request.form.get('banner_type')
        banner_url = request.form.get('banner_url')
        banner_file = request.files.get('banner_file')
        age_min = request.form.get('age_min')
        age_max = request.form.get('age_max')
        locations = request.form.getlist('locations')
        interests = request.form.getlist('interests')
        
        # Handle banner upload
        banner_path = None
        if banner_type == 'url' and banner_url:
            banner_path = banner_url
        elif banner_type == 'file' and banner_file:
            filename = secure_filename(banner_file.filename)
            banner_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            banner_file.save(banner_path)
            banner_path = url_for('static', filename=f'uploads/{filename}')
        
        if not banner_path:
            flash('Please provide a valid banner', 'error')
            return redirect(url_for('create_campaign'))
        
        # Create campaign
        campaign = {
            'id': len(campaigns) + 1,
            'name': campaign_name,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'status': 'Active',
            'banner': banner_path,
            'targeting': {
                'age_range': f"{age_min}-{age_max}",
                'locations': locations,
                'interests': interests
            },
            'analytics': simulate_analytics()
        }
        
        campaigns.append(campaign)
        flash('Campaign created successfully!', 'success')
        return redirect(url_for('list_campaigns'))
    
    return render_template('create.html', interests=INTERESTS, locations=LOCATIONS)

@app.route('/generate-ad-copy', methods=['POST'])
def generate_ad_copy():
    product_name = request.form.get('product_name')
    if not product_name:
        return {'error': 'Product name is required'}, 400
    return {'ad_copy': generate_ai_ad_copy(product_name)}

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)