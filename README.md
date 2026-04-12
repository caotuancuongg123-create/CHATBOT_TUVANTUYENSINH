function send() {
    const inputBox = document.getElementById("input");
    const input = inputBox.value.trim();

    if (!input) return;

    addMessage(input, "user");
    inputBox.value = "";

    fetch("/chat", {
        method: "POST",
        headers: { 
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: input })
    })
    .then(res => res.json())
    .then(data => {
        addMessage(data.response, "bot");
    })
    .catch(() => {
        addMessage("❌ Lỗi server", "bot");
    });
} 
