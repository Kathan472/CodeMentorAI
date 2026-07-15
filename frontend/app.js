// ==========================================
// CodeMentor AI - Frontend Application
// ==========================================

let currentAuthMode = 'login';
let monacoEditor = null;
window.updateLangIcon = function(newLang) {
    const langIcon = document.getElementById('lang-icon');
    if (langIcon) {
        const deviconMap = {
            'python': 'python/python-original.svg',
            'javascript': 'javascript/javascript-original.svg',
            'typescript': 'typescript/typescript-original.svg',
            'html': 'html5/html5-original.svg',
            'css': 'css3/css3-original.svg',
            'java': 'java/java-original.svg',
            'c': 'c/c-original.svg',
            'cpp': 'cplusplus/cplusplus-original.svg',
            'csharp': 'csharp/csharp-original.svg',
            'go': 'go/go-original.svg',
            'rust': 'rust/rust-original.svg',
            'ruby': 'ruby/ruby-original.svg',
            'php': 'php/php-original.svg',
            'swift': 'swift/swift-original.svg',
            'kotlin': 'kotlin/kotlin-original.svg',
            'shell': 'bash/bash-original.svg'
        };
        const iconPath = deviconMap[newLang] || 'devicon/devicon-original.svg';
        langIcon.src = `https://cdn.jsdelivr.net/gh/devicons/devicon/icons/${iconPath}`;
    }
};

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
                    'shell':      'shell',
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
                             // Update language icon
                if (typeof window.updateLangIcon === 'function') {
                    window.updateLangIcon(newLang);
                }
                
                // Clear AI chat and code snippet memory when switching languages manually
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

        // Explain Code button
        const explainBtn = document.getElementById('explain-code-btn');
        if (explainBtn) {
            explainBtn.addEventListener('click', explainCode);
        }

        // Close AI Panel button
        const closeAiBtn = document.getElementById('close-ai-btn');
        if (closeAiBtn) {
            closeAiBtn.addEventListener('click', () => {
                const aiPanel = document.getElementById('ai-panel');
                if (aiPanel) aiPanel.classList.add('hidden');
            });
        }

        // Terminal Clear button
        const clearTermBtn = document.getElementById('clear-btn');
        if (clearTermBtn) {
            clearTermBtn.addEventListener('click', () => {
                setOutput('Ready. Press Run to execute your code.', 'default');
            });
        }

        // Follow-up Input logic
        const sendFollowupBtn = document.getElementById('send-followup-btn');
        const followupInput = document.getElementById('followup-input');
        if (sendFollowupBtn && followupInput) {
            sendFollowupBtn.addEventListener('click', sendFollowUp);
            followupInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') sendFollowUp();
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
    const stdinEl = document.getElementById('stdin-input');
    const stdin = stdinEl ? stdinEl.value : '';

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
            body: JSON.stringify({ language, code, stdin })
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
// AI CHAT & CODE EXPLANATION
// ==========================================
let currentSubmissionId = null;

async function explainCode() {
    if (!monacoEditor) {
        alert('Editor not initialized.');
        return;
    }

    const code = monacoEditor.getValue();
    const langSelect = document.getElementById('language-select');
    const language = langSelect ? langSelect.value : 'python';
    const githubUrlInput = document.getElementById('github-url-input');
    const github_url = githubUrlInput ? githubUrlInput.value.trim() : null;
    
    if (!code.trim() && !github_url) {
        alert('Error: No code or GitHub URL to explain. Please write some code or paste a GitHub link first.');
        return;
    }

    const token = localStorage.getItem('token');
    if (!token) {
        alert('You must be logged in to use the AI Code Explanation feature.');
        openAuthModal();
        return;
    }

    const explainBtn = document.getElementById('explain-code-btn');
    const aiPanel = document.getElementById('ai-panel');
    const aiChatHistory = document.getElementById('ai-chat-history');
    const aiChatInputContainer = document.getElementById('ai-chat-input-container');

    // UI Updates: Disable button, show panel, show loading
    if (explainBtn) {
        explainBtn.disabled = true;
        explainBtn.innerHTML = '⏳ Thinking...';
    }
    
    if (aiPanel) aiPanel.classList.remove('hidden');
    if (aiChatInputContainer) aiChatInputContainer.classList.add('hidden'); // Hide input until initial explanation is done
    
    // Clear chat history and set up first message
    currentSubmissionId = null;
    let loadingText = github_url ? 'CodeMentor AI is fetching and analyzing the repository...' : 'CodeMentor AI is analyzing your code...';
    aiChatHistory.innerHTML = `
        <div class="chat-message ai-message">
            <div id="ai-response-content" class="ai-response-content">
                <div class="ai-loading"><div class="spinner"></div><span>${loadingText}</span></div>
            </div>
        </div>
    `;
    const aiContent = document.getElementById('ai-response-content');

    try {
        const response = await fetch(`${API_URL}/chat/explain`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ language, code, github_url })
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            if (response.status === 401) {
                localStorage.removeItem('token');
                aiContent.innerHTML = `<p class="ai-error">Session expired. Please log in again.</p>`;
                openAuthModal();
            } else {
                aiContent.innerHTML = `<p class="ai-error">Error: ${errorData.detail || 'Failed to explain code'}</p>`;
            }
            return;
        }

        // Initialize streaming response handling (SSE format)
        let explanationText = '';
        let firstChunkReceived = false;
        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;
            
            const chunkStr = decoder.decode(value, { stream: true });
            
            // SSE chunks look like: data: {"chunk": "..."}\n\n
            const lines = chunkStr.split('\n');
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    try {
                        const data = JSON.parse(line.substring(6));
                        
                        if (data.submission_id) {
                            currentSubmissionId = data.submission_id;
                        }
                        
                        if (data.error) {
                            if (!firstChunkReceived) {
                                aiContent.innerHTML = '';
                                firstChunkReceived = true;
                            }
                            aiContent.innerHTML += `<p class="ai-error" style="color: #ef4444; margin-top: 10px;">Error: ${data.error}</p>`;
                        }

                        if (data.chunk) {
                            if (!firstChunkReceived) {
                                aiContent.innerHTML = '';
                                firstChunkReceived = true;
                            }
                            explanationText += data.chunk;
                            aiContent.innerHTML = marked.parse(explanationText);
                            aiChatHistory.scrollTop = aiChatHistory.scrollHeight;
                        }
                    } catch (e) {
                        console.error("Error parsing SSE JSON:", e, line);
                    }
                }
            }
        }
        
        // Show follow-up input
        if (aiChatInputContainer) aiChatInputContainer.classList.remove('hidden');
        
    } catch (err) {
        aiContent.innerHTML = `<p class="ai-error">Network Error: ${err.message}</p>`;
    } finally {
        if (explainBtn) {
            explainBtn.disabled = false;
            explainBtn.innerHTML = 'Explain Code';
        }
        // Refresh dashboard stats so explanations increment in UI immediately
        loadDashboard();
    }
}

