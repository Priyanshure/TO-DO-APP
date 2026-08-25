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

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('tasks.tasks'))
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
        
        # Check if database is empty and create a test user
        if not User.query.first():
            print("No users found. Creating test user...")
            test_user = User(
                username='testuser',
                email='test@example.com'
            )
            test_user.set_password('password123')
            db.session.add(test_user)
            db.session.commit()
            print("Test user created: username='testuser', password='password123'")
    
    # Render provides a PORT environment variable. Use it, or default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)