document.getElementById("signUpForm").addEventListener('submit', async function (event) {
    event.preventDefault(); // prevent form normal form submission

    // disable submit button
    const submitButton = document.getElementById("signUpButton");
    submitButton.disabled = true;

    // get form data and parse into JSON format
    const form = event.target;
    const formData = new FormData(form);
    const obj = Object.fromEntries(formData);
    const json = JSON.stringify(obj);

    try {
        const url = '/api/v1/auth/register';
        const csrfToken = document.getElementById("signUpCSRFToken").value;
        const response = await fetch(url, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: json,
        });
        // response statuses return: success and unexpected error
        const result = await response.json();

        // response statuses return: 400 and 404
        if (!response.ok) {

            // show error
            document.getElementById("signUpErrorContainer").classList.remove("d-none");
            document.getElementById("signUpErrorSpan").textContent = "ERROR: " + result["message"];

            return; // early return so execution stops here
        }

        // response status returns 200 (or ok)
        if (result['status'] === 'success') {

            // show success message
            document.getElementById("signUpErrorContainer").classList.remove("d-none");
            document.getElementById("signUpErrorContainer").classList.remove("border-danger");
            document.getElementById("signUpErrorContainer").classList.add("border-success");
            document.getElementById("signUpErrorSpan").textContent = result["message"];

            // pause a bit
            setTimeout(() => {
                // redirect to the homepage
                window.location.href = '/auth/login';
            }, 750); // 0.75 seconds delay to show success

        } else {

            // error from the server
            // result['status'] is not returning 'success'
            console.error("Error from server");
            document.getElementById("signUpErrorContainer").classList.remove("d-none");
            document.getElementById("signUpErrorSpan").textContent = "An error occurred. Please contact administrator.";

            // re-enable the submit button
            submitButton.disabled = false;
        }

    } catch (error) {

        // show error
        console.error("AJAX Error: " + error);
        document.getElementById("signUpErrorContainer").classList.remove("d-none");
        document.getElementById("signUpErrorSpan").textContent = "A network error occurred. Please try again.";
    }
});