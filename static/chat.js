const chatArea = document.querySelector("#chat-area");
const messageInput = document.querySelector("#message-input");
const submitBtn = document.querySelector("#submit-btn");
const username = document.querySelector("#username").innerText;
const ws = new WebSocket(`/ws/chat/${username}`);
const users = document.querySelectorAll("#user");
const DOMAIN = "http://localhost:8000";

// event listeners
document.addEventListener("keypress", (event) => {
  if (event.keyCode == 13) {
    event.preventDefault();
    sendMessage(event);
  }
});

users.forEach((user) => {
  console.log(user.querySelector("#username").innerHTML);
  user.addEventListener("click", selectUser);
});

// on page load
users[0].click();

// Manipulate HTML
function displayChatMessage(username, message) {
  const newChatEl = document.createElement("div");
  if (username == "self") newChatEl.classList.add("self");
  else newChatEl.classList.add("other");

  if (username != "self") {
    const usernameEl = document.createElement("p");
    // usernameEl.classList.add("username");
    // usernameEl.innerText = username;
    newChatEl.appendChild(usernameEl);
  }

  const messageEl = document.createElement("p");
  messageEl.classList.add("message");
  messageEl.innerText = message;
  newChatEl.appendChild(messageEl);

  chatArea.appendChild(newChatEl);
}

function addSystemMessage(message) {
  const newChatEl = document.createElement("div");
  newChatEl.classList.add("system-message");
  newChatEl.innerText = message;
  chatArea.appendChild(newChatEl);
}

function clearChat() {
  chatArea.innerHTML = "";
}

function displayChats(chats) {
  chats.forEach((chat) => {
    if (chat.sender == username) {
      displayChatMessage("self", chat.message);
    } else {
      displayChatMessage(chat.sender, chat.message);
    }
  });
}

// Automatic scroll to the latest chat
const config = { childList: true };
const scrollToBottom = (mutation, observer) => {
  chatArea.scrollTop = chatArea.scrollHeight;
};
const observer = new MutationObserver(scrollToBottom);
observer.observe(chatArea, config);

// Handle WebSocket connection
function sendMessage(event) {
  if (messageInput.value == "") return;
  message = messageInput.value;
  messageInput.value = "";
  const receiver = document.querySelector("#receiver").innerHTML;

  let chat = JSON.stringify({
    sender: username,
    receiver: receiver,
    message: message,
  });

  console.log(chat);

  ws.send(chat);
  displayChatMessage("self", message);
  event.preventDefault();
}

ws.onmessage = function (event) {
  const chat = JSON.parse(event.data);
  if (chat.sender == "system") addSystemMessage(chat.message);
  else displayChatMessage(chat.sender, chat.message);
};

function removeUserSelection() {
  users.forEach((user) => {
    user.classList.remove("selected-user");
  });
}

function selectUser(event) {
  removeUserSelection();
  const receiver = event.target.querySelector("#username").innerHTML;
  event.target.classList.add("selected-user");
  const sender = username;
  clearChat();
  const chatAreaReceiver = document.querySelector("#receiver");
  chatAreaReceiver.innerText = receiver;
  const payload = JSON.stringify({
    sender: username,
    receiver: receiver,
  });

  console.log(payload);

  fetch(`${DOMAIN}/chat/chats`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: payload,
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Request failed.");
      }
      return response.json();
    })
    .then((chats) => {
      displayChats(chats.chats);
    });
}
