# Flask Todo App

This is a Flask-based Todo application with user authentication, task management, and PostgreSQL database integration.

## Features

- User Authentication (Signup, Login, Logout)
- Create, Update, and Delete Todos
- Mark Todos as Complete
- User Profile Management
- Password Change Functionality
- PostgreSQL Database Integration
- Secure Cookie Handling for Authentication

## Installation

1. **Clone the Repository**
   ```sh
   git clone https://github.com/yourusername/flask-todo-app.git
   cd flask-todo-app
   ```

2. **Create a Virtual Environment**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   Create a `.env` file in the root directory and add:
   ```env
   DATABASE_URL=your_postgresql_database_url
   SECRET_KEY=your_secret_key
   FLASK_APP=app.py
   FLASK_ENV=development  # Change to 'production' in live deployment
   DEBUG_MODE=true  # Set to 'false' in production
   ```

5. **Run Database Migrations**
   ```sh
   flask db upgrade
   ```

6. **Run the Application**
   ```sh
   python app.py
   ```

## Usage

- Visit `http://127.0.0.1:2300/` in your browser.
- Sign up or log in to manage your todos.

## Tech Stack

- **Backend:** Flask
- **Database:** PostgreSQL
- **Migrations:** Flask-Migrate

## License

This project is licensed under the MIT License.

