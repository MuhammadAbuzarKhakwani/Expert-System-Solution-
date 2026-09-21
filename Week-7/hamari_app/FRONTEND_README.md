# Hamari Quiz App - Frontend & Backend

A modern Django REST API with a fully-featured HTML/CSS/JavaScript frontend for creating and managing quizzes.

## Features

✅ **User Authentication**
- Register new users
- Login with token authentication
- Session-based authentication
- Secure password handling

✅ **Quiz Management**
- Create quizzes with title, description, and category
- View all your quizzes
- Edit quiz details
- Delete quizzes (only by creator)
- Users only see their own quizzes

✅ **Quiz Content**
- Add questions to quizzes
- Add multiple choice options
- Mark correct answers
- View questions with options in detail view

✅ **Responsive UI**
- Modern, gradient-based design
- Mobile-friendly layout
- Real-time feedback messages
- Smooth transitions and animations

## Installation

### 1. Install Dependencies

```bash
cd Week-7/hamari_app
pip install django djangorestframework django-cors-headers
```

### 2. Run Migrations

```bash
python manage.py migrate
```

### 3. Create Admin User (Optional)

```bash
python manage.py createsuperuser
```

### 4. Start Development Server

```bash
python manage.py runserver
```

The app will be available at: `http://localhost:8000`

## API Endpoints

### Authentication

- **Register**: `POST /api/auth/register/`
  ```json
  {
    "username": "your_username",
    "email": "your_email@example.com",
    "password": "your_password",
    "password2": "your_password",
    "first_name": "Optional",
    "last_name": "Optional"
  }
  ```

- **Login**: `POST /api/auth/token/`
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```
  Returns: `{"token": "your_auth_token"}`

### Quizzes

- **List/Create Quizzes**: `GET/POST /api/quizzes/`
  - Requires: `Authorization: Token <token>`
  - Only shows user's own quizzes

- **Get/Update/Delete Quiz**: `GET/PUT/DELETE /api/quizzes/{id}/`
  - Only creators can edit/delete

### Questions

- **List/Create Questions**: `GET/POST /api/questions/`
  - Requires: `Authorization: Token <token>`

- **Get/Update/Delete Question**: `GET/PUT/DELETE /api/questions/{id}/`
  - Requires: `Authorization: Token <token>`

## Frontend Usage

### 1. **Registration**
   - Click "Register here" on the login page
   - Fill in username, email, and password
   - You'll be automatically logged in with a token

### 2. **Login**
   - Enter username and password
   - Click Login
   - Token is saved to localStorage

### 3. **Dashboard**
   - View all your quizzes in a grid layout
   - Click any quiz to see details and questions

### 4. **Create Quiz**
   - Click "Create Quiz" button
   - Fill in title, description, category
   - Click "Create Quiz"

### 5. **View Quiz Details**
   - Click on a quiz card
   - See all questions and their options
   - Correct answers are marked with ✓

### 6. **Delete Quiz**
   - Open quiz details
   - Click "Delete" button
   - Confirm deletion

## Security Features

✅ **Token Authentication** - All API endpoints require authentication
✅ **User Isolation** - Users only see their own quizzes
✅ **Creator Permissions** - Only quiz creators can edit/delete
✅ **CORS Protection** - Only allowed origins can access the API
✅ **Password Validation** - Secure password hashing and validation

## Project Structure

```
hamari_app/
├── practice_app/
│   ├── templates/
│   │   └── index.html          # Frontend HTML
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css       # Styling
│   │   └── js/
│   │       └── app.js          # Frontend logic
│   ├── migrations/             # Database migrations
│   ├── models.py               # Quiz, Question, Option models
│   ├── views.py                # API views and frontend view
│   ├── serializers.py          # DRF serializers
│   ├── permissions.py          # Custom permissions
│   ├── urls.py                 # API routes
│   └── admin.py
├── hamari_app/
│   ├── settings.py             # Django settings
│   ├── urls.py                 # Main URL configuration
│   └── wsgi.py
├── manage.py
└── db.sqlite3                  # SQLite database
```

## Testing with cURL

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"testpass123","password2":"testpass123"}'

# Login
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'

# Create Quiz
curl -X POST http://localhost:8000/api/quizzes/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Math Quiz","description":"Test your math skills","category":"Math"}'

# Get Quizzes
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/quizzes/
```

## Troubleshooting

**CORS Error**: Make sure `localhost:8000` is in `CORS_ALLOWED_ORIGINS` in settings.py

**Token Error**: Ensure token is passed in header: `Authorization: Token <token>`

**Not seeing quizzes**: Remember - users only see their own quizzes. Create a quiz first!

**Database issues**: Run `python manage.py migrate` to apply all migrations

## Future Enhancements

- Add question creation through frontend
- Add option creation through frontend
- Export quizzes as PDF
- Quiz analytics and results tracking
- Multiple choice question types
- Quiz sharing and collaboration
- Search and filter functionality
