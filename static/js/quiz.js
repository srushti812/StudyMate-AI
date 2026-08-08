let quizData = [];
let timerInterval;


// ========================================
// Generate Quiz
// ========================================

document.getElementById("generateBtn").addEventListener("click", async function () {

    const generateBtn = document.getElementById("generateBtn");

    try {

        // Disable button while generating
        generateBtn.disabled = true;
        generateBtn.innerText = "Generating...";

        document.getElementById("quizContainer").innerHTML = `
            <div class="alert alert-info">
                🤖 AI is generating your quiz...
            </div>
        `;

        document.getElementById("result").innerHTML = "";


        const response = await fetch("/generate-quiz", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                pdf_text: ""
            })
        });


        const data = await response.json();

        console.log("Generate Quiz Response:", data);


        // Check backend error
        if (data.error) {
            throw new Error(data.error);
        }


        // Check quiz data
        if (!data.quiz) {
            throw new Error("Quiz data was not received from the server.");
        }


        // Convert JSON string into object if required
        const quiz = typeof data.quiz === "string"
            ? JSON.parse(data.quiz)
            : data.quiz;


        // Check questions
        if (!quiz.questions || quiz.questions.length === 0) {
            throw new Error("No questions were generated.");
        }


        // Store questions
        quizData = quiz.questions;


        // Display questions
        displayQuiz(quizData);


        // Start dynamic timer
        startTimer(quizData.length);


    } catch (error) {

        console.error("Quiz Error:", error);


        document.getElementById("quizContainer").innerHTML = `
            <div class="alert alert-danger">

                <strong>Error generating quiz:</strong>

                <br><br>

                ${error.message}

            </div>
        `;

    } finally {

        generateBtn.disabled = false;
        generateBtn.innerText = "Generate Quiz";

    }

});



// ========================================
// Display Quiz Questions
// ========================================

function displayQuiz(questions) {

    let html = "";


    questions.forEach((q, index) => {

        html += `

            <div
                class="card mb-3 p-3 shadow-sm"
                id="question-card-${index}"
            >

                <h5>
                    ${index + 1}. ${q.question}
                </h5>


                ${q.options.map(option => `

                    <div class="form-check mt-2">

                        <input
                            class="form-check-input"
                            type="radio"
                            name="q${index}"
                            value="${escapeHTML(option)}"
                            id="q${index}_${escapeHTML(option)}"
                        >

                        <label
                            class="form-check-label"
                            for="q${index}_${escapeHTML(option)}"
                        >
                            ${option}
                        </label>

                    </div>

                `).join("")}


                <!-- Correct answer will appear here after submission -->

                <div
                    id="feedback-${index}"
                    class="mt-3"
                ></div>

            </div>

        `;

    });


    document.getElementById("quizContainer").innerHTML = html;

}



// ========================================
// Dynamic Timer
// ========================================

function startTimer(questionCount) {

    // Stop previous timer
    clearInterval(timerInterval);


    // 1 minute per question + 5 minutes extra
    let totalSeconds = (questionCount * 60) + 300;


    const timer = document.getElementById("timer");


    // Display immediately
    updateTimerDisplay(timer, totalSeconds);


    timerInterval = setInterval(function () {

        totalSeconds--;


        updateTimerDisplay(timer, totalSeconds);


        if (totalSeconds <= 0) {

            clearInterval(timerInterval);


            alert("Time is over!");


            document.getElementById("quizForm").requestSubmit();

        }

    }, 1000);

}



// ========================================
// Timer Display
// ========================================

function updateTimerDisplay(timer, totalSeconds) {

    if (totalSeconds < 0) {
        totalSeconds = 0;
    }


    const minutes = Math.floor(totalSeconds / 60);

    const seconds = totalSeconds % 60;


    timer.innerHTML =
        `Time Left: ${minutes}:${seconds.toString().padStart(2, "0")}`;

}



// ========================================
// Submit Quiz
// ========================================

document.getElementById("quizForm")
    .addEventListener("submit", function (e) {

        e.preventDefault();


        // Stop timer
        clearInterval(timerInterval);


        let score = 0;

        let resultHTML = "";


        quizData.forEach((q, index) => {

            const selected = document.querySelector(
                `input[name="q${index}"]:checked`
            );


            const selectedAnswer = selected
                ? selected.value
                : "Not answered";


            const correctAnswer = q.answer;


            const questionCard =
                document.getElementById(`question-card-${index}`);


            const feedback =
                document.getElementById(`feedback-${index}`);


            // ========================================
            // Correct Answer
            // ========================================

            if (selectedAnswer === correctAnswer) {

                score++;


                questionCard.classList.add("border-success");


                feedback.innerHTML = `

                    <div class="alert alert-success mb-0">

                        <strong>
                            ✅ Correct Answer
                        </strong>

                        <br>

                        Your Answer:
                        <strong>${selectedAnswer}</strong>

                    </div>

                `;

            }


            // ========================================
            // Wrong Answer
            // ========================================

            else {

                questionCard.classList.add("border-danger");


                feedback.innerHTML = `

                    <div class="alert alert-danger mb-0">

                        <strong>
                            ❌ Wrong Answer
                        </strong>

                        <br>

                        Your Answer:
                        <strong>${selectedAnswer}</strong>

                        <br>

                        Correct Answer:
                        <strong>${correctAnswer}</strong>

                    </div>

                `;

            }

        });


        // ========================================
        // Final Score
        // ========================================

        const percentage =
            quizData.length > 0
                ? Math.round((score / quizData.length) * 100)
                : 0;


        resultHTML = `

            <div class="alert alert-primary text-center">

                <h3>
                    🎉 Quiz Completed
                </h3>

                <h4>
                    Score: ${score} / ${quizData.length}
                </h4>

                <h5>
                    Percentage: ${percentage}%
                </h5>

            </div>

        `;


        document.getElementById("result").innerHTML = resultHTML;


        // ========================================
        // Disable all answers
        // ========================================

        document
            .querySelectorAll("#quizForm input")
            .forEach(function (input) {

                input.disabled = true;

            });


        // Disable submit button
        const submitButton =
            document.querySelector(
                '#quizForm button[type="submit"]'
            );


        if (submitButton) {

            submitButton.disabled = true;
            submitButton.innerText = "Quiz Submitted";

        }


        // Scroll to result
        document.getElementById("result")
            .scrollIntoView({
                behavior: "smooth"
            });

    });



// ========================================
// Escape HTML
// ========================================

function escapeHTML(text) {

    const div = document.createElement("div");

    div.textContent = text;

    return div.innerHTML;

}