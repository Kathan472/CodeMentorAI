// ==========================================
// CodeMentor AI - Frontend Application
// ==========================================

let currentAuthMode = 'login';
let monacoEditor = null;
let currentLanguage = 'python';  // tracks the active language
const API_URL = '/api';

// ==========================================
// STARTER CODE PER LANGUAGE
// ==========================================
const starterCode = {
    python:
`def greet(name):
    """A simple greeting function."""
    print(f"Hello, {name}! Welcome to CodeMentor AI!")

greet("World")
`,
    javascript:
`function greet(name) {
    // A simple greeting function
    console.log(\`Hello, \${name}! Welcome to CodeMentor AI!\`);
}

greet("World");
`,
    typescript:
`function greet(name: string): void {
    // A simple greeting function
    console.log(\`Hello, \${name}! Welcome to CodeMentor AI!\`);
}

greet("World");
`,
    java:
`public class Main {
    public static void main(String[] args) {
        String name = "World";
        System.out.println("Hello, " + name + "! Welcome to CodeMentor AI!");
    }
}
`,
    c:
`#include <stdio.h>

int main() {
    printf("Hello, World! Welcome to CodeMentor AI!\\n");
    return 0;
}
`,
    cpp:
`#include <iostream>
#include <string>

int main() {
    std::string name = "World";
    std::cout << "Hello, " << name << "! Welcome to CodeMentor AI!" << std::endl;
    return 0;
}
`,
    csharp:
`using System;

class Program {
    static void Main(string[] args) {
        string name = "World";
        Console.WriteLine($"Hello, {name}! Welcome to CodeMentor AI!");
    }
}
`,
    go:
`package main

import "fmt"

func main() {
    name := "World"
    fmt.Printf("Hello, %s! Welcome to CodeMentor AI!\\n", name)
}
`,
    rust:
`fn main() {
    let name = "World";
    println!("Hello, {}! Welcome to CodeMentor AI!", name);
}
`,
    ruby:
`def greet(name)
  puts "Hello, #{name}! Welcome to CodeMentor AI!"
end

greet("World")
`,
    php:
`<?php
function greet($name) {
    echo "Hello, $name! Welcome to CodeMentor AI!\\n";
}

greet("World");
?>
`,
    swift:
`import Foundation

func greet(_ name: String) {
    print("Hello, \\(name)! Welcome to CodeMentor AI!")
}

greet("World")
`,
    kotlin:
`fun main() {
    val name = "World"
    println("Hello, $name! Welcome to CodeMentor AI!")
}
`,
    sqlite:
`-- Welcome to CodeMentor AI SQLite Editor
-- SQLite syntax: use single quotes for strings

SELECT
    'Hello, World!' AS greeting,
    'Welcome to CodeMentor AI!' AS message;
`,
    postgresql:
`-- Welcome to CodeMentor AI PostgreSQL Editor

SELECT 
    'Hello, PostgreSQL!' AS greeting,
    current_date AS today;
`
};

// ==========================================
// DOM READY — Initialize Everything
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    console.log('[CodeMentor AI] Frontend Initialized');

    // 1. Initialize theme from localStorage
    initializeTheme();

    // 2. Check if user is already logged in
    checkAuthStatus();

    // 3. Wire up auth form
    const authForm = document.getElementById('auth-form');
    if (authForm) {
        authForm.addEventListener('submit', handleAuthSubmit);
    }

    // 4. Initialize Monaco Editor
    initMonacoEditor();
});

