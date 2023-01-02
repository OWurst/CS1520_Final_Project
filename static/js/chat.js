let timeoutID;
let timeout = 15000;

window.addEventListener('load', setup);

function setup() { 
    timeoutID = window.setTimeout(poller, timeout);
    showMessages();
    const chatSubmitButton = document.getElementById("submitButton");
    chatSubmitButton.addEventListener('click', chatSubmit)
}

function chatSubmit() {
    var msg = document.getElementById("chatToSend");
    var name = document.getElementById("user");

    fetch("/new_message/", {
        method: "post",
        headers: { "Content-type": "application/x-www-form-urlencoded; charset=UTF-8" },
        body: `username=${name.value}&message=${message = msg.value}`
    })
    .then((response) => {
        return response.json();
    })
    .then(() => {
        msg.value = "";
        showMessages();
        })
        .catch(() => {
            console.log("Error posting new chats!");
        });
}

function showMessages() {
    fetch("/messages/")
        .then((response) => {
            return response.json();
        })
        .then((results) => {
            let chat_window = document.getElementById("chat_window");
            let messages = "";
            for (let index in results) {
                current_set = results[index];
                
                keys = Object.keys(current_set);
                userKey = keys[0];
                author = current_set[userKey];
                chatKey = keys[1];

                message = current_set[chatKey];
                
                messages += `${author}:\n${message}\n\n`;
            }
            chat_window.innerText = messages;
            timeoutID = window.setTimeout(poller, timeout);
		    //chat_window.scrollTop = scroll_to_bottom.scrollHeight;
        })
        .catch(() => {
            chat_window.value = "error retrieving messages from server";
        });
}

function poller() {
	console.log("Polling for new items");
	showMessages();
}