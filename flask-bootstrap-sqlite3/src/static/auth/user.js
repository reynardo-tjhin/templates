document.addEventListener("DOMContentLoaded", async function () {
    try {
        const resp = await fetch("/api/v1/auth/user", {
            "method": "GET",
            headers: {
                'Content-Type': 'application/json',
            }
        });
        const res = await resp.json();

        if (res['status'] === 'success') {
            // user is not logged in
            if (res['message'] === 'user has not logged in') {
                document.getElementById("sign-up-sign-in-btn").classList.remove("d-none"); // show sign up/sign in button
                document.getElementById("account-btn").classList.add("d-none"); // hide account button
            }

        } else if (res['status'] === 'error') {

        } else {
            console.error("Error fetching from '/api/v1/auth': unknown status - " + res['status']);
        }

    } catch (error) {
        console.error("Error fetching from '/api/v1/auth': " + error);
    }
})
