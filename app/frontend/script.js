const input = document.getElementById("question-input");
const sendButton = document.getElementById("send-button");
const chatMessages = document.getElementById("chat-messages");

// Store conversation history in the browser
let conversationHistory = [];


function addMessage(message, type) {
    const messageWrapper = document.createElement("div");

    messageWrapper.className = `message ${type}-message`;

    const content = document.createElement("div");

    content.className = "message-content";

    content.textContent = message;

    messageWrapper.appendChild(content);

    chatMessages.appendChild(messageWrapper);

    chatMessages.scrollTop = chatMessages.scrollHeight;
}


function addAssistantResponse(answer, sources) {
    const messageWrapper = document.createElement("div");

    messageWrapper.className = "message assistant-message";

    const content = document.createElement("div");

    content.className = "message-content";


    // Render Markdown safely
    const answerElement = document.createElement("div");

    answerElement.className = "assistant-answer";

    answerElement.innerHTML = DOMPurify.sanitize(
        marked.parse(answer)
    );

    content.appendChild(answerElement);


    // Add sources
    if (sources.length > 0) {
        const sourcesTitle = document.createElement("strong");

        sourcesTitle.className = "sources-title";
        sourcesTitle.textContent = "Sources";

        content.appendChild(sourcesTitle);


        const sourceList = document.createElement("ul");

        sourceList.className = "source-list";


        sources.forEach((source) => {
            const listItem = document.createElement("li");

            listItem.textContent = source;

            sourceList.appendChild(listItem);
        });


        content.appendChild(sourceList);
    }


    messageWrapper.appendChild(content);

    chatMessages.appendChild(messageWrapper);

    chatMessages.scrollTop = chatMessages.scrollHeight;
}


function addLoadingMessage() {
    const messageWrapper = document.createElement("div");

    messageWrapper.className = "message assistant-message";

    messageWrapper.id = "loading-message";


    const content = document.createElement("div");

    content.className = "message-content loading-message";


    content.innerHTML = `
        <span>MediRAG is thinking</span>
        <span class="typing-dots">...</span>
    `;


    messageWrapper.appendChild(content);

    chatMessages.appendChild(messageWrapper);

    chatMessages.scrollTop = chatMessages.scrollHeight;
}


function removeLoadingMessage() {
    const loadingMessage = document.getElementById(
        "loading-message"
    );

    if (loadingMessage) {
        loadingMessage.remove();
    }
}


async function sendMessage() {

    const question = input.value.trim();


    if (!question) {
        return;
    }


    // Display the user's question
    addMessage(question, "user");


    // Clear input
    input.value = "";


    // Disable input while processing
    sendButton.disabled = true;

    sendButton.textContent = "Thinking...";


    // Show loading indicator
    addLoadingMessage();


    try {

        const response = await fetch("/ask", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question,
                history: conversationHistory
            })
        });


        if (!response.ok) {
            throw new Error(
                `Server returned ${response.status}`
            );
        }


        const data = await response.json();


        // Remove loading indicator
        removeLoadingMessage();


        // Display assistant response
        addAssistantResponse(
            data.answer,
            data.sources
        );


        // Store the conversation after successful response
        conversationHistory.push({
            role: "user",
            content: question
        });


        conversationHistory.push({
            role: "assistant",
            content: data.answer
        });


    } catch (error) {

        console.error("API error:", error);


        removeLoadingMessage();


        addMessage(
            "Sorry, something went wrong while processing your question.",
            "assistant"
        );


    } finally {

        sendButton.disabled = false;

        sendButton.textContent = "Send";

        input.focus();
    }
}


// Send button
sendButton.addEventListener(
    "click",
    sendMessage
);


// Enter → send
// Shift + Enter → new line
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