// Application entry point
let currentAuthMode = 'login';
const API_URL = '/api'; // Relative path - works from http://localhost:8000

document.addEventListener("DOMContentLoaded", () => {
    console.log("CodeMentor AI Frontend Initialized");
    checkAuthStatus();
    
    // Attach form submit listener
    const authForm = document.getElementById('auth-form');
    if (authForm) {
        authForm.addEventListener('submit', handleAuthSubmit);
    }
});

function openAuthModal() {
    document.getElementById('auth-modal').classList.remove('hidden');
    document.getElementById('auth-error').classList.add('hidden');
}

function closeAuthModal() {
    document.getElementById('auth-modal').classList.add('hidden');
}

function switchAuthTab(mode) {
    currentAuthMode = mode;
    const isLogin = mode === 'login';
    
    // Update Tab Styles
    document.getElementById('tab-login').classList.toggle('active', isLogin);
    document.getElementById('tab-signup').classList.toggle('active', !isLogin);
    
    // Update Form Content
    document.getElementById('modal-title').innerText = isLogin ? 'Welcome Back' : 'Create an Account';
    document.getElementById('submit-auth').innerText = isLogin ? 'Login' : 'Sign Up';
    
    // Show/Hide specific fields
    const nameGroup = document.getElementById('name-group');
    if (isLogin) {
        nameGroup.classList.add('hidden');
        document.getElementById('name').removeAttribute('required');
    } else {
        nameGroup.classList.remove('hidden');
        document.getElementById('name').setAttribute('required', 'true');
    }
    
    document.getElementById('auth-error').classList.add('hidden');
}

// Check if user is logged in
function checkAuthStatus() {
    const token = localStorage.getItem('token');
    const authBtn = document.getElementById('auth-btn');
    
    if (token) {
        authBtn.innerText = 'Logout';
        authBtn.onclick = handleLogout;
    } else {
        authBtn.innerText = 'Login / Sign Up';
        authBtn.onclick = openAuthModal;
    }
}

// Handle Logout
function handleLogout() {
    localStorage.removeItem('token');
    checkAuthStatus();
    alert("You have been successfully logged out.");
}

// Handle Login & Signup
async function handleAuthSubmit(event) {
    event.preventDefault(); // Stop page reload
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const name = document.getElementById('name').value;
    const errorDiv = document.getElementById('auth-error');
    
    errorDiv.classList.add('hidden');
    
    const isLogin = currentAuthMode === 'login';
    const endpoint = isLogin ? '/auth/login' : '/auth/signup';
    
    let payload;
    if (isLogin) {
        payload = { email, password };
    } else {
        payload = { name, email, password, gender: "Other" };
    }
    
    try {
        const response = await fetch(`${API_URL}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            // Handle error from backend (e.g. "Invalid credentials")
            throw new Error(data.detail || 'Authentication failed');
        }
        
        if (isLogin) {
            // Save token
            localStorage.setItem('token', data.access_token);
            closeAuthModal();
            checkAuthStatus();
            alert("Login successful!");
            document.getElementById('auth-form').reset();
        } else {
            // Signup successful, switch to login
            alert("Account created successfully! Please log in.");
            switchAuthTab('login');
        }
        
    } catch (error) {
        errorDiv.innerText = error.message;
        errorDiv.classList.remove('hidden');
    }
}
