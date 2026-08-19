from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models import Task, User
from app import db
from datetime import datetime, date

tasks_bp = Blueprint('tasks', __name__, template_folder='../templates')

@tasks_bp.route('/')
@login_required
def tasks():
    # Get all tasks for current user, ordered by priority and created date
    user_tasks = Task.query.filter_by(user_id=current_user.id).order_by(
        Task.completed.asc(),
        Task.priority.desc(),
        Task.created_at.desc()
    ).all()
    
    return render_template('tasks.html', tasks=user_tasks, now=date.today())

@tasks_bp.route('/add', methods=['POST'])
@login_required
def add_task():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        priority = request.form.get('priority', 'medium')
        due_date_str = request.form.get('due_date', '')
        
        if not title:
            flash('Task title is required.', 'error')
            return redirect(url_for('tasks.tasks'))
        
        if len(title) > 200:
            flash('Task title is too long (max 200 characters).', 'error')
            return redirect(url_for('tasks.tasks'))
        
        # Parse due date
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format.', 'error')
                return redirect(url_for('tasks.tasks'))
        
        # Create task
        try:
            new_task = Task(
                title=title,
                priority=priority,
                due_date=due_date,
                user_id=current_user.id
            )
            db.session.add(new_task)
            db.session.commit()
            
            flash('Task added successfully!', 'success')
            return redirect(url_for('tasks.tasks'))
        
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while adding the task.', 'error')
            return redirect(url_for('tasks.tasks'))

@tasks_bp.route('/edit/<int:task_id>', methods=['POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    # Check ownership
    if task.user_id != current_user.id:
        flash('You do not have permission to edit this task.', 'error')
        return redirect(url_for('tasks.tasks'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        priority = request.form.get('priority', 'medium')
        due_date_str = request.form.get('due_date', '')
        
        if not title:
            flash('Task title is required.', 'error')
            return redirect(url_for('tasks.tasks'))
        
        # Parse due date
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format.', 'error')
                return redirect(url_for('tasks.tasks'))
        
        try:
            task.title = title
            task.priority = priority
            task.due_date = due_date
            task.updated_at = datetime.utcnow()
            db.session.commit()
            
            flash('Task updated successfully!', 'success')
            return redirect(url_for('tasks.tasks'))
        
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the task.', 'error')
            return redirect(url_for('tasks.tasks'))

@tasks_bp.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    # Check ownership
    if task.user_id != current_user.id:
        flash('You do not have permission to delete this task.', 'error')
        return redirect(url_for('tasks.tasks'))
    
    try:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the task.', 'error')
    
    return redirect(url_for('tasks.tasks'))

@tasks_bp.route('/toggle/<int:task_id>', methods=['POST'])
@login_required
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    # Check ownership
    if task.user_id != current_user.id:
        return jsonify({'error': 'Permission denied'}), 403
    
    try:
        task.completed = not task.completed
        task.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({'success': True, 'completed': task.completed})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update task'}), 500

@tasks_bp.route('/complete/<int:task_id>', methods=['POST'])
@login_required
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    if task.user_id != current_user.id:
        flash('You do not have permission to modify this task.', 'error')
        return redirect(url_for('tasks.tasks'))
    
    try:
        task.completed = True
        task.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Task marked as complete!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred.', 'error')
    
    return redirect(url_for('tasks.tasks'))

@tasks_bp.route('/incomplete/<int:task_id>', methods=['POST'])
@login_required
def incomplete_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    if task.user_id != current_user.id:
        flash('You do not have permission to modify this task.', 'error')
        return redirect(url_for('tasks.tasks'))
    
    try:
        task.completed = False
        task.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Task marked as incomplete!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred.', 'error')
    
    return redirect(url_for('tasks.tasks'))

# API endpoint for getting tasks (optional, for AJAX)
@tasks_bp.route('/api/tasks')
@login_required
def get_tasks_api():
    user_tasks = Task.query.filter_by(user_id=current_user.id).all()
    return jsonify([task.to_dict() for task in user_tasks])