async function sendFollowUp() {
    const inputEl = document.getElementById('followup-input');
    const sendBtn = document.getElementById('send-followup-btn');
    const aiChatHistory = document.getElementById('ai-chat-history');
    const question = inputEl.value.trim();

    if (!question || !currentSubmissionId) return;

    const token = localStorage.getItem('token');
    if (!token) return;

    // 1. Add User Message to UI
    inputEl.value = '';
    inputEl.disabled = true;
    sendBtn.disabled = true;

    aiChatHistory.insertAdjacentHTML('beforeend', `
        <div class="chat-message user-message">
            ${question}
        </div>
    `);
    
    // Create AI response placeholder
    const aiMessageId = 'ai-msg-' + Date.now();
    aiChatHistory.insertAdjacentHTML('beforeend', `
        <div class="chat-message ai-message">
            <div id="${aiMessageId}" class="ai-response-content">
                <div class="ai-loading"><div class="spinner"></div><span>Thinking...</span></div>
            </div>
        </div>
    `);
    aiChatHistory.scrollTop = aiChatHistory.scrollHeight;
    
    const aiContent = document.getElementById(aiMessageId);

    try {
        const response = await fetch(`${API_URL}/chat/followup`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ 
                submission_id: currentSubmissionId, 
                question: question 
            })
        });

        if (!response.ok) {
            aiContent.innerHTML = `<p class="ai-error">Failed to send message.</p>`;
            return;
        }

        let answerText = '';
        let firstChunkReceived = false;
        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;
            
            const chunkStr = decoder.decode(value, { stream: true });
            const lines = chunkStr.split('\n');
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    try {
                        const data = JSON.parse(line.substring(6));
                        
                        if (data.error) {
                            aiContent.innerHTML = `<p class="ai-error">${data.error}</p>`;
                            return;
                        }
                        
                        if (data.chunk) {
                            if (!firstChunkReceived) {
                                aiContent.innerHTML = '';
                                firstChunkReceived = true;
                            }
                            answerText += data.chunk;
                            aiContent.innerHTML = marked.parse(answerText);
                            aiChatHistory.scrollTop = aiChatHistory.scrollHeight;
                        }
                    } catch (e) {
                        console.error("Error parsing SSE JSON:", e, line);
                    }
                }
            }
        }
    } catch (err) {
        aiContent.innerHTML = `<p class="ai-error">Network Error: ${err.message}</p>`;
    } finally {
        inputEl.disabled = false;
        sendBtn.disabled = false;
        inputEl.focus();
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
function openAuthModal(mode = 'login') {
    switchAuthTab(mode);
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
function parseJwt(token) {
    try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));
        return JSON.parse(jsonPayload);
    } catch(e) {
        return null;
    }
}

