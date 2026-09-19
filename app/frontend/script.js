const input = document.getElementById("question-input");
const sendButton = document.getElementById("send-button");
const chatMessages = document.getElementById("chat-messages");
const welcomeScreen = document.getElementById("welcome-screen");

const clearButton = document.getElementById("clear-chat");
const newChatButton = document.getElementById("new-chat-button");
const themeToggle = document.getElementById("theme-toggle");

let conversationHistory = [];


// ---------------------------------------------------------
// Theme
// ---------------------------------------------------------

function loadTheme() {
    const savedTheme = localStorage.getItem("medirag-theme");

    if (savedTheme === "dark") {
        document.body.classList.add("dark");
        themeToggle.textContent = "☀";
    } else {
        themeToggle.textContent = "☾";
    }
}


function toggleTheme() {
    document.body.classList.toggle("dark");

    const isDark = document.body.classList.contains("dark");

    localStorage.setItem(
        "medirag-theme",
        isDark ? "dark" : "light"
    );

    themeToggle.textContent = isDark ? "☀" : "☾";
}


themeToggle.addEventListener("click", toggleTheme);

loadTheme();


// ---------------------------------------------------------
// Textarea auto resize
// ---------------------------------------------------------

function resizeTextarea() {
    input.style.height = "auto";

    input.style.height = `${Math.min(
        input.scrollHeight,
        150
    )}px`;
}


input.addEventListener("input", resizeTextarea);


// ---------------------------------------------------------
// Add user message
// ---------------------------------------------------------

function addMessage(message, type) {

    if (welcomeScreen) {
        welcomeScreen.remove();
    }

    const messageWrapper =
        document.createElement("div");

    messageWrapper.className =
        `message ${type}-message`;

    const content =
        document.createElement("div");

    content.className =
        "message-content";

    content.textContent = message;

    messageWrapper.appendChild(content);

    chatMessages.appendChild(
        messageWrapper
    );

    scrollToBottom();
}


// ---------------------------------------------------------
// Add assistant response
// ---------------------------------------------------------

function addAssistantResponse(answer, sources) {

    const messageWrapper =
        document.createElement("div");

    messageWrapper.className =
        "message assistant-message";


    const content =
        document.createElement("div");

    content.className =
        "message-content";


    const answerElement =
        document.createElement("div");

    answerElement.className =
        "assistant-answer";


    answerElement.innerHTML =
        DOMPurify.sanitize(
            marked.parse(answer)
        );


    content.appendChild(
        answerElement
    );


    // Sources
    if (sources && sources.length > 0) {

        const sourcesWrapper =
            document.createElement("div");

        sourcesWrapper.className =
            "sources-wrapper";


        const sourcesTitle =
            document.createElement("div");

        sourcesTitle.className =
            "sources-title";

        sourcesTitle.textContent =
            "📚 Sources";

        sourcesWrapper.appendChild(
            sourcesTitle
        );


        const sourceList =
            document.createElement("ul");

        sourceList.className =
            "source-list";


        sources.forEach((source) => {

            const listItem =
                document.createElement("li");

            listItem.textContent =
                source;

            sourceList.appendChild(
                listItem
            );

        });


        sourcesWrapper.appendChild(
            sourceList
        );

        content.appendChild(
            sourcesWrapper
        );
    }


    // Copy button
    const actions =
        document.createElement("div");

    actions.className =
        "answer-actions";


    const copyButton =
        document.createElement("button");

    copyButton.className =
        "copy-button";

    copyButton.textContent =
        "Copy answer";


    copyButton.addEventListener(
        "click",
        async () => {

            try {

                await navigator.clipboard.writeText(
                    answer
                );

                copyButton.textContent =
                    "Copied ✓";

                setTimeout(() => {
                    copyButton.textContent =
                        "Copy answer";
                }, 1800);

            } catch (error) {

                copyButton.textContent =
                    "Copy failed";

            }

        }
    );


    actions.appendChild(
        copyButton
    );

    content.appendChild(
        actions
    );


    messageWrapper.appendChild(
        content
    );

    chatMessages.appendChild(
        messageWrapper
    );

    scrollToBottom();
}


// ---------------------------------------------------------
// Loading state
// ---------------------------------------------------------

function addLoadingMessage() {

    const messageWrapper =
        document.createElement("div");

    messageWrapper.className =
        "message assistant-message";

    messageWrapper.id =
        "loading-message";


    const content =
        document.createElement("div");

    content.className =
        "message-content loading-message";


    content.innerHTML = `
        <span>MediRAG is thinking</span>

        <span class="typing-dots">
            <span></span>
            <span></span>
            <span></span>
        </span>
    `;


    messageWrapper.appendChild(
        content
    );

    chatMessages.appendChild(
        messageWrapper
    );

    scrollToBottom();
}


function removeLoadingMessage() {

    const loadingMessage =
        document.getElementById(
            "loading-message"
        );

    if (loadingMessage) {
        loadingMessage.remove();
    }
}