// ==========================================
// MONACO EDITOR
// ==========================================
function initMonacoEditor() {
    if (!window.require) {
        console.error('[Monaco] require.js not loaded');
        return;
    }

    require(['vs/editor/editor.main'], () => {
        const editorContainer = document.getElementById('editor-container');
        if (!editorContainer) return;

        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';

        monacoEditor = monaco.editor.create(editorContainer, {
            value: starterCode['python'],
            language: 'python',
            theme: isDark ? 'vs-dark' : 'vs',
            automaticLayout: true,
            minimap: { enabled: false },
            fontSize: 14,
            fontFamily: "'JetBrains Mono', 'Fira Code', Consolas, monospace",
            fontLigatures: true,
            lineNumbers: 'on',
            scrollBeyondLastLine: false,
            padding: { top: 16, bottom: 16 },
            renderLineHighlight: 'all',
            cursorBlinking: 'smooth',
            smoothScrolling: true,
        });

        // Language change → ALWAYS load starter code for the new language
        const langSelect = document.getElementById('language-select');
        if (langSelect) {
            langSelect.addEventListener('change', (e) => {
                const newLang = e.target.value;

                // Map our language keys to Monaco language IDs
                const monacoLangMap = {
                    'python':     'python',
                    'javascript': 'javascript',
                    'typescript': 'typescript',
                    'java':       'java',
                    'c':          'c',
                    'cpp':        'cpp',
                    'csharp':     'csharp',
                    'go':         'go',
                    'rust':       'rust',
                    'ruby':       'ruby',
                    'php':        'php',
                    'swift':      'swift',
                    'kotlin':     'kotlin',
                    'sqlite':     'sql',
                    'postgresql': 'pgsql',
                };
                const monacoLang = monacoLangMap[newLang] || newLang;

                // Always: update Monaco syntax highlighting
                monaco.editor.setModelLanguage(monacoEditor.getModel(), monacoLang);

                // Always: load starter code for the new language
                if (starterCode[newLang]) {
                    monacoEditor.setValue(starterCode[newLang]);
                }

                currentLanguage = newLang;

                // Reset output terminal
                setOutput('Ready. Press Run to execute your code.', 'default');
            });
        }

        // Run Code button
        const runBtn = document.getElementById('run-code-btn');
        if (runBtn) runBtn.addEventListener('click', executeCode);

        // Clear editor button
        const clearBtn = document.getElementById('clear-editor-btn');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => {
                monacoEditor.setValue('');
                setOutput('Editor cleared.', 'default');
            });
        }

        // Clear output button
        const clearOutputBtn = document.getElementById('clear-output-btn');
        if (clearOutputBtn) {
            clearOutputBtn.addEventListener('click', () => {
                setOutput('Ready. Press Run to execute your code.', 'default');
            });
        }

        // Explain Code button (Phase 4 placeholder)
        const explainBtn = document.getElementById('explain-code-btn');
        if (explainBtn) {
            explainBtn.addEventListener('click', () => {
                setOutput('AI code explanation coming in Phase 4! Stay tuned.', 'loading');
            });
        }
    });
}

// ==========================================
// CODE EXECUTION — via backend proxy
// ==========================================
function setOutput(text, type = 'default') {
    const el = document.getElementById('output-content');
    if (!el) return;
    el.textContent = text;
    el.className = 'output-content';
    if (type === 'success') el.classList.add('output-success');
    else if (type === 'error')   el.classList.add('output-error');
    else if (type === 'loading') el.classList.add('output-loading');
}

async function executeCode() {
    if (!monacoEditor) {
        setOutput('Editor not initialized.', 'error');
        return;
    }

    const code = monacoEditor.getValue();
    const langSelect = document.getElementById('language-select');
    const language = langSelect ? langSelect.value : 'python';
    const runBtn = document.getElementById('run-code-btn');

    if (!code.trim()) {
        setOutput('Error: No code to execute. Please write some code first.', 'error');
        return;
    }

    // Disabled specific client-side checks for non-exec since we rely on backend
    // and we removed the HTML/CSS options.

    // Disable button while running
    if (runBtn) {
        runBtn.disabled = true;
        runBtn.classList.add('running');
        runBtn.innerHTML = '<span class="run-icon">⏳</span> Running...';
    }
    setOutput('⏳ Executing your code...', 'loading');

    try {
        const response = await fetch(`${API_URL}/code/execute`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ language, code })
        });

        const data = await response.json();

        if (!response.ok) {
            setOutput(`Server Error: ${data.detail || 'Unknown error'}`, 'error');
            return;
        }

        if (data.success) {
            setOutput(data.output || 'Code executed successfully (no output).', 'success');
        } else {
            const errorText = data.error || 'Execution failed with an unknown error.';
            const outputText = data.output ? `Program Output:\n${data.output}\n\n` : '';
            setOutput(outputText + errorText, 'error');
        }
    } catch (err) {
        setOutput(`Network Error: ${err.message}\n\nMake sure the server is running at localhost:8000`, 'error');
    } finally {
        // Re-enable button
        if (runBtn) {
            runBtn.disabled = false;
            runBtn.classList.remove('running');
            runBtn.innerHTML = '<span class="run-icon">▶</span> Run';
        }
    }
}

