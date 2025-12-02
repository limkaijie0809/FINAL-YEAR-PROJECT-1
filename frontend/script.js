const startBtn = document.getElementById("startBtn");
const questionArea = document.getElementById("questionArea");

startBtn.addEventListener("click", async () => {
    try {
        // Call your Flask API
        const response = await fetch("http://127.0.0.1:5000/api/start-training");
        const data = await response.json();

        console.log("Received from backend:", data);

        // Show question on page
        questionArea.innerHTML = `
            <h2>Email Subject: ${data.email_subject}</h2>
            <p>${data.email_body}</p>
            <p><strong>(This is just a sample question)</strong></p>
        `;
    } catch (error) {
        console.error("Error fetching data:", error);
        questionArea.innerHTML = "<p>Failed to load question.</p>";
    }
});
