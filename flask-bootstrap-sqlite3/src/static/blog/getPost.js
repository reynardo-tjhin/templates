document.addEventListener("DOMContentLoaded", async function () {
    try {
        // get the post id
        const pathName = window.location.pathname;
        const postId = pathName.split("/").at(-1);

        // get response
        const resp = await fetch("/api/v1/blog/posts/" + postId, {
            method: "GET",
            headers: {
                'Content-Type': 'application/json',
            }
        });
        const res = await resp.json();

        // assign to the front end's element
        document.getElementById("title").value = res.message.title;
        document.getElementById("body").textContent = res.message.body;

    } catch (error) {
        console.error("Error from API '/api/v1/blog/posts': " + error);
    }
});