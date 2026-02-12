document.addEventListener("DOMContentLoaded", () => {

    const checkBtn = document.getElementById("checkEnvironment");
    const passwordBox = document.getElementById("passwordBox");
    const revealedPassword = document.getElementById("revealedPassword");
    const resultBox = document.getElementById("resultBox");

    checkBtn.addEventListener("click", async () => {

        const environmentData = {
            client_date: new Date().toISOString(),
            language: navigator.language,
            viewport_width: window.innerWidth
        };

        const res = await fetch("/game/level/1/environment", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(environmentData)
        });

        const data = await res.json();

        if (!data.success) {
            resultBox.textContent = data.message;
            return;
        }

        passwordBox.style.display = "block";
        revealedPassword.textContent = data.password;
    });

});
