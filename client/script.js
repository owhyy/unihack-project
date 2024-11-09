const api = "http://localhost:8000";

async function post(endpoint, data) {
    try {
        const response = await fetch(`${api}/${endpoint}`, {
            method: "POST",
            body: JSON.stringify(data),
            headers: {
                "Content-Type": "application/json",
            },
        });
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }

        const json = await response.json();
    } catch (error) {
	console.log(error);
    }
}

