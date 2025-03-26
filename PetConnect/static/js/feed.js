let heartButtons = document.querySelectorAll(".heart-button");
let commentButtons = document.querySelectorAll(".comment-button");

document.getElementById('create-post-form').addEventListener('submit', function(event) {
    event.preventDefault();
    let form = new FormData(this);
    let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    fetch("/pets/create-post", {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken 
        },
        body: form,
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.reload(); 
        } else {
            alert("Error: " + data.error);
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Failed to create post");
    });
});

commentButtons.forEach((button) => {
  button.addEventListener("click",saveComment)
});

heartButtons.forEach((button) => {
    button.addEventListener("click", function() {
        if (this.innerHTML == `<i class="fas fa-heart"></i>`) {
            likeDecrement.call(this); 
        } else {
            likeIncrement.call(this); 
        }
    });
});


function saveComment() {
    let commentInput = this.closest('.comments-div').querySelector('.form-control'); 
    let commentText = commentInput.value;
    let postId = this.getAttribute("data-post-id");
    let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    if (!commentText.trim()) {
        alert("Please enter a comment!");
        return; 
    }

    fetch("/pets/add-comments", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({
            "post-id":postId,
            "comment-content": commentText,
        }),
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.success) {
            console.log("Comment has been added");

            let commentDiv = this.closest('.comments-div').querySelector('.comment-list');
            let newComment = document.createElement('p');  
            newComment.innerHTML = `<strong>${data.username}:</strong> ${data.comment_text}`; 
            commentDiv.appendChild(newComment);  

            commentInput.value = '';
        }
    })
    .catch((error) => {
        console.error("Error:", error);
    });
}

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
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        console.log("New Like Count: ", data.new_like_count);

        let likeCountSpan = document.querySelector(`#like-count-${postId}`);
        likeCountSpan.textContent = `${data.new_like_count}`;

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
    .then((response) => response.json()) 
    .then((data) => {
      if (data.success) {
        console.log("New Like Count: ", data.new_like_count);

        let likeCountSpan = document.querySelector(`#like-count-${postId}`);
        likeCountSpan.textContent = `${data.new_like_count}`;

        this.innerHTML = `<i class="far fa-heart"></i>`;
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
