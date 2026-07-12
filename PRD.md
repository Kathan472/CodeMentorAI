# CodeMentor AI - Product Requirements Document

**Document Version:** 1.0  
**Last Updated:** July 2026  
**Status:** Active Development  
**Target Release:** Phase 1 (MVP) - 14-16 weeks

---

## 1. Executive Summary

**CodeMentor AI** is an AI-powered education platform designed to teach programming concepts through interactive code explanation and personalized learning. Unlike traditional learning platforms or ChatGPT clones, CodeMentor AI acts as a teaching assistant that explains code, identifies bugs, generates practice problems, and tracks learning progress.

**Vision:** Democratize programming education by providing every student with a personalized AI tutor that understands their learning pace and weak areas.

**Target Market:** University students majoring in Computer Science, Data Science, Computer Information Systems, and related tech disciplines (ages 18-25).

---

## 2. Goals & Objectives

### Primary Goals
- **Goal 1:** Enable students to understand code at a deep level through AI-powered explanations
- **Goal 2:** Identify and help students overcome knowledge gaps through personalized tracking
- **Goal 3:** Create an engaging learning experience that reduces dependency on tutors

### Measurable Objectives (Success Metrics)
- Achieve 50+ active users in first month
- Average session duration: 20+ minutes
- User retention rate: 40%+ weekly active users
- 80%+ code submission success rate (proper parsing)
- Average explanation satisfaction rating: 4.0+/5.0

---

## 3. Target Users & User Personas

### Primary User Persona
**Name:** Sarah (CS Major)
- **Age:** 20
- **Background:** Sophomore in Computer Science program
- **Pain Points:** Struggles with understanding complex code structures, feels lost during lectures, doesn't have time for tutoring
- **Goals:** Pass her Data Structures course, build confidence in coding

### Secondary User Persona
**Name:** Marcus (Self-Learner)
- **Age:** 22
- **Background:** Career-changing bootcamp student
- **Pain Points:** No formal CS background, needs quick explanations, wants instant feedback
- **Goals:** Learn Python quickly, build portfolio projects

### Tertiary User Persona
**Name:** Professor Chen (Educator)
- **Age:** 45
- **Background:** Computer Science instructor
- **Pain Points:** Too many students to help individually, repetitive questions
- **Goals:** Reduce office hours load, improve student outcomes

---

## 4. User Stories

### Phase 1: Core Learning Experience

#### Story 1.1: Code Explanation
**As a** student  
**I want to** paste code and get line-by-line explanations with practical examples  
**So that** I can understand what each part does with real-world context

**Acceptance Criteria:**
- [ ] User can paste code in a code editor with syntax highlighting
- [ ] AI provides clear, beginner-friendly explanations with concrete examples
- [ ] Explanations include plain English descriptions of each line
- [ ] Each explanation includes a practical example (BEFORE/AFTER or use case)
- [ ] User can ask follow-up questions about specific lines
- [ ] Explanation is provided within 3 seconds
- [ ] Examples are language-specific and relatable

**Suggested Implementation:** Use Claude API with language-aware system prompts optimized for example-based teaching

---

#### Story 1.2: Language Selection
**As a** student  
**I want to** select my programming language  
**So that** the AI understands and explains code correctly

**Acceptance Criteria:**
- [ ] Landing page shows language selection
- [ ] Supported languages: Python, Java, C++, JavaScript, C, HTML, CSS, Ruby, Go, Rust, TypeScript, PHP, SQL
- [ ] Language affects syntax highlighting
- [ ] AI adjusts explanations based on language idioms
- [ ] User can change language at any time

**Phased Language Rollout Strategy:**
- **Phase 1 (MVP):** All 8 languages (Python, JavaScript, Java, C, C++, HTML, CSS, TypeScript)
- **Phase 2:** Add Ruby, Go, Rust, PHP, SQL
- **Phase 3+:** Additional languages and specialized domain support

---

#### Story 1.3: Chat History
**As a** student  
**I want to** see my previous conversations  
**So that** I can review what I learned earlier

**Acceptance Criteria:**
- [ ] All explanations are saved in chat history
- [ ] History is organized by date
- [ ] User can search through previous conversations
- [ ] Each code snippet is stored with its explanation

**Suggested Implementation:** Simple timestamp-based sorting initially

---

#### Story 1.4: User Authentication
**As a** student  
**I want to** create an account and log in  
**So that** my progress is saved across sessions

