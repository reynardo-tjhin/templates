document.addEventListener("DOMContentLoaded", async function () {
    try {
        const resp = await fetch("/api/v1/auth/user", {
            method: "GET",
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
            // user is logged in
            else if (res['message']['username'] !== null) {
                document.getElementById("sign-up-sign-in-btn").classList.add("d-none"); // hide sign up/sign in button
                document.getElementById("account-btn").classList.remove("d-none"); // show account button
                document.getElementById("accountName").textContent = res["message"]['username'];
            }

        // error finding the user based on the id from the database
        } else if (res['status'] === 'error') {
            console.error("ERROR: Could not find the user from the database");
            console.error("ERROR: Database might be corrupted");

        // unexpected error
        } else {
            console.error("Error fetching from '/api/v1/auth': unknown status - " + res['status']);
        }

    } catch (error) {
        console.error("Error fetching from '/api/v1/auth': " + error);
    }
})
