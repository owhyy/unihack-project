const api = "https://faithful-primate-divine.ngrok-free.app";
const headers = new Headers({
    "Content-Type": "application/json",
});

if ('access' in localStorage) {
    headers.append("Authorization", `Bearer ${localStorage.access}`);
}

async function get(endpoint) {
    return await fetch(`${api}/${endpoint}`, {
        method: "GET",
        headers: headers,
    });
}

async function post(endpoint, data) {
    return await fetch(`${api}/${endpoint}`, {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json",
        },
    });
}