function checkAuthStatus() {
    const token = localStorage.getItem('token');
    const authButtonsContainer = document.getElementById('auth-buttons-container');
    const userProfileContainer = document.getElementById('user-profile-container');
    const dropdownEmail = document.getElementById('dropdown-email');
    
    if (!authButtonsContainer || !userProfileContainer) return;

    if (token) {
        authButtonsContainer.classList.add('hidden');
        userProfileContainer.classList.remove('hidden');
        
        const payload = parseJwt(token);
        if (payload && payload.email) {
            dropdownEmail.textContent = payload.email;
        } else {
            dropdownEmail.textContent = 'Logged In';
        }
    } else {
        authButtonsContainer.classList.remove('hidden');
        userProfileContainer.classList.add('hidden');
    }
}

function handleLogout() {
    localStorage.removeItem('token');
    document.getElementById('dropdown-menu').classList.remove('show');
    checkAuthStatus();
    // Switch to editor section
    document.querySelector('a[href="#editor-section"]').click();
    showToast('You have been logged out.');
}

document.addEventListener('DOMContentLoaded', () => {
    const avatarBtn = document.getElementById('avatar-btn');
    const dropdownMenu = document.getElementById('dropdown-menu');
    const logoutBtn = document.getElementById('logout-btn');

    if (avatarBtn && dropdownMenu) {
        avatarBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            dropdownMenu.classList.toggle('show');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!avatarBtn.contains(e.target) && !dropdownMenu.contains(e.target)) {
                dropdownMenu.classList.remove('show');
            }
        });
    }

    if (logoutBtn) {
        logoutBtn.addEventListener('click', handleLogout);
    }
});

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

/* =========================================================
   Dashboard & History Logic
   ========================================================= */

