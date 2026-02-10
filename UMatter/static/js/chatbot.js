/**
 * UMatter Guide Chatbot
 * Empathetic AI assistant for mental wellness platform
 * Theme: Virasat se Vikas Tak (Heritage to Progress)
 */

class UMatterChatbot {
    constructor() {
        this.isOpen = false;
        this.messages = [];
        this.currentPage = this.detectCurrentPage();

        this.init();
    }

    init() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setup());
        } else {
            this.setup();
        }
    }

    setup() {
        this.createChatbotHTML();
        this.attachEventListeners();
        this.loadConversationHistory();
        this.sendWelcomeMessage();
    }

    createChatbotHTML() {
        const chatbotHTML = `
            <button class="chatbot-toggle" id="chatbot-toggle" aria-label="Open UMatter Guide">
                <span class="chatbot-toggle-icon">🧘</span>
            </button>
            <div class="chatbot-window" id="chatbot-window">
                <div class="chatbot-header">
                    <div class="chatbot-header-content">
                        <div class="chatbot-avatar">🧘</div>
                        <div class="chatbot-title">
                            <h4 class="chatbot-name">UMatter Guide</h4>
                            <div class="chatbot-status">
                                <span class="status-dot"></span>
                                <span>Here to support you</span>
                            </div>
                        </div>
                    </div>
                    <button class="chatbot-close" id="chatbot-close" aria-label="Close chat">×</button>
                </div>
                <div class="chatbot-messages" id="chatbot-messages"></div>
                <div class="typing-indicator" id="typing-indicator">
                    <div class="message-avatar">🧘</div>
                    <div class="typing-dots">
                        <span class="typing-dot"></span>
                        <span class="typing-dot"></span>
                        <span class="typing-dot"></span>
                    </div>
                </div>
                <div class="chatbot-input-area">
                    <input type="text" class="chatbot-input" id="chatbot-input" placeholder="Type your message..." aria-label="Chat message input">
                    <button class="chatbot-send" id="chatbot-send" aria-label="Send message">→</button>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', chatbotHTML);
    }

    attachEventListeners() {
        const toggle = document.getElementById('chatbot-toggle');
        const close = document.getElementById('chatbot-close');
        const send = document.getElementById('chatbot-send');
        const input = document.getElementById('chatbot-input');

        toggle.addEventListener('click', () => this.toggleChat());
        close.addEventListener('click', () => this.toggleChat());
        send.addEventListener('click', () => this.sendMessage());
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });

        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('quick-action-btn')) {
                const action = e.target.dataset.action;
                // If action is a direct link, navigate immediately
                if (action.startsWith('/')) {
                    window.location.href = action;
                } else {
                    this.handleQuickAction(action);
                }
            }
        });
    }

    toggleChat() {
        this.isOpen = !this.isOpen;
        const window = document.getElementById('chatbot-window');
        const toggle = document.getElementById('chatbot-toggle');

        if (this.isOpen) {
            window.classList.add('active');
            toggle.classList.add('active');
            document.getElementById('chatbot-input').focus();
        } else {
            window.classList.remove('active');
            toggle.classList.remove('active');
        }
    }

    sendMessage() {
        const input = document.getElementById('chatbot-input');
        const message = input.value.trim();
        if (!message) return;

        this.addMessage('user', message);
        input.value = '';
        this.showTyping();

        setTimeout(() => {
            const response = this.getBotResponse(message);
            this.hideTyping();
            this.addMessage('bot', response.text, response.quickActions);

            // Execute navigation if present
            if (response.navigate) {
                setTimeout(() => {
                    window.location.href = response.navigate;
                }, 1500);
            }
        }, 800 + Math.random() * 800);
    }

    addMessage(sender, text, quickActions = null) {
        const container = document.getElementById('chatbot-messages');
        const messageHTML = `
            <div class="message ${sender}">
                <div class="message-avatar">${sender === 'bot' ? '🧘' : '👤'}</div>
                <div class="message-bubble">
                    <div class="message-content">${text}</div>
                    ${quickActions ? this.createQuickActions(quickActions) : ''}
                </div>
            </div>
        `;
        container.insertAdjacentHTML('beforeend', messageHTML);
        container.scrollTop = container.scrollHeight;
        this.messages.push({ sender, text, time: new Date().toISOString() });
        this.saveConversationHistory();
    }

    createQuickActions(actions) {
        return `<div class="quick-actions">
            ${actions.map(a => `<button class="quick-action-btn" data-action="${a.value}">${a.label}</button>`).join('')}
        </div>`;
    }

    handleQuickAction(action) {
        const input = document.getElementById('chatbot-input');
        const actionMap = {
            'take-assessment': 'I want to take the assessment',
            'view-progress': 'Show me my progress',
            'self-care': 'I need self-care tips',
            'breathing': 'Teach me a breathing exercise'
        };

        if (actionMap[action]) {
            input.value = actionMap[action];
            this.sendMessage();
        }
    }

    // ------------------------------------------------------------------------
    // CORE LOGIC: Responses & Navigation
    // ------------------------------------------------------------------------

    getBotResponse(userMessage) {
        const msg = userMessage.toLowerCase();

        // 1. Navigation Commands
        if (msg.includes('assessment') || msg.includes('test') || msg.includes('quiz')) {
            if (msg.includes('take') || msg.includes('start') || msg.includes('open') || msg.includes('go to')) {
                return {
                    text: "Opening the Trauma Assessment for you... 📋",
                    navigate: '/questions/',
                    quickActions: null
                };
            }
        }

        if (msg.includes('self care') || msg.includes('selfcare') || msg.includes('tips')) {
            if (msg.includes('open') || msg.includes('go to') || msg.includes('show')) {
                return {
                    text: "Taking you to the Self-Care section... 🧘",
                    navigate: '/selfcare/',
                    quickActions: null
                };
            }
        }

        if (msg.includes('progress') || msg.includes('track') || msg.includes('stats')) {
            if (msg.includes('open') || msg.includes('go to') || msg.includes('view') || msg.includes('show')) {
                return {
                    text: "Opening your Progress Tracker... 📊",
                    navigate: '/progress/', /* Assuming this URL, adjust if needed */
                    quickActions: null
                };
            }
        }

        // 2. Crisis Detection
        if (this.detectCrisis(msg)) {
            return {
                text: "I hear your pain. Please reach out to a professional or someone you trust. \n\n🆘 KIRAN Helpline: 1800-599-0019 (24/7)",
                quickActions: null
            };
        }

        // 3. Information & Support (Short, Context-Specific)

        // Greetings
        if (this.matchesIntent(msg, ['hi', 'hello', 'hey', 'namaste'])) {
            return {
                text: "Namaste! 🙏 I'm your wellness guide. How are you feeling right now?",
                quickActions: [
                    { label: 'Stress', value: 'I am stressed' },
                    { label: 'Anxiety', value: 'I feel anxious' },
                    { label: 'Just passing by', value: 'Just exploring' }
                ]
            };
        }

        // Stress/Anxiety
        if (this.matchesIntent(msg, ['stress', 'anxious', 'worried', 'overwhelmed'])) {
            return {
                text: "It's okay to feel this way. Let's take a moment. Would you like a quick breathing exercise?",
                quickActions: [
                    { label: 'Yes, breathe', value: 'breathing' },
                    { label: 'No, talk more', value: 'I want to talk' }
                ]
            };
        }

        // Breathing
        if (this.matchesIntent(msg, ['breath', 'breathe', 'pranayama'])) {
            return {
                text: "Inhale slowly (4s)... Hold (4s)... Exhale (6s). \nFocus only on your breath. Repeat this 3 times.",
                quickActions: [
                    { label: 'Feeling better', value: 'I feel better' },
                    { label: 'Still anxious', value: 'Still anxious' }
                ]
            };
        }

        // Trauma Explanations (Short)
        if (msg.includes('family trauma')) {
            return {
                text: "Family trauma stems from conflicts, loss, or deep-rooted emotional gaps within the home. It often affects how we connect with others.",
                quickActions: [{ label: 'Check my pattern', value: 'take-assessment' }]
            };
        }

        if (msg.includes('financial')) {
            return {
                text: "Financial stress isn't just about money—it's about security. It can cause constant low-grade anxiety affecting sleep and focus.",
                quickActions: [{ label: 'Check my pattern', value: 'take-assessment' }]
            };
        }

        if (msg.includes('career') || msg.includes('work')) {
            return {
                text: "Career anxiety often comes from pressure to perform or fear of failure. Remember: Your worth is more than your productivity.",
                quickActions: [{ label: 'Check my pattern', value: 'take-assessment' }]
            };
        }

        // Default / Confusion
        return {
            text: "I'm here to listen. You can ask me to open pages like 'Assessment' or 'Self Care', or tell me how you're feeling.",
            quickActions: [
                { label: 'Take Assessment', value: '/questions/' }, /* Direct link action */
                { label: 'Self Care Tips', value: '/selfcare/' }
            ]
        };
    }

    matchesIntent(message, keywords) {
        return keywords.some(keyword => message.includes(keyword));
    }

    detectCrisis(message) {
        const crisisKeywords = ['suicide', 'kill myself', 'die', 'end it', 'no point'];
        return crisisKeywords.some(k => message.includes(k));
    }

    detectCurrentPage() {
        const path = window.location.pathname;
        if (path.includes('questions')) return 'assessment';
        if (path.includes('progress')) return 'progress';
        if (path.includes('selfcare')) return 'selfcare';
        return 'home';
    }

    sendWelcomeMessage() {
        if (this.messages.length > 0) return;

        const welcomeText = {
            'home': "Welcome to UMatter. 🙏 How can I support your wellness today?",
            'assessment': "This assessment helps us understand your needs. Take your time.",
            'progress': "Here is your journey so far. Consistency is key!",
            'selfcare': "Explore these heritage-inspired practices for peace."
        };

        const text = welcomeText[this.currentPage] || welcomeText['home'];

        setTimeout(() => {
            this.addMessage('bot', text, [
                { label: 'Take Assessment', value: 'take-assessment' },
                { label: 'Self Care', value: 'self-care' }
            ]);
        }, 1000);
    }

    showTyping() {
        document.getElementById('typing-indicator').classList.add('active');
        const container = document.getElementById('chatbot-messages');
        container.scrollTop = container.scrollHeight;
    }

    hideTyping() {
        document.getElementById('typing-indicator').classList.remove('active');
    }

    saveConversationHistory() {
        try { localStorage.setItem('umatter_chat_history', JSON.stringify(this.messages)); } catch (e) { }
    }

    loadConversationHistory() {
        try {
            const history = localStorage.getItem('umatter_chat_history');
            if (history) {
                this.messages = JSON.parse(history);
                this.messages.slice(-5).forEach(m => this.addMessage(m.sender, m.text)); // Load last 5 only
            }
        } catch (e) { }
    }
}

const umatterChatbot = new UMatterChatbot();