// ---------------------------------------------------------
// Scroll
// ---------------------------------------------------------

function scrollToBottom() {

    requestAnimationFrame(() => {

        chatMessages.scrollTo({
            top: chatMessages.scrollHeight,
            behavior: "smooth"
        });

    });
}


// ---------------------------------------------------------
// Send message
// ---------------------------------------------------------

async function sendMessage() {

    const question =
        input.value.trim();


    if (!question) {
        return;
    }


    addMessage(
        question,
        "user"
    );


    input.value = "";
    resizeTextarea();


    sendButton.disabled = true;

    sendButton.innerHTML =
        "•••";


    addLoadingMessage();


    try {

        const response =
            await fetch(
                "/ask",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        question: question,

                        history:
                            conversationHistory
                    })
                }
            );


        if (!response.ok) {

            let errorMessage =
                `Server returned ${response.status}`;

            try {

                const errorData =
                    await response.json();

                if (errorData.detail) {
                    errorMessage =
                        errorData.detail;
                }

            } catch (_) {
                // Ignore JSON parsing errors.
            }

            throw new Error(
                errorMessage
            );
        }


        const data =
            await response.json();


        removeLoadingMessage();


        addAssistantResponse(
            data.answer,
            data.sources
        );


        conversationHistory.push({
            role: "user",
            content: question
        });


        conversationHistory.push({
            role: "assistant",
            content: data.answer
        });


    } catch (error) {

        console.error(
            "API error:",
            error
        );


        removeLoadingMessage();


        addMessage(
            "Sorry, something went wrong while processing your question.",
            "assistant"
        );

    } finally {

        sendButton.disabled = false;

        sendButton.innerHTML =
            "<span>↑</span>";

        input.focus();

    }
}


// ---------------------------------------------------------
// Clear conversation
// ---------------------------------------------------------

function clearConversation() {

    conversationHistory = [];

    chatMessages.innerHTML = "";

    chatMessages.appendChild(
        createWelcomeScreen()
    );

    input.value = "";

    resizeTextarea();

    input.focus();
}


function createWelcomeScreen() {

    const wrapper =
        document.createElement("div");

    wrapper.className =
        "welcome-screen";


    wrapper.innerHTML = `
        <div class="welcome-icon">

            <div class="pulse-ring"></div>

            <div class="medical-symbol">
                ✚
            </div>

        </div>

        <div class="welcome-badge">
            AI • RAG • Medical Knowledge
        </div>

        <h1>
            Your medical knowledge,
            <span>grounded in evidence.</span>
        </h1>

        <p class="welcome-description">
            Ask questions about medical conditions,
            symptoms, prevention and general health
            information.
        </p>

        <div class="suggestion-grid">

            <button
                class="suggestion-card"
                data-question="What are the symptoms of diabetes?"
            >
                <div class="suggestion-icon blue">◉</div>

                <div>
                    <strong>Explore symptoms</strong>
                    <span>What are the symptoms of diabetes?</span>
                </div>

                <span class="suggestion-arrow">→</span>
            </button>

            <button
                class="suggestion-card"
                data-question="What causes diabetes?"
            >
                <div class="suggestion-icon purple">◈</div>

                <div>
                    <strong>Understand causes</strong>
                    <span>What causes diabetes?</span>
                </div>

                <span class="suggestion-arrow">→</span>
            </button>

            <button
                class="suggestion-card"
                data-question="How can diabetes be prevented?"
            >
                <div class="suggestion-icon green">✓</div>

                <div>
                    <strong>Learn prevention</strong>
                    <span>How can diabetes be prevented?</span>
                </div>

                <span class="suggestion-arrow">→</span>
            </button>

            <button
                class="suggestion-card"
                data-question="What is type 2 diabetes?"
            >
                <div class="suggestion-icon orange">?</div>

                <div>
                    <strong>Learn about conditions</strong>
                    <span>What is type 2 diabetes?</span>
                </div>

                <span class="suggestion-arrow">→</span>
            </button>

        </div>
    `;


    attachSuggestionListeners(
        wrapper
    );


    return wrapper;
}


// ---------------------------------------------------------
// Suggested questions
// ---------------------------------------------------------

function attachSuggestionListeners(
    container = document
) {

    const buttons =
        container.querySelectorAll(
            ".suggestion-card"
        );


    buttons.forEach((button) => {

        button.addEventListener(
            "click",
            () => {

                input.value =
                    button.dataset.question;

                resizeTextarea();

                sendMessage();

            }
        );

    });
}


attachSuggestionListeners();


// ---------------------------------------------------------
// New conversation
// ---------------------------------------------------------

newChatButton.addEventListener(
    "click",
    clearConversation
);


clearButton.addEventListener(
    "click",
    clearConversation
);


// ---------------------------------------------------------
// Keyboard shortcuts
// ---------------------------------------------------------

input.addEventListener(
    "keydown",
    (event) => {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendMessage();
        }

    }
);