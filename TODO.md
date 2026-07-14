# CodeMentorAI - Project Todo List

This document outlines the sequential, atomic tasks required to build the CodeMentorAI MVP. The tech stack is **HTML/CSS/Vanilla JS** (Frontend) and **Python/FastAPI/MySQL** (Backend) using the **Gemini API**. The list is structured to ensure no overlapping dependencies, meaning each task can be completed one after the other.

## Phase 1: Project Setup & Infrastructure
- [x] 1. Initialize a new Git repository for the project (monorepo or split frontend/backend).
- [x] 2. **Backend**: Create a Python virtual environment (`python -m venv venv`).
- [x] 3. **Backend**: Create `requirements.txt` with FastAPI, Uvicorn, SQLAlchemy, MySQL-connector, passlib, python-jose, and google-generativeai.
- [x] 4. **Backend**: Install dependencies (`pip install -r requirements.txt`).
- [x] 5. **Backend**: Set up the basic FastAPI application structure (`main.py`, `routes/`, `models/`, `services/`, `utils/`).
- [x] 6. **Backend**: Create a `.env` file for `DATABASE_URL`, `GEMINI_API_KEY`, and JWT secrets (add to `.gitignore`).
- [x] 7. **Database**: Set up `database.py` with SQLAlchemy to connect to the MySQL database.
- [x] 8. **Database**: Define the SQLAlchemy database models (`User`, `Submission`, `ChatHistory`, `UserStats`) in `models.py`.
- [x] 9. **Database**: Create the initial database tables (using SQLAlchemy `Base.metadata.create_all`).
- [x] 10. **Frontend**: Create the base `index.html` structure.
- [x] 11. **Frontend**: Create empty `styles.css` and `app.js` files and link them in `index.html`.

## Phase 2: Authentication System
- [x] 12. **Backend**: Implement password hashing and JWT token generation in `utils/security.py`.
- [x] 13. **Backend**: Build the user signup endpoint (`POST /api/auth/signup`).
- [x] 14. **Backend**: Build the user login endpoint (`POST /api/auth/login`).
- [x] 15. **Backend**: Implement JWT authentication middleware/dependency to protect secure routes (`middleware/auth.py`).
- [x] 16. **Frontend**: Build the HTML/CSS UI for the Signup and Login forms (modals or separate pages).
- [x] 17. **Frontend**: Write JS logic to handle signup form submission and display validation errors/success.
- [x] 18. **Frontend**: Write JS logic to handle login form submission and securely store the JWT token (e.g., localStorage).
- [x] 19. **Frontend**: Write JS logic for the logout functionality (clearing the token and updating UI).

## Phase 3: Core UI Framework & Code Editor
- [x] 20. **Frontend**: Build the responsive Navigation Bar HTML (Brand, Links, Theme Toggle, Profile).
- [x] 21. **Frontend**: Define CSS variables for Light Mode and Dark Mode palettes (from `DESIGN.md`).
- [x] 22. **Frontend**: Implement JS logic for the Theme Toggle button to switch the `data-theme` attribute and save preference.
- [x] 23. **Frontend**: Integrate the Monaco Editor (or CodeMirror) via CDN into the main HTML container.
- [x] 24. **Frontend**: Build the HTML/CSS for the Language Selection dropdown (Python, JS, Java, C, C++, HTML, CSS, TS).
- [x] 25. **Frontend**: Implement JS logic to dynamically change the Monaco Editor syntax highlighting based on the selected language.

## Phase 4: AI Integration & Chat Interface
- [ ] 26. **Backend**: Implement the `GeminiService` class in `services/gemini_service.py` to connect to the Gemini API.
- [ ] 27. **Backend**: Create the 8 language-specific system prompt templates (focusing on line-by-line breakdown and analogies).
- [ ] 28. **Backend**: Build the code explanation endpoint (`POST /api/chat/explain`). It must save to `submissions` and `chat_history` tables.
- [ ] 29. **Backend**: Build the follow-up question endpoint (`POST /api/chat/followup`).
- [ ] 30. **Frontend**: Add the "Submit Code" button and a loading/spinner UI state.
- [ ] 31. **Frontend**: Build the Chat Interface HTML/CSS (Message container, AI/User message bubbles).
- [ ] 32. **Frontend**: Implement JS logic to send code from Monaco Editor + selected language to the `/explain` endpoint.
- [ ] 33. **Frontend**: Implement JS logic to parse the API response and render the AI's explanation in the chat interface.
- [ ] 34. **Frontend**: Add a text input field and button for asking follow-up questions in the chat interface.
- [ ] 35. **Frontend**: Implement JS logic to send follow-up questions to the `/followup` endpoint and append responses to the chat.

## Phase 5: Dashboard & History Tracking
- [ ] 36. **Backend**: Build the user statistics endpoint (`GET /api/dashboard/stats`) to aggregate user submission data.
- [ ] 37. **Backend**: Build the endpoint to fetch the current user's past code submissions (`GET /api/submissions`).
- [ ] 38. **Backend**: Build the endpoint to fetch a specific submission's chat history (`GET /api/chat/{submissionId}`).
- [ ] 39. **Frontend**: Build the HTML/CSS for the Dashboard section (Stats cards, History list layout).
- [ ] 40. **Frontend**: Implement JS logic to fetch and display the user's dashboard statistics (Total explanations, etc.).
- [ ] 41. **Frontend**: Implement JS logic to fetch and render the user's past submissions in a clickable list.
- [ ] 42. **Frontend**: Implement JS logic so clicking a past submission loads its code into the editor and its previous messages into the chat interface.

## Phase 6: Deployment & Final Polish
- [ ] 43. **Backend**: Configure CORS middleware in FastAPI to allow requests from the Vercel frontend domain.
- [ ] 44. **Deployment**: Create a Railway project and deploy the MySQL Database.
- [ ] 45. **Deployment**: Add the Railway MySQL connection string to the local `.env` to run final migrations against production.
- [ ] 46. **Deployment**: Deploy the FastAPI backend repository to Railway and configure its environment variables.
- [ ] 47. **Frontend**: Update the base API URL in the frontend JS files to point to the live Railway backend URL.
- [ ] 48. **Deployment**: Deploy the frontend repository (HTML/CSS/JS) to Vercel.
- [ ] 49. **Testing**: Perform a complete end-to-end manual test on the live production URLs (Auth -> Code Submit -> Chat -> History).
