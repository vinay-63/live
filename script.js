const socket = new WebSocket("ws://localhost:8000/ws/score");

socket.onmessage = (event) => {
    try {
        const data = JSON.parse(event.data);
        document.getElementById("teamA-score").textContent = data.teamA;
        document.getElementById("teamB-score").textContent = data.teamB;

        const updatesList = document.getElementById("updates-list");
        const newItem = document.createElement("li");
        newItem.textContent = `Update: ${data.teamA} vs ${data.teamB}`;
        updatesList.prepend(newItem);
    } catch {
        console.log("Non-JSON message:", event.data);
    }
};
