const API_BASE_URL = 'http://localhost:8000/api';

// Global state for form operations
let currentQuizId = null;
let currentQuestionId = null;

// Check if user is logged in on page load
document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('authToken');
    const username = localStorage.getItem('username');
    
    if (token) {
        showDashboard(username);
        loadQuizzes();
    }
});

// Toggle between login and register forms
function toggleForms() {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    
    loginForm.classList.toggle('hidden');
    registerForm.classList.toggle('hidden');
}

// Register user
async function registerUser() {
    const username = document.getElementById('register-username').value;
    const email = document.getElementById('register-email').value;
    const first_name = document.getElementById('register-first-name').value;
    const last_name = document.getElementById('register-last-name').value;
    const password = document.getElementById('register-password').value;
    const password2 = document.getElementById('register-password2').value;

    if (!username || !email || !password || !password2) {
        showMessage('Please fill all required fields', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/auth/register/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username,
                email,
                first_name,
                last_name,
                password,
                password2
            })
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem('authToken', data.token);
            localStorage.setItem('username', data.user.username);
            showMessage('Registration successful!', 'success');
            setTimeout(() => {
                showDashboard(data.user.username);
                loadQuizzes();
            }, 1000);
        } else {
            const errors = Object.values(data).flat().join(', ');
            showMessage(errors || 'Registration failed', 'error');
        }
    } catch (error) {
        showMessage('Error: ' + error.message, 'error');
    }
}

// Login user
async function loginUser() {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    if (!username || !password) {
        showMessage('Please enter username and password', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/auth/token/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username,
                password
            })
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem('authToken', data.token);
            localStorage.setItem('username', username);
            showMessage('Login successful!', 'success');
            setTimeout(() => {
                showDashboard(username);
                loadQuizzes();
            }, 1000);
        } else {
            showMessage('Invalid credentials', 'error');
        }
    } catch (error) {
        showMessage('Error: ' + error.message, 'error');
    }
}

// Logout user
function logoutUser() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('username');
    document.getElementById('auth-container').classList.remove('hidden');
    document.getElementById('dashboard-container').classList.add('hidden');
    document.getElementById('login-form').classList.remove('hidden');
    document.getElementById('register-form').classList.add('hidden');
    document.getElementById('login-username').value = '';
    document.getElementById('login-password').value = '';
    showMessage('Logged out successfully', 'success');
}

// Show dashboard
function showDashboard(username) {
    document.getElementById('auth-container').classList.add('hidden');
    document.getElementById('dashboard-container').classList.remove('hidden');
    document.getElementById('user-info').textContent = `Welcome, ${username}!`;
}

// Load quizzes
async function loadQuizzes() {
    const token = localStorage.getItem('authToken');
    const container = document.getElementById('quizzes-container');

    try {
        const response = await fetch(`${API_BASE_URL}/quizzes/`, {
            headers: {
                'Authorization': `Token ${token}`
            }
        });

        const quizzes = await response.json();

        if (Array.isArray(quizzes) && quizzes.length > 0) {
            container.innerHTML = quizzes.map(quiz => `
                <div class="quiz-card" onclick="viewQuiz(${quiz.id})">
                    <h3>${quiz.title}</h3>
                    <p>${quiz.description}</p>
                    <p><strong>${quiz.questions.length}</strong> questions</p>
                    <span class="category-badge">${quiz.category}</span>
                </div>
            `).join('');
        } else {
            container.innerHTML = '<p class="loading">No quizzes yet. Create your first quiz!</p>';
        }
    } catch (error) {
        container.innerHTML = `<p class="error">Error loading quizzes: ${error.message}</p>`;
    }
}

// Show quiz list view
function showQuizzes() {
    document.getElementById('quiz-list-view').classList.remove('hidden');
    document.getElementById('create-quiz-view').classList.add('hidden');
    document.getElementById('quiz-detail-view').classList.add('hidden');
    loadQuizzes();
}