async function loadDashboard() {
    const token = localStorage.getItem('token');
    if (!token) return;

    try {
        // Fetch Stats
        const statsRes = await fetch(`${API_URL}/dashboard/stats`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (statsRes.ok) {
            const stats = await statsRes.json();
            const statSubmissions = document.getElementById('stat-total-submissions');
            if (statSubmissions) statSubmissions.textContent = stats.total_submissions || 0;
            
            const statExplanations = document.getElementById('stat-total-explanations');
            if (statExplanations) statExplanations.textContent = stats.total_explanations || 0;
            
            const langsCount = Object.keys(stats.languages_practiced || {}).length;
            const statLangs = document.getElementById('stat-languages');
            if (statLangs) statLangs.textContent = langsCount || 0;
        }

        // Fetch History
        const histRes = await fetch(`${API_URL}/submissions`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (histRes.ok) {
            const submissions = await histRes.json();
            const list = document.getElementById('history-list');
            list.innerHTML = '';
            
            if (submissions.length === 0) {
                list.innerHTML = '<li class="history-item"><div class="history-item-left"><span class="history-snippet">No past submissions found.</span></div></li>';
            }
            
            submissions.forEach(sub => {
                const li = document.createElement('li');
                li.className = 'history-item';
                const dateStr = new Date(sub.created_at).toLocaleString();
                let snippet = sub.code_snippet || sub.github_url || 'No code provided';
                if (snippet.length > 50) snippet = snippet.substring(0, 50) + '...';
                
                li.innerHTML = `
                    <div class="history-item-left">
                        <span class="history-language">${sub.language}</span>
                        <span class="history-snippet">${snippet}</span>
                        <span class="history-date">${dateStr}</span>
                    </div>
                `;
                li.addEventListener('click', () => loadSubmission(sub));
                list.appendChild(li);
            });
        }
    } catch (err) {
        console.error("Failed to load dashboard:", err);
    }
}

async function loadSubmission(sub) {
    // 1. Switch back to editor tab
    document.querySelector('a[href="#editor-section"]').click();
    
    // 2. Set language and code
    const langSelect = document.getElementById('language-select');
    if (langSelect) langSelect.value = sub.language.toLowerCase();
    
    // Update Monaco model language if editor exists
    if (monacoEditor) {
        const monacoLangMap = {
            'cpp': 'cpp', 'java': 'java', 'javascript': 'javascript', 'python': 'python',
            'go': 'go', 'ruby': 'ruby', 'php': 'php', 'csharp': 'csharp', 'swift': 'swift'
        };
        const lang = sub.language.toLowerCase();
        const monacoLang = monacoLangMap[lang] || lang;
        
        monaco.editor.setModelLanguage(monacoEditor.getModel(), monacoLang);
        if (typeof updateLangIcon === 'function') {
            updateLangIcon(lang);
        }
        if (sub.code_snippet) {
            monacoEditor.setValue(sub.code_snippet);
            document.getElementById('github-url-input').value = '';
        } else if (sub.github_url) {
            monacoEditor.setValue('');
            document.getElementById('github-url-input').value = sub.github_url;
        }
    }
    
    currentSubmissionId = sub.id;
    
    // 3. Fetch chat history
    const token = localStorage.getItem('token');
    if (!token) return;
    
    const aiChatHistory = document.getElementById('ai-chat-history');
    const aiChatInputContainer = document.getElementById('ai-chat-input-container');
    const aiPanel = document.getElementById('ai-panel');
    
    if (aiPanel) aiPanel.classList.remove('hidden');
    
    aiChatHistory.innerHTML = '<p class="ai-loading">Loading chat history...</p>';
    aiChatInputContainer.classList.add('hidden');
    
    try {
        const chatRes = await fetch(`/api/chat/${sub.id}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (chatRes.ok) {
            const chatHistory = await chatRes.json();
            aiChatHistory.innerHTML = ''; // Clear initial loading message
            
            chatHistory.forEach(chat => {
                if (chat.user_message && chat.user_message !== 'Explain this code') {
                    const userMsg = document.createElement('div');
                    userMsg.className = 'ai-message user-message';
                    userMsg.innerHTML = marked.parse(chat.user_message);
                    aiChatHistory.appendChild(userMsg);
                }
                
                const aiMsg = document.createElement('div');
                aiMsg.className = 'ai-message ai-response';
                aiMsg.innerHTML = marked.parse(chat.ai_response);
                aiChatHistory.appendChild(aiMsg);
            });
            
            aiChatInputContainer.classList.remove('hidden');
            
            // Scroll to bottom
            aiChatHistory.scrollTop = aiChatHistory.scrollHeight;
        } else {
            aiChatHistory.innerHTML = '<p class="ai-error">Failed to load history.</p>';
        }
    } catch (err) {
        aiChatHistory.innerHTML = `<p class="ai-error">Network Error: ${err.message}</p>`;
    }
}

// Navigation Setup
document.addEventListener('DOMContentLoaded', () => {
    const navLinks = document.querySelectorAll('.nav-link');
    const editorSection = document.getElementById('editor-section');
    const dashboardSection = document.getElementById('dashboard-section');
    const historySection = document.getElementById('history-section');
    
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href');
            
            // Update active link state
            navLinks.forEach(l => l.style.fontWeight = '500');
            link.style.fontWeight = 'bold';
            
            // Hide all by default
            if (editorSection) {
                editorSection.classList.add('hidden');
                editorSection.style.display = 'none';
            }
            if (dashboardSection) {
                dashboardSection.classList.add('hidden');
                dashboardSection.style.display = 'none';
            }
            if (historySection) {
                historySection.classList.add('hidden');
                historySection.style.display = 'none';
            }
            
            if (targetId === '#editor-section') {
                if (editorSection) {
                    editorSection.classList.remove('hidden');
                    editorSection.style.display = 'block';
                }
            } else if (targetId === '#dashboard') {
                if (dashboardSection) {
                    dashboardSection.classList.remove('hidden');
                    dashboardSection.style.display = 'block';
                }
                loadDashboard();
            } else if (targetId === '#history') {
                if (historySection) {
                    historySection.classList.remove('hidden');
                    historySection.style.display = 'block';
                }
                loadDashboard();
            }
        });
    });
});