**Acceptance Criteria:**
- [ ] User can sign up with email
- [ ] User can log in securely
- [ ] Password is hashed (using bcrypt)
- [ ] Sessions persist across browser sessions
- [ ] User profile shows join date and stats

**Suggested Implementation:** JWT tokens with 7-day expiration

---

#### Story 1.5: Code Editor
**As a** student  
**I want to** write or paste code in a nice editor  
**So that** the code is easy to read and format

**Acceptance Criteria:**
- [ ] Code editor supports multiple languages with syntax highlighting
- [ ] Copy/paste works smoothly
- [ ] Auto-indentation is available
- [ ] Character count is displayed
- [ ] Submit button sends code to AI

**Suggested Tool:** Monaco Editor (VS Code's engine) or CodeMirror

---

### Phase 2: Learning Enhancement (Post-MVP)

#### Story 2.1: Quiz Generation
**As a** student  
**I want to** take a quiz on the code I just learned  
**So that** I can test my understanding

**Acceptance Criteria:**
- [ ] AI generates 3-5 multiple-choice questions based on code
- [ ] Questions test understanding, not memorization
- [ ] User can see correct answers with explanations
- [ ] Quiz results are saved

---

#### Story 2.2: Weakness Tracking
**As a** student  
**I want to** see which concepts I struggle with  
**So that** I can focus my study time

**Acceptance Criteria:**
- [ ] Dashboard shows "Weak Areas" (loops, recursion, OOP, etc.)
- [ ] AI tags code submissions with relevant concepts
- [ ] Weak areas are ranked by frequency
- [ ] Visual chart shows progress over time

---

---

## 5. Feature List

### MVP Features (Phase 1 - Beginner Focused)

#### Core Features
1. **User Authentication**
   - Email/password sign up
   - Secure login
   - Profile dashboard with username and stats
   - Logout functionality

2. **Code Input & Display**
   - Code editor with syntax highlighting (Python focus)
   - Paste or type code
   - Character/line counter
   - Clear/Reset button
   - Submit button

3. **AI Code Explanation**
   - Line-by-line explanation with real-world examples
   - Plain English descriptions with analogies
   - Function/variable purpose explanation with use cases
   - Output prediction with worked examples
   - 3-second response time target
   - Related code examples for better understanding

4. **Chat History**
   - View all previous sessions
   - Search by date or keyword
   - Delete individual conversations
   - Export conversation as text

5. **Dashboard**
   - Total explanations count
   - Languages practiced
   - Last session date
   - Total learning time

### Phase 2 Features (Post-MVP)
- Quiz generation based on code
- Flashcard system
- Practice problem recommendations
- Visual flowchart generation
- Bug detection and explanation
- Concept tagging and tracking
- Personalized study plan

### Phase 3 Features (Advanced)
- Code complexity analysis
- Performance optimization suggestions
- Collaborative learning (peer review)
- Mobile app version
- Integration with GitHub

---

## 6. Non-Functional Requirements

### Performance
- API response time: < 3 seconds for explanations
- Page load time: < 2 seconds
- Database query time: < 200ms
- Support for 100+ concurrent users

### Security
- All passwords hashed (bcrypt)
- HTTPS only
- SQL injection prevention (parameterized queries)
- Rate limiting on API (100 requests/hour per user)
- User data encryption at rest

### Scalability
- Stateless backend for horizontal scaling
- Database indexing on frequently queried columns
- Caching layer for frequently asked concepts
- CDN for frontend assets

### Usability
- Mobile-responsive design
- Accessibility (WCAG 2.1 AA)
- Error messages in plain language
- Loading indicators for API calls
- Dark/light mode support

---

## 7. Technology Stack Recommendations

### Frontend
- **Framework:** React.js (or Vue.js if preferred)
- **Code Editor:** Monaco Editor or CodeMirror
- **Styling:** Tailwind CSS (fast, utility-first)
- **HTTP Client:** Axios or Fetch API

### Backend
- **Language:** Node.js + Express.js (JavaScript) or Python + Flask
- **Authentication:** JWT (JSON Web Tokens)
- **Rate Limiting:** express-rate-limit or similar

### Database
- **Primary:** PostgreSQL (relational data for users, sessions)
- **Cache:** Redis (optional, for session storage)
- **File Storage:** AWS S3 or Firebase Storage (optional for exports)

### AI/ML
- **API:** Anthropic Claude API (claude-sonnet-4-6 or later)
- **Prompt Engineering:** Dedicated system prompts for teaching vs. explaining

### DevOps & Deployment
- **Version Control:** GitHub
- **Hosting:** Vercel (frontend) + Railway/Render (backend)
- **Environment:** Docker for containerization
- **Monitoring:** Sentry for error tracking

### Analytics
- **User Tracking:** Posthog or Mixpanel
- **Metrics:** Tracking accuracy, session duration, user retention

---

## 8. Beginner Project Recommendations

Since this is your **first big project**, here are strategic suggestions to keep scope manageable while demonstrating key skills:

### MVP Scope (Phase 1 Only)
**Recommended Timeline:** 14-16 weeks

**Week 1-2: Setup & Auth**
- Project setup (React + Express)
- Database schema design
- User authentication flow
- Deployed basic "Hello World"

**Week 3-5: Code Editor & Languages**
- Integrate code editor component (support 8 languages)
- Language selection dropdown
- Syntax highlighting for all 8 languages (Python, JS, Java, C, C++, HTML, CSS, TypeScript)
- Create code submission API endpoint
- Test language detection

**Week 6-10: AI Integration with Examples**
- Integrate Claude API
- Create system prompts for explanations (language-aware, example-based)
- Develop example generation logic
- Test with real API calls for each language
- Add error handling and language detection
- Optimize prompts for clarity and examples

**Week 11-13: Features & Polish**
- Chat history storage and retrieval
- Dashboard statistics (languages practiced, total submissions)
- Code highlighting by language
- Example display formatting
- Multi-language support verification
- Performance testing across all languages

**Week 14-15: Testing & Optimization**
- Test with all 8 languages thoroughly
- Performance optimization
- Bug fixes across languages
- Load testing

**Week 16: Final Polish & Deploy**
- UI improvements
- Security audit
- Production deployment

### Beginner Feature Prioritization

#### Must-Have (Drop-Dead Essential)
1. User sign up/login
2. Code submission with syntax highlighting (8 languages: Python, JavaScript, Java, C, C++, HTML, CSS, TypeScript)
3. AI explanation via Claude API with examples
4. Display explanation with code examples to user
5. Save explanations to database
6. View chat history

#### Should-Have (Adds Real Value)
1. Dashboard with stats (languages practiced count)
2. Language selection dropdown (shows all 8 languages)
3. Search chat history
4. Better UI/UX
5. Example-based explanations for each language

#### Nice-to-Have (If You Have Time)
1. Export as PDF
2. Dark mode
3. Mobile optimization
4. Keyboard shortcuts
5. Support for additional languages (Ruby, Go, Rust, PHP, SQL)

### Recommended Simplifications for First Project

| Feature | Full Version | Beginner Version (MVP) | Timeline |
|---------|--------------|------------------|----------|
| Languages | 13+ languages | 8 languages (Python, JS, Java, C, C++, HTML, CSS, TS) | Add Ruby, Go, Rust, PHP, SQL in Phase 2 |
| Quiz | AI-generated questions | Text-based questions (no full QA) | Phase 2 |
| Weak Areas | Automatic concept tagging | Manual tagging by user | Phase 3 |
| Flowcharts | Auto-generated SVGs | Link to AI explanation | Phase 2 |
| Bug Detection | Automatic parsing | AI description with examples | Phase 2 |
| Storage | Multiple databases | PostgreSQL only | Expand later |
| Code Examples | Generated examples | Shown in explanations | Phase 1 |

---

## 9. Database Schema (Beginner Version)

```sql
-- Users Table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  username VARCHAR(100),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Code Submissions Table
CREATE TABLE submissions (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  code_snippet TEXT NOT NULL,
  language VARCHAR(50),
  explanation TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  tokens_used INTEGER
);

-- Chat History Table
CREATE TABLE chat_history (
  id SERIAL PRIMARY KEY,
  submission_id INTEGER REFERENCES submissions(id),
  user_message TEXT,
  ai_response TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- User Stats Table
CREATE TABLE user_stats (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  total_submissions INTEGER DEFAULT 0,
  total_explanations INTEGER DEFAULT 0,
  languages_practiced VARCHAR[],
  total_tokens_used INTEGER DEFAULT 0,
  updated_at TIMESTAMP DEFAULT NOW()
);
```

---

## 10. API Endpoints (MVP)

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/me` - Get current user info

### Code Submissions
- `POST /api/submissions` - Submit code for explanation
- `GET /api/submissions` - Get user's submission history
- `GET /api/submissions/:id` - Get specific submission
- `DELETE /api/submissions/:id` - Delete a submission

### Chat
- `GET /api/chat/:submissionId` - Get chat history for a submission
- `POST /api/chat/:submissionId` - Add new message to chat

### Dashboard
- `GET /api/dashboard/stats` - Get user statistics

---

## 10.5 Multi-Language Implementation Strategy

### Supported Languages (MVP Phase 1)

**Tier 1 - Launch with These (Weeks 1-14)**
1. **Python** - Most beginner-friendly, easiest syntax highlighting
2. **JavaScript** - Growing demand, web development relevant
3. **Java** - Enterprise relevance, good for learning OOP
4. **C** - Systems programming, foundational language concepts
5. **C++** - Advanced OOP, competitive programming
6. **HTML** - Web fundamentals, markup language
7. **CSS** - Web styling, design basics
8. **TypeScript** - Modern JavaScript with types

### Why These 8 Languages?
- **Backend Focus:** Python, Java, C, C++, JavaScript
- **Web Focus:** HTML, CSS, TypeScript
- **Breadth:** Covers procedural, OOP, web dev, and systems programming

#### 1. Code Editor Configuration
```javascript
// Use Monaco Editor language options
const languages = {
  python: { id: 'python', extensions: ['.py'] },
  javascript: { id: 'javascript', extensions: ['.js'] },
  java: { id: 'java', extensions: ['.java'] },
  c: { id: 'c', extensions: ['.c'] },
  cpp: { id: 'cpp', extensions: ['.cpp'] },
  html: { id: 'html', extensions: ['.html'] },
  css: { id: 'css', extensions: ['.css'] },
  typescript: { id: 'typescript', extensions: ['.ts'] }
};
```

#### 2. AI Prompt Strategy (Per Language with Examples)
For each language, create specialized system prompts focused on examples:

**Python Prompt:**
```
You are a patient programming tutor explaining Python code to a beginner.
Explain EACH LINE in simple English with real-world examples.
- Use analogies (e.g., "list is like a shopping list")
- Show BEFORE/AFTER examples
- Highlight Python-specific concepts: indentation, list comprehensions, decorators
- Include a simple example of similar code the student could write
```

**JavaScript Prompt:**
```
You are a patient programming tutor explaining JavaScript code to a beginner.
Explain EACH LINE with practical browser examples.
- Explain closures, async/await, this binding with concrete examples
- Show how the code would run in browser console
- Include example output
- Provide a simpler variation they could try
```

**Java Prompt:**
```
You are a patient programming tutor explaining Java code to a beginner.
Explain EACH LINE focusing on OOP concepts.
- Explain classes, objects, inheritance with real-world examples
- Show type safety and exception handling
- Include example of running the code
- Explain use cases for this pattern
```

**C/C++ Prompt:**
```
You are a patient programming tutor explaining C/C++ code to a beginner.
Explain EACH LINE with memory and performance focus.
- Explain pointers, memory management, data types
- Show memory layout with diagrams/ASCII art
- Include example output and memory state
- Explain when to use this approach
```

**HTML/CSS Prompt:**
```
You are a patient programming tutor explaining HTML/CSS code to a beginner.
Explain EACH LINE focusing on visual and structural concepts.
- Explain semantic HTML and CSS selectors
- Show visual result/preview
- Include example of final rendered appearance
- Provide variation they could try
```

**TypeScript Prompt:**
```
You are a patient programming tutor explaining TypeScript code to a beginner.
Explain EACH LINE focusing on type safety benefits.
- Explain type annotations, interfaces, generics
- Show how it prevents errors
- Include example error (and how TypeScript catches it)
- Explain JavaScript equivalent
```

#### 3. Database Tagging
```sql
-- Store language with each submission
ALTER TABLE submissions ADD COLUMN language_id VARCHAR(50);
-- Use: 'python', 'javascript', 'java'
```

#### 4. API Enhancement
```
POST /api/submissions
{
  "code": "const x = 5;",
  "language": "javascript",  // Specify language
  "explanation_depth": "beginner"
}
```

#### 5. Validation Layer
- Detect language from file extension if not specified
- Validate code structure matches language
- Fallback to Claude for unsure cases

### Language-Specific Features for MVP (8 Languages)

#### Python
- Explain indentation, duck typing, decorators
- Show Python shell execution and output
- Highlight list/dict comprehensions
- Examples: loops, functions, classes, string operations

#### JavaScript  
- Explain closures, hoisting, this binding, prototypes
- Show browser console and DOM manipulation
- Include async/await and promises
- Examples: callbacks, event handlers, array methods

#### Java
- Explain classes, inheritance, interfaces, access modifiers
- Show compilation and runtime concepts
- Include exception handling and try-catch
- Examples: constructors, methods, static members, polymorphism

#### C
- Explain pointers, memory allocation (malloc/free), arrays
- Show memory diagrams for addresses and stack/heap
- Include string handling and struct definition
- Examples: function pointers, file I/O, manual memory management

#### C++
- Explain OOP concepts (classes, inheritance, polymorphism)
- Show STL containers (vector, map, set) and algorithms
- Include modern C++ features (smart pointers, lambda expressions)
- Examples: templates, operator overloading, exception handling

#### HTML
- Explain semantic tags (<header>, <main>, <article>) and their meaning
- Show document structure and hierarchy
- Include accessibility attributes (alt text, ARIA labels)
- Examples: forms, meta tags, proper semantic structure

#### CSS
- Explain selectors (class, ID, descendant), specificity, cascade
- Show visual results of styling with descriptions
- Include box model, flexbox, and CSS Grid basics
- Examples: colors, fonts, padding/margin, responsive design

#### TypeScript
- Explain type annotations and their benefits
- Show interfaces, type aliases, and generics
- Include type checking and error prevention
- Examples: classes with types, function signatures, type guards

### Adding More Languages (Phase 2+)

**Tier 2 - Add in Month 4-6:**
- Ruby (expressive, great for web dev)
- Go (concurrency, systems programming)
- Rust (memory safety, performance)

**Tier 3 - Add Later (Month 7+):**
- PHP (server-side web)
- SQL (databases and queries)

### Cost Optimization for Multiple Languages

- Cache common explanations (e.g., "what is a variable" in each language)
- Use shorter prompts for well-known concepts
- Monitor API usage per language
- Consider language-specific rate limits

---

## 11. Success Metrics & KPIs

### User Metrics
- **Sign-ups:** Target 100+ in first month
- **Daily Active Users (DAU):** Target 20+
- **Weekly Active Users (WAU):** Target 40+
- **Monthly Active Users (MAU):** Target 50+
- **Retention:** 40%+ week-over-week retention

### Engagement Metrics
- **Average Session Duration:** 15-30 minutes
- **Submissions per Session:** 2-4 code submissions
- **Chat Messages per Submission:** 3+ follow-up questions
- **Daily Login Rate:** 30%+ of registered users

### Quality Metrics
- **Explanation Satisfaction:** 4.0+/5.0 rating
- **Code Parse Success Rate:** 95%+ successful submissions
- **API Response Time:** Average < 2 seconds
- **System Uptime:** 99%+

### Business Metrics
- **Cost per User:** Track API costs (Claude API spend)
- **Free vs. Premium Conversion:** (Post-MVP) Target 10%
- **User Acquisition Cost:** Track if using ads later

---

## 12. Risk Assessment & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|-----------|
| Claude API costs too high (8 languages) | Budget overrun | High | Implement rate limiting, cache examples, monitor usage per language, optimize prompts |
| Poor explanation quality across 8 languages | User churn | Medium | Extensive prompt engineering per language, test explanations thoroughly, user feedback loop |
| Scope creep with 8 languages | Delayed launch | High | Strict feature scope, defer Phase 2 features, pre-test all language prompts |
| Extended timeline (16 weeks) | Project fatigue | Medium | Break into milestones (auth, editor, API, polish), celebrate small wins |
| Authentication bugs | Security issue | Low | Use established libraries (passport.js), thorough testing, security audit before launch |
| Database performance with multiple languages | Slow queries | Low | Add indexes on language_id, start with small dataset, monitor queries per language |
| Deployment issues | Downtime | Medium | Use CI/CD pipeline, automated tests, staging environment, rollback plan |
| Example generation quality | Low user satisfaction | Medium | Use cached examples, test with users, refine prompts iteratively |

---

## 13. Success Criteria for MVP Launch

**Your MVP will be successful if:**

- [ ] Users can sign up and create accounts
- [ ] Users can submit Python code
- [ ] Claude API provides explanations within 3 seconds
- [ ] Users can see chat history of their sessions
- [ ] Dashboard shows basic stats (total submissions, etc.)
- [ ] No critical bugs on production
- [ ] At least 10 users test and provide feedback
- [ ] Average user session is 10+ minutes
- [ ] Zero data loss or security breaches
- [ ] You have a clear roadmap for Phase 2

---

## 14. Post-Launch Roadmap

### Month 2-3: Phase 2 (Post-MVP)
- Quiz generation system with examples
- Concept tracking and weak areas
- Expand language support (add Ruby, Go, Rust, PHP, SQL)
- Visual flowchart generation with examples
- Bug detection system with corrected examples
- Advanced example generation (real-world use cases)

### Month 4-5: Phase 3 (Growth)
- Premium tier with advanced features
- Bug detection and optimization suggestions
- Batch code submission (analyze entire files)
- Export and sharing features

### Month 6+: Phase 4 (Scale)
- Mobile app (React Native)
- GitHub integration
- Classroom mode for educators
- Marketplace for practice problems

---

## 15. Getting Started Checklist

### Before You Start Coding
- [ ] Create GitHub repository
- [ ] **Design language support strategy** (Start with Python, JavaScript, Java)
- [ ] Design database schema (draw it out, include language column)
- [ ] Create wireframes/mockups (include language selector)
- [ ] Set up development environment locally
- [ ] Create `.env` file for API keys
- [ ] Write a brief tech spec for yourself
- [ ] **Create language-specific system prompts** for Claude API

### As You Develop
- [ ] Commit frequently (at least daily)
- [ ] Write basic unit tests
- [ ] Test authentication flow manually
- [ ] Test API endpoints with Postman/Insomnia
- [ ] Keep a development log

### Before Launch
- [ ] Security audit (check OWASP top 10)
- [ ] Load testing (test with 50+ concurrent users)
- [ ] User acceptance testing with 5+ beta users
- [ ] Set up monitoring and error tracking
- [ ] Create deployment documentation

---

## 16. Appendix: System Prompts Reference

### Prompt Template 1: Line-by-Line Explanation with Examples

**Base Template:**
```
You are a patient programming tutor explaining [LANGUAGE] code to a beginner.
When given code, explain EACH LINE in simple, plain English with concrete examples.

Guidelines:
- Avoid jargon; use real-world analogies
- Explain the PURPOSE of each line
- Provide a real-world example of what the line does
- Show BEFORE/AFTER if applicable
- For functions: briefly explain what it does and when you'd use it
- Include expected output

Format:
Line X: [explanation]
Example: [concrete example]
Output: [what happens]

After all lines, summarize what the code does overall and provide a simple variation the learner could try.
```

### Prompt Template 2: Language-Specific Variations

**Python (Beginner Focus):**
```
Explain this Python code to a complete beginner.
- Use shopping list/cookbook analogies
- Explain indentation as "nesting"
- Show how to run code in Python shell
- Include print() output examples
- Explain Python-specific features like list comprehensions simply
```

**JavaScript (Browser Focus):**
```
Explain this JavaScript code focusing on browser behavior.
- Show how the code runs in browser console
- Include console.log() outputs
- Explain DOM manipulation with visual results
- Use event examples (clicks, page loads)
- Show actual webpage behavior changes
```

**Java (OOP Focus):**
```
Explain this Java code focusing on object-oriented concepts.
- Use class and object analogies (blueprints vs houses)
- Explain why we need classes for this code
- Show inheritance and polymorphism with real examples
- Include compilation and runtime concepts
- Explain type safety benefits
```

**C (Memory Focus):**
```
Explain this C code with memory and performance in mind.
- Draw simple memory diagrams
- Explain pointers with address analogies
- Show stack vs heap concepts
- Include memory output/addresses
- Explain when C is the right choice
```

**HTML/CSS (Visual Focus):**
```
Explain this HTML/CSS code focusing on visual output.
- Describe what appears on the webpage
- Explain semantic HTML tags with meaning examples
- Show CSS selectors with visual matching
- Include screenshot description or ASCII visualization
- Explain accessibility and best practices
```

**TypeScript (Type Safety Focus):**
```
Explain this TypeScript code highlighting type safety.
- Show the equivalent JavaScript without types
- Explain type annotations with examples
- Show errors TypeScript would catch
- Include interface and generic explanations
- Explain when TypeScript helps developers
```

### Prompt Template 3: Follow-up Question Handler
```
The student is learning to code. They ask: "[QUESTION]"
In response to code: "[CODE]"
Language: [LANGUAGE]

Provide a 2-3 sentence answer that:
- Directly answers their question
- Uses beginner-friendly language and examples
- Relates to the specific code they submitted
- Includes a concrete example if applicable
- Encourages them to think deeper (if appropriate)
```

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | July 2026 | Project Team | Initial PRD for CodeMentor AI MVP |

---

**Next Steps:** Approve this PRD and begin tech stack setup and architecture design.
