document.getElementById("createPostForm").addEventListener('submit', async function (event) {
    event.preventDefault(); // prevent from normal submission

    // disable submit button to prevent double submission
    document.getElementById("createPostButton").disabled = true;

    // both create a new post and update a new post in the same HTML document
    let method; // initialise - will return undefined
    let postId; // initialise - will return undefined
    if (window.location.pathname.includes("update")) {
        method = "PUT";
        postId = "/" + window.location.pathname.split("/").at(-1);
    } else {
        method = "POST";
        postId = "";
    }

    // get the post details
    const form = event.target;
    const formData = new FormData(form);
    
    // turn it into JSON string
    const obj = {};
    formData.forEach((value, key) => {
        obj[key] = value;
    });
    const json = JSON.stringify(obj);

    // perform an async request
    try {
        const csrfToken = document.getElementById("createPostCSRFToken").value;
        console.log(csrfToken);

        const resp = await fetch("/api/v1/blog/posts" + postId, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: json,
        });
        const res = await resp.json();

        console.log(res);
        if (res.message === 'successfully added a new post') {
            window.location.href = '/';
        } else if (res.message === 'successfully updated the post with a new title and body') {
            window.location.href = '/';
        }

    } catch (error) {
        console.error("Error in '': " + error);
    }
});