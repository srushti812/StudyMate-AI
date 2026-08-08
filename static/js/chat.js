document.getElementById("askBtn").addEventListener("click", async () => {

    const question = document.getElementById("question").value;

    if (question.trim() === "") {
        alert("Please enter your question.");
        return;
    }

    document.getElementById("answer").innerHTML =
        "<b>🤖 Thinking...</b>";

    const response = await fetch("/ask-ai", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            question: question
        })
    });

    const data = await response.json();

    if (data.answer) {
        document.getElementById("answer").innerHTML = `
            <div class="alert alert-success">
                <h5>🤖 AI Answer</h5>
                <p>${data.answer}</p>
            </div>
        `;
    } else {
        document.getElementById("answer").innerHTML = `
            <div class="alert alert-danger">
                ${data.error}
            </div>
        `;
    }
});