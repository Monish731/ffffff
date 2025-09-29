import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
# IMPORTANT: Set a secret key for session management and flashing messages
app.secret_key = 'your_super_secret_key_change_me'

# --- Database Setup and Utilities ---

def get_db_connection():
    # Connect to the SQLite database
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn

def init_db():
    # Initialize the database and create the 'students' table if it doesn't exist
    conn = get_db_connection()
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                course TEXT NOT NULL,
                year INTEGER NOT NULL
            );
        ''')
    conn.close()

# Initialize the database when the application starts
init_db()

# --- Routes (Controller) ---

@app.route('/')
def index():
    """Home Page route."""
    return render_template('index.html')

@app.route('/register')
def register():
    """Registration Form page route."""
    return render_template('register.html')

@app.route('/submit', methods=['POST'])
def submit():
    """Handles form submission and inserts data into the database."""
    name = request.form['name']
    email = request.form['email']
    course = request.form['course']
    year = request.form['year']

    try:
        conn = get_db_connection()
        with conn:
            conn.execute(
                "INSERT INTO students (name, email, course, year) VALUES (?, ?, ?, ?)",
                (name, email, course, year)
            )
        flash(f"Student '{name}' registered successfully!", 'success')
    except sqlite3.IntegrityError:
        # Email is defined as UNIQUE in the table schema
        flash("Error: This email address is already registered.", 'danger')
    except Exception as e:
        flash(f"An unexpected error occurred: {e}", 'danger')
    finally:
        if 'conn' in locals() and conn:
            conn.close()
    
    # Redirect back to the registration page after submission
    return redirect(url_for('register'))

@app.route('/students')
def students():
    """Displays a list of all registered students."""
    conn = get_db_connection()
    # Fetch all students. .fetchall() returns a list of Row objects.
    students_data = conn.execute("SELECT * FROM students ORDER BY id DESC").fetchall()
    conn.close()

    # Convert to a list of tuples/lists for cleaner template rendering (matching your original structure)
    students_list = [tuple(s) for s in students_data]

    return render_template('students.html', students=students_list)

@app.route('/delete/<int:student_id>')
def delete(student_id):
    """Deletes a student record by ID."""
    conn = get_db_connection()
    with conn:
        conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.close()
    
    flash("Student record deleted successfully!", 'warning')
    # Redirect back to the students list page
    return redirect(url_for('students'))

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)