let heartButtons = document.querySelectorAll(".heart-button");

heartButtons.forEach((button) => {
    button.addEventListener("click", function() {
        // Check the current state of the heart icon to decide which action to take
        if (this.innerHTML == `<i class="fas fa-heart"></i>`) {
            // If it's already liked (solid heart), decrement the like
            likeDecrement.call(this); 
        } else {
            // If it's unliked (outline heart), increment the like
            likeIncrement.call(this); 
        }
    });
});

function likeIncrement() {
  let postId = this.getAttribute("data-post-id");
  let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

  fetch("/pets/add-likes", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({
      "post-id": postId,
    }),
  })
    .then((response) => response.json()) // Make sure to parse the response as JSON
    .then((data) => {
      if (data.success) {
        console.log("New Like Count: ", data.new_like_count);

        let likeCountSpan = document.querySelector(`#like-count-${postId}`);
        likeCountSpan.textContent = `${data.new_like_count}`;

        // Update the heart icon to solid (liked)
        this.innerHTML = `<i class="fas fa-heart"></i>`;
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function likeDecrement() {
  let postId = this.getAttribute("data-post-id");
  let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

  fetch("/pets/remove-likes", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({
      "post-id": postId,
    }),
  })
    .then((response) => response.json()) // Parse the response as JSON
    .then((data) => {
      if (data.success) {
        console.log("New Like Count: ", data.new_like_count);

        let likeCountSpan = document.querySelector(`#like-count-${postId}`);
        likeCountSpan.textContent = `${data.new_like_count}`;

        // Update the heart icon to outline (unliked)
        this.innerHTML = `<i class="far fa-heart"></i>`;
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
