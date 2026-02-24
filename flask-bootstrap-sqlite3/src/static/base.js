document.addEventListener("DOMContentLoaded", async function () {
    try {
        const resp = await fetch("/api/v1/auth/user", {
            "method": "GET",
            headers: {
                'Content-Type': 'application/json',
            }
        });
        const res = await resp.json();

        console.log(res);

    } catch (error) {
        console.error("Error fetching from '/api/v1/auth': " + error);
    }
})
