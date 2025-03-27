document.addEventListener("DOMContentLoaded", () => {
    const followButton = document.getElementById("follow-button");
    if (!followButton) return;

    followButton.addEventListener("click", function () {
        const username = followButton.getAttribute("username");
        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

        fetch("/pets/follower", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ username: username })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                followButton.innerText = data.following ? "Unfollow" : "Follow";
                document.getElementById("followers-count").innerText = data.followers;

            } else {
                alert("Error: " + data.error);
            }
        });
    });
});
