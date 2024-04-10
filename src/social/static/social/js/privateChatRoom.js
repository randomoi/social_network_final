// START - code was developed with the help of documentation and enhanced with adding image to the text message, please see referenced links.
/**
 * Add text or image message to chat
 * @param {string} username - senders username
 * @param {string} timestamp - time of sent message
 * @param {string} content - text or image URL of message.
 * @param {boolean} isImageFile - image file
 * @param {boolean} isSender - sender
 */
 function addMessage(username, timestamp, content, isImageFile, isSender) {
    // holder of messages 
    const messageHolder = document.createElement('div');
    messageHolder.className = `chat-msg-box ${isSender ? 'chat-sender-message' : 'chat-friend-message'}`;

    // holder for senders name and time 
    const headerHolder = document.createElement('div');
    const timeRecord = document.createElement('span');
    timeRecord.innerText = `(${timestamp}): `;
    const senderUsername = document.createElement('b');
    senderUsername.innerText = isSender ? 'Me' : username;

    headerHolder.appendChild(senderUsername);
    headerHolder.appendChild(timeRecord);
    messageHolder.appendChild(headerHolder);

    // add text or image
    if (isImageFile) {
        const image = document.createElement('img');
        image.className = `chat-image-box ${isSender ? 'chat-sender-image' : 'chat-friend-image'}`;
        image.src = content;
        messageHolder.appendChild(image);
    } else {
        const textSpanElement = document.createElement('span');
        textSpanElement.innerText = content;
        messageHolder.appendChild(textSpanElement);
    }

    document.getElementById('chat-messages').appendChild(messageHolder);
    scrollToLast();
}

// handles scrolling to latest messages 
function scrollToLast() {
    const sectionHolder = document.getElementById("chat-messages");
    sectionHolder.scrollTop = sectionHolder.scrollHeight;
}

scrollToLast();

// creates WebSocket connection for chat 
const chatWebSocket = new WebSocket(`ws://${window.location.host}/ws/${privatChatRoomName}/`);

// handles date formatting
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/padStart
// https://www.w3schools.com/jsref/jsref_obj_date.asp
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/getUTCMonth
function dateFormatUTC(date) {
    const allMonths = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'Jun.', 'Jul.', 'Aug.', 'Sep.', 'Oct.', 'Nov.', 'Dec.'];
    const month = allMonths[date.getUTCMonth()];
    const day = date.getUTCDate();
    const year = date.getUTCFullYear();
    let hours = date.getUTCHours();
    const mins = date.getUTCMinutes().toString().padStart(2, '0'); 
    const am_pm = hours >= 12 ? 'p.m.' : 'a.m.';
    hours = hours % 12;
    hours = hours === 0 ? 12 : hours; 

    return `${month} ${day}, ${year}, ${hours}:${mins} ${am_pm}`;
}

// receiving messages handler
chatWebSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);

    // get timestamp from server
    const serverTime = data.timestamp;

    // transform server time to Date()
    const msgDate = new Date(serverTime);

    // user date formatting function to format date and time 
    const timeRecord = dateFormatUTC(msgDate);
 
    const isSender = data.username === username;

    // check if text or image and add it 
    if (data.message && data.username) {
        const isImageFile = data.message.startsWith('data:image');
        addMessage(data.username, timeRecord, data.message, isImageFile, isSender);
    } else if (data.image_url && data.username) {
        addMessage(data.username, timeRecord, data.image_url, true, isSender);
    } else {
        console.log('Empty message or username!');
    }
};

// handle WebSocket when it closes and prints message to console
chatWebSocket.onclose = function (e) {
    console.log('Chat socket closed abruptly!');
};

// handles WebSocket errors and print them to console
chatWebSocket.onerror = function (error) {
    console.error("Chat socket error:", error);
};


// transmits message through WS
 function transmitMessage() {
    // text and image inputs
    const textInputDOM = document.querySelector('#chat-text-input');
    const message = textInputDOM.value.trim(); // removes whitespace
    const imageInputDOM = document.querySelector('#chat-image-input');
    const file = imageInputDOM.files[0];

    // if text or image 
    if (message || file) {
        try {
            if (message) { // if text message, send it
                chatWebSocket.send(JSON.stringify({message, username, room: privatChatRoomName}));
            } else if (file) { // if image file
                // if it's image file that starts with image/ read and send it 
                if (file.type.startsWith('image/')) { 
                    const imageReader = new FileReader();
                    imageReader.onloadend = function () {
                        const stringBase64 = imageReader.result.replace('data:', '').replace(/^.+,/, '');
                        chatWebSocket.send(JSON.stringify({'image': stringBase64, 'username': username, 'room': privatChatRoomName}));
                    };
                    imageReader.readAsDataURL(file);
                } else { // otherwise display error
                    console.error("Unsupported file format. Please upload .jpg, .jpeg or .png.");
                    return;
                }
            }
            
        } catch (error) { // catch an error and display it
            console.error("Can not send message. Error:", error);
        }

        // refresh input fields after text or image was sent
        textInputDOM.value = '';
        imageInputDOM.value = '';
    } else {
        console.log("Nothing was sent.");
    }
}

// add transmitmessage to SEND button
document.querySelector('#submit-chat-message').onclick = transmitMessage;

// References:
// https://djangochannelsrestframework.readthedocs.io/en/latest/tutorial/part_1.html
// https://djangochannelsrestframework.readthedocs.io/en/latest/tutorial/part_2.html
// https://developer.mozilla.org/en-US/docs/Web/API/WebSocket
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/parse
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/toLocaleString
// https://developer.mozilla.org/en-US/docs/Web/API/Document/createElement
// https://developer.mozilla.org/en-US/docs/Web/API/FileReader/readAsDataURL
// https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelector
// https://developer.mozilla.org/en-US/docs/Web/API/FileList
// https://developer.mozilla.org/en-US/docs/Web/API/FileReader
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/padStart
// https://www.w3schools.com/jsref/jsref_obj_date.asp
// https://stackoverflow.com/questions/76798762/django-websocket-website-returning-an-empty-json-dictionary-when-i-try-to-refere

// END - code was developed with the help of documentation and enhanced with adding image to the text message, please see referenced links.