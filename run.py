from app import create_app, db
from app.models import User, Task
from flask import redirect, url_for
from flask_login import current_user
import os

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Task': Task
    }

# --- THIS IS THE FIX ---
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('tasks.tasks'))
    return redirect(url_for('auth.login'))
# -----------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        if not User.query.first():
            print("No users found. Creating test user...")
            test_user = User(username='testuser', email='test@example.com')
            test_user.set_password('password123')
            db.session.add(test_user)
            db.session.commit()
            print("Test user created: username='testuser', password='password123'")
    
    debug_mode = os.environ.get('FLASK_ENV', 'development') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)