// ==========================================
// THEME MANAGEMENT
// ==========================================
function initializeTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);

    const themeToggleBtn = document.getElementById('theme-toggle');
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const current = document.documentElement.getAttribute('data-theme');
            const next = current === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', next);
            localStorage.setItem('theme', next);
            updateThemeIcon(next);

            // Sync Monaco theme
            if (window.monaco && monacoEditor) {
                monaco.editor.setTheme(next === 'dark' ? 'vs-dark' : 'vs');
            }
        });
    }
}

function updateThemeIcon(theme) {
    const icon = document.querySelector('.theme-icon');
    if (icon) icon.textContent = theme === 'dark' ? '☀️' : '🌙';
}

// ==========================================
// AUTH MODAL
// ==========================================
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

    document.getElementById('tab-login').classList.toggle('active', isLogin);
    document.getElementById('tab-signup').classList.toggle('active', !isLogin);
    document.getElementById('modal-title').innerText = isLogin ? 'Welcome Back' : 'Create an Account';
    document.getElementById('submit-auth').innerText = isLogin ? 'Login' : 'Sign Up';

    const nameGroup = document.getElementById('name-group');
    const nameInput = document.getElementById('name');
    if (isLogin) {
        nameGroup.classList.add('hidden');
        nameInput.removeAttribute('required');
    } else {
        nameGroup.classList.remove('hidden');
        nameInput.setAttribute('required', 'true');
    }

    document.getElementById('auth-error').classList.add('hidden');
}

// ==========================================
// AUTH STATUS (Logged in / out)
// ==========================================
function checkAuthStatus() {
    const token = localStorage.getItem('token');
    const authBtn = document.getElementById('auth-btn');
    if (!authBtn) return;

    if (token) {
        authBtn.textContent = 'Logout';
        authBtn.onclick = handleLogout;
    } else {
        authBtn.textContent = 'Login / Sign Up';
        authBtn.onclick = openAuthModal;
    }
}

function handleLogout() {
    localStorage.removeItem('token');
    checkAuthStatus();
    // Show a subtle notification instead of alert
    showToast('You have been logged out.');
}

// ==========================================
// AUTH FORM SUBMISSION
// ==========================================
async function handleAuthSubmit(event) {
    event.preventDefault();

    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const name = document.getElementById('name').value.trim();
    const errorDiv = document.getElementById('auth-error');
    const submitBtn = document.getElementById('submit-auth');

    errorDiv.classList.add('hidden');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Please wait...';

    const isLogin = currentAuthMode === 'login';
    const endpoint = isLogin ? '/auth/login' : '/auth/signup';
    const payload = isLogin
        ? { email, password }
        : { name, email, password, gender: 'Other' };

    try {
        const response = await fetch(`${API_URL}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Authentication failed. Please try again.');
        }

        if (isLogin) {
            localStorage.setItem('token', data.access_token);
            closeAuthModal();
            checkAuthStatus();
            document.getElementById('auth-form').reset();
            showToast('✅ Logged in successfully!');
        } else {
            showToast('✅ Account created! Please log in.');
            switchAuthTab('login');
        }

    } catch (err) {
        errorDiv.textContent = err.message;
        errorDiv.classList.remove('hidden');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = isLogin ? 'Login' : 'Sign Up';
    }
}

// ==========================================
// TOAST NOTIFICATION (replaces alert)
// ==========================================
function showToast(message, duration = 3000) {
    // Remove existing toast
    const existing = document.getElementById('toast-notification');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.id = 'toast-notification';
    toast.style.cssText = `
        position: fixed;
        bottom: 1.5rem;
        right: 1.5rem;
        background: #1E293B;
        color: #F1F5F9;
        padding: 0.875rem 1.25rem;
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        font-size: 0.9rem;
        font-weight: 500;
        z-index: 9999;
        transform: translateY(0);
        transition: all 0.3s ease;
        max-width: 320px;
        font-family: 'Inter', sans-serif;
    `;
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(8px)';
        setTimeout(() => toast.remove(), 300);
    }, duration);
}
