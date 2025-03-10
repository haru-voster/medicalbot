document.addEventListener("DOMContentLoaded", function () {
    const chatbox = document.getElementById("chatbox");
    const userInput = document.getElementById("userInput");

    // Function to append messages in styled format
    function appendMessage(sender, message, isBot = false) {
        const msgDiv = document.createElement("div");
        msgDiv.classList.add("message", isBot ? "bot" : "user");
        msgDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
        chatbox.appendChild(msgDiv);
        chatbox.scrollTop = chatbox.scrollHeight; // Auto-scroll to latest message
    }

    window.sendMessage = async function () {
        const message = userInput.value.trim();
        if (!message) return;

        appendMessage("You", message, false); // Append user message (Green, Right)

        try {
            const response = await fetch("http://127.0.0.1:5000/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message }),
            });

            if (!response.ok) throw new Error(`Server error: ${response.status}`);

            const data = await response.json();
            appendMessage("Bot", data.response, true); // Append bot message (Blue, Left)

        } catch (error) {
            console.error("Fetch error:", error);
            appendMessage("Error", "Could not connect to chatbot.", true);
        }

        userInput.value = ""; // Clear input field
    };
});
