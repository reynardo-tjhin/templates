async function fetchUser() {
    try {
        const resp = await fetch("/api/v1/auth/user", {
            method: "GET",
            headers: {
                'Content-Type': 'application/json',
            }
        });
        const res = await resp.json();
        return res.message;

    } catch (error) {
        console.error("Error fetching from '/api/v1/auth': " + error);
    }
}

async function fetchCSRFToken() {
    try {
        const resp = await fetch("/api/v1/auth/csrf-token", {
            method: "GET",
            headers: {
                'Content-Type': 'application/json',
            }
        });
        const res = await resp.json();
        console.log(res.message);

        return res.message;

    } catch (error) {
        console.error("Error fetching from '/api/v1/auth/csrf-token': " + error);
    }
}

document.addEventListener("DOMContentLoaded", async function () {
    try {
        // if signed in, create 
        const user = await fetchUser();
        console.log(user);
        if (user.id !== undefined) {
            document.getElementById("createPost").textContent = "New";
        }

        // get the CSRF token
        const csrfToken = await fetchCSRFToken();

        // load posts
        const postsResp = await fetch("/api/v1/blog/posts", {
            method: "GET",
            headers: {
                'Content-Type': 'application/json',
            }
        });
        const postsRes = await postsResp.json();

        // get current user id
        const userId = user.id;

        // remove loading text
        document.getElementById("loading").innerHTML = "";

        // render the posts
        const postsElement = document.getElementById("posts");
        const posts = postsRes.message;
        posts.forEach((post, index) => {

            const article = document.createElement("article");
            article.classList.add("post");

            const header = document.createElement("header");
            const div = document.createElement("div");

            const title = document.createElement("h1");
            title.textContent = post.title;

            const about = document.createElement("div");
            about.textContent = "by " + post.username + " on " + post.created;

            div.appendChild(title);
            div.appendChild(about);

            header.appendChild(div);

            if (post.author_id === userId) {
                const editButton = document.createElement("a");
                // editButton.id = "editButton";
                editButton.textContent = "Edit";
                editButton.href = "/blog/update/" + post.id;
                editButton.classList.add("action");
                header.appendChild(editButton);

                const deleteForm = document.createElement("form");
                deleteForm.addEventListener("submit", async function (event) {
                    event.preventDefault();

                    const resp = await fetch("/api/v1/blog/posts/" + post.id, {
                        method: "DELETE",
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrfToken,
                        },
                    });
                    const res = await resp.json();
                    console.log(res.message);

                    // return back to home (or refresh the page)
                    window.location.href = "/";
                });

                const deleteCSRFToken = document.createElement("input");
                // deleteCSRFToken.id = "deleteCSRFToken";
                deleteCSRFToken.type = "hidden";
                deleteCSRFToken.name = "csrf_token";
                deleteCSRFToken.value = csrfToken;

                const deleteButton = document.createElement("button");
                deleteButton.type = "submit";
                deleteButton.textContent = "Delete";
                
                deleteForm.appendChild(deleteCSRFToken);
                deleteForm.appendChild(deleteButton);
                header.appendChild(deleteForm);
            }

            const body = document.createElement("p");
            body.textContent = post.body;

            article.appendChild(header);
            article.appendChild(body);

            postsElement.appendChild(article);

            if (index < posts.length - 1) {
                const hr = document.createElement("hr");
                postsElement.appendChild(hr);
            }
        });

    } catch (error) {
        console.error("Error in getting posts: " + error);
    }
});