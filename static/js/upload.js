document.getElementById("uploadForm").addEventListener("submit", async function(e){

    e.preventDefault();

    const file = document.getElementById("pdf").files[0];

    if(!file){
        alert("Please select a PDF.");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    document.getElementById("result").innerHTML = `
        <div class="alert alert-info">
            🤖 Generating AI Summary...
        </div>
    `;

    const response = await fetch("/upload-pdf", {
        method: "POST",
        body: formData
    });

    const data = await response.json();
    console.log(data);
    console.log(data.overview);
    console.log(data.important_points);
    console.log(data.technologies);
    console.log(data.key_takeaways);

    if(data.error){
        document.getElementById("result").innerHTML = `
            <div class="alert alert-danger">
                ${data.error}
            </div>
        `;
        return;
    }

    let html = `
    <div class="alert alert-success">

        <h4>✅ PDF Uploaded Successfully</h4>

        <p><strong>File:</strong> ${data.filename}</p>

        <hr>

        <h5>📘 Overview</h5>
    `;

    data.overview.forEach(line => {
        html += `<p>${line}</p>`;
    });

    html += `<hr>`;

    html += `<h5>📌 Important Points</h5><ul>`;

    data.important_points.forEach(point => {
        html += `<li>${point}</li>`;
    });

    html += `</ul><hr>`;

    html += `<h5>🛠 Technologies</h5><ul>`;

    data.technologies.forEach(tech => {
        html += `<li>${tech}</li>`;
    });

    html += `</ul><hr>`;

    html += `<h5>🎯 Key Takeaways</h5><ul>`;

    data.key_takeaways.forEach(point => {
        html += `<li>${point}</li>`;
    });

    html += `</ul>

    <hr>

    <a href="/chat" class="btn btn-primary me-2">
        💬 Ask AI
    </a>

    <a href="/quiz" class="btn btn-success">
        📝 Generate Quiz
    </a>

    </div>`;

    document.getElementById("result").innerHTML = html;

});