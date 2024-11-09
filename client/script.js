const api = "https://faithful-primate-divine.ngrok-free.app";

async function post(endpoint, data) {
    return await fetch(`${api}/${endpoint}`, {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json",
        },
    });
}

