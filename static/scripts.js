document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("player-form");
    let intervalId = null;

    form.addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent form submission from reloading the page

        const platform = document.getElementById("platform").value;
        const username = document.getElementById("username").value;

        // Start polling for updates
        if (intervalId) {
            clearInterval(intervalId);
        }
        fetchAndUpdateProfile(platform, username); // Fetch immediately
        intervalId = setInterval(() => fetchAndUpdateProfile(platform, username), 30000); // Fetch every 30 seconds
    });

    function fetchAndUpdateProfile(platform, username) {
        fetch(`http://localhost:5000/warzone/${platform}/${username}`)
            .then(response => response.json())
            .then(data => {
                if (!data.error) {
                    document.getElementById("activision-id").textContent = data.username;
                    document.getElementById("kd-ratio").textContent = data.lifetime.mode.br.properties.kdRatio.toFixed(2);
                    document.getElementById("wins").textContent = data.lifetime.mode.br.properties.wins;
                    document.getElementById("win-streak").textContent = data.lifetime.mode.br.properties.winStreak;
                    document.getElementById("player-info").style.display = "block"; // Show the player info
                } else {
                    document.getElementById("player-info").style.display = "none";
                    alert("Error fetching data: " + data.error);
                }
            })
            .catch(error => {
                document.getElementById("player-info").style.display = "none";
                alert("Error fetching data.");
                console.error("Error:", error);
            });
    }
});