// Show create quiz view
function showCreateQuiz() {
    document.getElementById('quiz-list-view').classList.add('hidden');
    document.getElementById('create-quiz-view').classList.remove('hidden');
    document.getElementById('quiz-detail-view').classList.add('hidden');
    document.getElementById('quiz-title').value = '';
    document.getElementById('quiz-description').value = '';
    document.getElementById('quiz-category').value = '';
}

// Create quiz
async function createQuiz() {
    const token = localStorage.getItem('authToken');
    const title = document.getElementById('quiz-title').value;
    const description = document.getElementById('quiz-description').value;
    const category = document.getElementById('quiz-category').value;

    if (!title || !description || !category) {
        showMessage('Please fill all fields', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/quizzes/`, {
            method: 'POST',
            headers: {
                'Authorization': `Token ${token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title,
                description,
                category
            })
        });

        if (response.ok) {
            showMessage('Quiz created successfully!', 'success');
            setTimeout(() => {
                showQuizzes();
            }, 1000);
        } else {
            showMessage('Failed to create quiz', 'error');
        }
    } catch (error) {
        showMessage('Error: ' + error.message, 'error');
    }
}

// View quiz detail
async function viewQuiz(quizId) {
    const token = localStorage.getItem('authToken');
    currentQuizId = quizId;

    try {
        const response = await fetch(`${API_BASE_URL}/quizzes/${quizId}/`, {
            headers: {
                'Authorization': `Token ${token}`
            }
        });

        const quiz = await response.json();

        document.getElementById('quiz-list-view').classList.add('hidden');
        document.getElementById('create-quiz-view').classList.add('hidden');
        document.getElementById('quiz-detail-view').classList.remove('hidden');

        document.getElementById('detail-title').textContent = quiz.title;
        document.getElementById('detail-description').textContent = quiz.description;
        document.getElementById('detail-category').textContent = `Category: ${quiz.category}`;

        // Store current quiz ID for delete
        document.getElementById('quiz-detail-view').dataset.quizId = quizId;

        // Display questions
        const questionsContainer = document.getElementById('questions-container');
        if (quiz.questions && quiz.questions.length > 0) {
            questionsContainer.innerHTML = quiz.questions.map((question, index) => `
                <div class="question-item" data-question-id="${question.id}">
                    <h4>${index + 1}. ${question.text}</h4>
                    ${question.options && question.options.length > 0 ? `
                        <ul class="options-list">
                            ${question.options.map(option => `
                                <li class="${option.is_correct ? 'correct' : ''}">
                                    <span>${option.text}</span>
                                    ${option.is_correct ? '<span class="option-badge">Correct</span>' : ''}
                                </li>
                            `).join('')}
                        </ul>
                    ` : '<p class="empty-state">No options yet</p>'}
                    <div class="question-actions">
                        <button onclick="showAddOptionForm(${question.id})" class="btn btn-primary">+ Add Option</button>
                        <button onclick="deleteQuestion(${question.id})" class="btn btn-danger">Delete Question</button>
                    </div>
                </div>
            `).join('');
        } else {
            questionsContainer.innerHTML = '<p class="empty-state">No questions yet. Click "Add Question" to get started!</p>';
        }

        // Hide any open forms
        hideAddQuestionForm();
        hideAddOptionForm();
    } catch (error) {
        showMessage('Error loading quiz: ' + error.message, 'error');
    }
}

// Delete quiz
async function deleteQuiz() {
    const token = localStorage.getItem('authToken');
    const quizId = document.getElementById('quiz-detail-view').dataset.quizId;

    if (!confirm('Are you sure you want to delete this quiz?')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/quizzes/${quizId}/`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Token ${token}`
            }
        });

        if (response.ok || response.status === 204) {
            showMessage('Quiz deleted successfully!', 'success');
            setTimeout(() => {
                showQuizzes();
            }, 1000);
        } else {
            showMessage('Failed to delete quiz', 'error');
        }
    } catch (error) {
        showMessage('Error: ' + error.message, 'error');
    }
}

