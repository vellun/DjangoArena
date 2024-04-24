// const url = new URL(window.location.href);
// const path = url.pathname;
// const pathComponents = path.split('/');
// const roomId = pathComponents[pathComponents.length - 2];
//
// const chatSocket = new WebSocket(
//     'ws://'
//     + window.location.host
//     + `/${roomId}/`
// );
//
// chatSocket.onmessage = function (e) {
//     const data = JSON.parse(e.data);
//     if (data.message === "start_game") {
//         document.getElementById("lobby-page").style.display = "none";
//         document.getElementById("game-page").style.display = "block";
//     }
// };
//
// chatSocket.onclose = function (e) {
//     console.error('Chat socket closed unexpectedly');
// };
//
// document.querySelector('#start-button').onclick = function (e) {
//     chatSocket.send(JSON.stringify({
//         "message": "start_game",
//     }));
// };