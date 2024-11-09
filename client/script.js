const api = "https://156a-85-120-207-252.ngrok-free.app";

async function post(endpoint, data) {
    return await fetch(`${api}/${endpoint}`, {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json",
        },
    });
}