// Show message
function showMessage(message, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = type;
    messageDiv.textContent = message;
    messageDiv.style.position = 'fixed';
    messageDiv.style.top = '20px';
    messageDiv.style.right = '20px';
    messageDiv.style.zIndex = '9999';
    messageDiv.style.maxWidth = '400px';
    
    document.body.appendChild(messageDiv);
    
    setTimeout(() => {
        messageDiv.remove();
    }, 4000);
}

// ============ QUESTION FUNCTIONS ============

// Show add question form
function showAddQuestionForm() {
    document.getElementById('add-question-form').classList.remove('hidden');
    document.getElementById('question-text').value = '';
    document.getElementById('question-text').focus();
}

// Hide add question form
function hideAddQuestionForm() {
    document.getElementById('add-question-form').classList.add('hidden');
    document.getElementById('question-text').value = '';
}

// Create question
async function createQuestion() {
    const token = localStorage.getItem('authToken');
    const questionText = document.getElementById('question-text').value.trim();

    if (!questionText) {
        showMessage('Please enter a question', 'error');
        return;
    }

    if (!currentQuizId) {
        showMessage('No quiz selected', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/questions/`, {
            method: 'POST',
            headers: {
                'Authorization': `Token ${token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                quiz: currentQuizId,
                text: questionText
            })
        });

        if (response.ok) {
            showMessage('Question added successfully!', 'success');
            hideAddQuestionForm();
            // Reload quiz to show new question
            viewQuiz(currentQuizId);
        } else {
            const error = await response.json();
            showMessage('Failed to create question: ' + JSON.stringify(error), 'error');
        }
    } catch (error) {
        showMessage('Error: ' + error.message, 'error');
    }
}

// Delete question
async function deleteQuestion(questionId) {
    const token = localStorage.getItem('authToken');

    if (!confirm('Are you sure you want to delete this question?')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/questions/${questionId}/`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Token ${token}`
            }
        });

        if (response.ok || response.status === 204) {
            showMessage('Question deleted successfully!', 'success');
            viewQuiz(currentQuizId);
        } else {
            showMessage('Failed to delete question', 'error');
        }
    } catch (error) {
        showMessage('Error: ' + error.message, 'error');
    }
}

// ============ OPTION FUNCTIONS ============

// Show add option form
function showAddOptionForm(questionId) {
    currentQuestionId = questionId;
    document.getElementById('add-option-form').classList.remove('hidden');
    document.getElementById('add-option-title').textContent = `Add Option to Question #${questionId}`;
    document.getElementById('option-text').value = '';
    document.getElementById('option-is-correct').checked = false;
    document.getElementById('option-text').focus();
}

// Hide add option form
function hideAddOptionForm() {
    document.getElementById('add-option-form').classList.add('hidden');
    document.getElementById('option-text').value = '';
    document.getElementById('option-is-correct').checked = false;
    currentQuestionId = null;
}

// Create option
async function createOption() {
    const token = localStorage.getItem('authToken');
    const optionText = document.getElementById('option-text').value.trim();
    const isCorrect = document.getElementById('option-is-correct').checked;

    if (!optionText) {
        showMessage('Please enter option text', 'error');
        return;
    }

    if (!currentQuestionId) {
        showMessage('No question selected', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/quizzes/options/`, {
            method: 'POST',
            headers: {
                'Authorization': `Token ${token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question: currentQuestionId,
                text: optionText,
                is_correct: isCorrect
            })
        });

        if (response.ok) {
            showMessage('Option added successfully!', 'success');
            hideAddOptionForm();
            // Reload quiz to show new option
            viewQuiz(currentQuizId);
        } else {
            const error = await response.json();
            showMessage('Failed to create option: ' + JSON.stringify(error), 'error');
        }
    } catch (error) {
        showMessage('Error: ' + error.message, 'error');
    }
}
