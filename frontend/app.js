// Application entry point
let currentAuthMode = 'login';

document.addEventListener("DOMContentLoaded", () => {
    console.log("CodeMentor AI Frontend Initialized");
});

function openAuthModal() {
    document.getElementById('auth-modal').classList.remove('hidden');
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
}
