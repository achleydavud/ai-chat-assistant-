const chatBody = document.querySelector(".chat-body");
const messageInput = document.querySelector(".message-input");
const sendMessageButton = document.querySelector("#send-message");
const API_URL = `http://localhost:5000/api/chat`;

// Creating a message element with dynamic classes and returning it
const createMessageElement = (content, ...classes) => {
    const div = document.createElement("div");
    div.classList.add("message", ...classes);
    div.innerHTML = content;
    return div;
}

// Function to generate bot response
const generateBotResponse = async (userMessage) => {
    try {
        // Create a thinking indicator message
        const thinkingContent = `
            <svg class="bot-avatar" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="37" height="31" viewBox="0 0 502 497">
                <!-- here is svg code -->
            </svg>
            <div class="message-text">
                <div class="thinking-indicator">
                    <div class="dot"></div>
                    <div class="dot"></div>
                    <div class="dot"></div>
                </div>
            </div>`;
        
        const thinkingMessageDiv = createMessageElement(thinkingContent, "bot-message", "thinking");
        chatBody.appendChild(thinkingMessageDiv);
        
        // Scroll to the bottom of the chat
        chatBody.scrollTop = chatBody.scrollHeight;
        
        // Send request to Flask backend
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: userMessage }),
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // Parse the JSON response
        const data = await response.json();
        
        // Remove the thinking indicator
        chatBody.removeChild(thinkingMessageDiv);
        
        // Create a new message element for the bot response
        const messageContent = `
            <svg class="bot-avatar" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="37" height="31" viewBox="0 0 502 497">
                <!-- here is svg code -->
            </svg>
            <div class="message-text"></div>`;
        
        const botMessageDiv = createMessageElement(messageContent, "bot-message");
        const botMessageText = botMessageDiv.querySelector(".message-text");
        
        // Add the new message to the chat
        chatBody.appendChild(botMessageDiv);
        
        // Display the response text
        // Display the response text
if (data.response) {
    botMessageText.textContent = data.response;
} else if (data.error) {
    botMessageText.textContent = "Sorry, I encountered an error. Please try again.";
    botMessageDiv.classList.add("error");
} else {
    botMessageText.textContent = "No response received.";
}

        
        // Scroll to the bottom of the chat
        chatBody.scrollTop = chatBody.scrollHeight;
        
    } catch (error) {
        console.error('Error generating bot response:', error);
        
        // Remove thinking indicator if it exists
        const thinkingIndicator = document.querySelector(".bot-message.thinking");
        if (thinkingIndicator) {
            chatBody.removeChild(thinkingIndicator);
        }
        
        // Show error message
        const errorContent = `
            <svg class="bot-avatar" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="37" height="31" viewBox="0 0 502 497">
                <!-- here is svg code -->
            </svg>
            <div class="message-text">Sorry, I couldn't process your request. Please try again later.</div>`;
        
        const errorMessageDiv = createMessageElement(errorContent, "bot-message", "error");
        chatBody.appendChild(errorMessageDiv);
        
        // Scroll to the bottom of the chat
        chatBody.scrollTop = chatBody.scrollHeight;
    }
}

// Handling outgoing user message
const handleOutGoingMessage = (e) => {
    // Preventing form from submitting
    e.preventDefault();
    
    // Storing the user's message
    const userMessage = messageInput.value.trim();
    
    // Don't proceed if message is empty
    if (!userMessage) return;
    
    // Clear input field
    messageInput.value = "";
    
    // Create and display user message
    const messageContent = `<div class="message-text"></div>`;
    const outgoingMessageDiv = createMessageElement(messageContent, "user-message");
    outgoingMessageDiv.querySelector(".message-text").innerText = userMessage;
    chatBody.appendChild(outgoingMessageDiv);
    
    // Scroll to the bottom of the chat
    chatBody.scrollTop = chatBody.scrollHeight;
    
    // Generate bot response
    generateBotResponse(userMessage);
}

// Handle Enter key press to send message
messageInput.addEventListener("keydown", (e) => {
    const userMessage = e.target.value.trim();
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        if (userMessage) {
            handleOutGoingMessage(e);
        }
    }
});

// Handle send button click
sendMessageButton.addEventListener("click", (e) => handleOutGoingMessage(e));
