document.querySelector("#chatName").focus();

// Handle Enter key press for chat creation form
document.querySelector("#chatName").onkeyup = function (e) {
  if (e.keyCode === 13) {
    document.querySelector("#createChatSubmit").click();
  }
};

document
  .querySelector("#createChatSubmit")
  .addEventListener("click", function (e) {
    e.preventDefault();

    const chatName = document.querySelector("#chatName").value;
    const addUsers = document.querySelector("#addUsers").value.split(" "); // Space-separated usernames

    createChat(chatName, addUsers);
  });

function createChat(chatName, addUsers) {
  let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  fetch("/pets/create-chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({ chat_name: chatName }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        alert("Chat created successfully!");
        addUsersToChat(chatName, addUsers);
      } else {
        alert("Error creating chat: " + data.error);
      }
    })
    .catch((error) => console.error("Error:", error));
}

function addUsersToChat(chatName, addUsers) {
  let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  const addUserPromises = addUsers.map((username) => {
    return fetch("/pets/add-user", {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken },
      body: JSON.stringify({ chat_name: chatName, username: username.trim() }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (!data.success)
          throw new Error(`Error adding ${username}: ${data.error}`);
      });
  });

  Promise.all(addUserPromises)
    .then(() => (window.location.href = `/pets/${chatName}/`))
    .catch((error) => alert(error.message));
}
