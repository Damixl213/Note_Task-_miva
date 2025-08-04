# Main application routes - notes, tasks, dashboard, chatbot
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .model import Note, Task
from . import db
import google.generativeai as genai
import os
from dotenv import load_dotenv  # Fix this import

# Load environment variables
load_dotenv()

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # Main dashboard - create notes and view all content
    if request.method == 'POST':
        # Create new note
        subject = request.form.get('subject')
        note = request.form.get('note')
        
        # Validate input
        if len(subject) < 1:
            flash('Subject is required!', category='error')
        elif len(note) < 1:
            flash('Note content is too short!', category='error')
        else:
            # Save note to database
            new_note = Note(subject=subject, data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    
    # Get user's notes and tasks
    notes = Note.query.filter_by(user_id=current_user.id).all()
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", user=current_user, notes=notes, tasks=tasks)

@views.route('/download-note/<int:id>')
@login_required
def download_note(id):
    # Download note as text file
    note = Note.query.get_or_404(id)
    
    # Security check - user owns this note
    if note.user_id != current_user.id:
        flash('You do not have permission to download this note.', category='error')
        return redirect(url_for('views.home'))
    
    from flask import make_response
    
    # Create file content
    content = f"Subject: {note.subject}\n"
    content += f"Date: {note.date.strftime('%Y-%m-%d %H:%M')}\n"
    content += f"Author: {current_user.Name}\n\n"
    content += f"Content:\n{note.data}"
    
    # Return as downloadable file
    response = make_response(content)
    response.headers['Content-Type'] = 'text/plain'
    response.headers['Content-Disposition'] = f'attachment; filename="{note.subject}.docx"'
    return response

@views.route('/delete-note/<int:id>', methods=['POST'])
@login_required
def delete_note(id):
    # Delete note with ownership check
    note = Note.query.get_or_404(id)
    if note.user_id != current_user.id:
        flash('You do not have permission to delete this note.', category='error')
        return redirect(url_for('views.home'))
    
    db.session.delete(note)
    db.session.commit()
    flash('Note deleted!', category='error')
    return redirect(url_for('views.home'))
  
@views.route('/edit-note/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_note(id):
    # Edit existing note
    note = Note.query.get_or_404(id)
    
    # Security check
    if note.user_id != current_user.id:
        flash('You do not have permission to edit this note.', category='error')
        return redirect(url_for('views.home'))
    
    if request.method == 'POST':
        # Update note content
        new_data = request.form.get('note')
        if len(new_data) < 1:
            flash('Note is too short!', category='error')
        else:
            note.data = new_data
            db.session.commit()
            flash('Note updated!', category='success')
            return redirect(url_for('views.home'))
    
    return render_template('note.html', note=note, user=current_user)

@views.route('/chat', methods=['POST'])
@login_required
def chat():
    # AI chatbot using Google Gemini
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    # Get API key from environment variable
    api_key = os.getenv("GEMINI_API_KEY")
    
    # Check if API key is available
    if not api_key:
        return jsonify({'error': 'API key not configured. Please check your .env file.'}), 500
    
    try:
        # Configure Gemini with environment variable
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(user_message)
        answer = response.text
        return jsonify({'answer': answer})
    except Exception as e:
        print(f"Gemini API error: {e}")
        return jsonify({'error': 'Sorry, the AI assistant is temporarily unavailable.'}), 500
    
@views.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    # Task management
    if request.method == 'POST':
        # Create new task
        description = request.form.get('description')
        if not description or len(description) < 1:
            flash('Task description is too short!', category='error')
        else:
            new_task = Task(description=description, user_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()
            flash('Task added!', category='success')
    
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", user=current_user, tasks=tasks)

@views.route('/toggle-task/<int:id>', methods=['POST'])
@login_required
def toggle_task(id):
    # Mark task as complete/incomplete
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        flash('You do not have permission to update this task.', category='error')
        return redirect(url_for('views.tasks'))
    
    task.completed = not task.completed  # Toggle status
    db.session.commit()
    return redirect(url_for('views.tasks'))

@views.route('/delete-task/<int:id>', methods=['POST'])
@login_required
def delete_task(id):
    # Delete task with ownership check
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        flash('You do not have permission to delete this task.', category='error')
        return redirect(url_for('views.tasks'))
    
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted!', category='success')
    return redirect(url_for('views.tasks'))  

@views.route('/dashboard')
@login_required
def dashboard():
    # Read-only dashboard view
    notes = Note.query.filter_by(user_id=current_user.id).all()
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", user=current_user, notes=notes, tasks=tasks)