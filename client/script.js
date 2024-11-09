const api = "http://localhost:8000";

async function post(endpoint, data) {
    return await fetch(`${api}/${endpoint}`, {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json",
        },
    });
}

