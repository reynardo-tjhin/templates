document.getElementById("signInForm").addEventListener('submit', async function (event) {
    event.preventDefault(); // prevent from normal submission

    // disable submit button to prevent double submission
    document.getElementById("signInButton").disabled = true;

    // get the sign in details
    const form = event.target;
    const formData = new FormData(form);
    var obj = {};
    formData.forEach(function (value, key) {
        obj[key] = value;
    });
    const json = JSON.stringify(obj);

    // perform an async request
    try {
        const url = '/api/v1/auth/login';
        const csrfToken = document.getElementById("signInCSRFToken").value;
        const response = await fetch(url, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: json,
        });
        const result = await response.json();

        if (result['status'] === "error") {
            // show error
            document.getElementById("signInErrorContainer").classList.remove("d-none");
            document.getElementById("signInErrorSpan").textContent = "ERROR: " + result["message"];

            // re-enable sign in button
            document.getElementById("signInButton").disabled = false;

        } else if (result['status'] === 'success') {
            // show success message
            document.getElementById("signInErrorContainer").classList.remove("d-none");
            document.getElementById("signInErrorContainer").classList.remove("border-danger");
            document.getElementById("signInErrorContainer").classList.add("border-success");
            document.getElementById("signInErrorSpan").textContent = result["message"];

            // pause a bit
            setTimeout(() => {
                // redirect to the homepage
                window.location.href = '/';
            }, 750); // 0.75 seconds delay to show success

        } else {
            console.error("Error from server");
        }

    } catch (error) {
        console.error("AJAX Error: " + error);
    };
});