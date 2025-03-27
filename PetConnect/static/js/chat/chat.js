// static/js/chat/chat.js
const chatroomData = JSON.parse(
  document.getElementById("chatroom-data").textContent
);
const chatId = chatroomData.id;
const roomName = chatroomData.chat_name;
const userId = JSON.parse(document.getElementById("user-id").textContent);
const username = JSON.parse(document.getElementById("username").textContent);

document.getElementById("leave-chat").addEventListener("click",leaveChat)

const chatSocket = new WebSocket(
  "ws://" + window.location.host + "/ws/chat/" + roomName + "/"
);

// Message handling function
function appendMessage(username, content) {
  const chatLog = document.getElementById("chat-log");

  // Remove empty placeholder if it exists
  if (chatLog.classList.contains("empty-chat")) {
    chatLog.classList.remove("empty-chat");
    const placeholder = chatLog.querySelector(".empty-placeholder");
    if (placeholder) placeholder.remove();
  }

  const messageDiv = document.createElement("div");
  messageDiv.className = "message";
  messageDiv.innerHTML = `<strong>${username}:</strong> ${content}`;
  chatLog.appendChild(messageDiv);

  chatLog.scrollTop = chatLog.scrollHeight;
}

// WebSocket handlers
chatSocket.onmessage = function (e) {
  const data = JSON.parse(e.data);
  appendMessage(data.username || username, data.message);
};

chatSocket.onclose = function (e) {
  console.error("Chat socket closed unexpectedly");
};

// Input and send handlers
document.querySelector("#chat-message-input").focus();

document
  .querySelector("#chat-message-input")
  .addEventListener("keyup", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      document.querySelector("#chat-message-submit").click();
    }
  });

document
  .querySelector("#chat-message-submit")
  .addEventListener("click", function (e) {
    const messageInputDom = document.querySelector("#chat-message-input");
    const message = messageInputDom.value.trim();

    if (message) {
      chatSocket.send(
        JSON.stringify({
          message: message,
          refChat: chatId,
          author: userId,
          type: 0,
          extraData: "",
        })
      );
      messageInputDom.value = "";
    }
  });

// Initial scroll to bottom
window.addEventListener("DOMContentLoaded", () => {
  const chatLog = document.getElementById("chat-log");
  if (chatLog) {
    chatLog.scrollTop = chatLog.scrollHeight;
  }
});

// Cleanup on page unload
window.addEventListener("beforeunload", () => {
  chatSocket.close();
});

function leaveChat(){
    let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  fetch("/pets/leave-chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({ chat_name: roomName }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        window.location.reload();
      } else {
        alert("Error leaving chat: " + data.error);
      }
    })
    .catch((error) => console.error("Error:", error));
}
