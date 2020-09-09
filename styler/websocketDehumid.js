// need to change to websocket server's address
var wsUri = "ws://192.168.43.6:9999";
var output;
var work,username;
var server_status;
function init()
{
  output = document.getElementById("output");
  console.log("continue");
  print(init);
  testWebSocket();
}
function testWebSocket()
{
  websocket = new WebSocket(wsUri);
  console.log("new socket")
  websocket.onopen = function(evt) { onOpen(evt) };
  websocket.onclose = function(evt) { onClose(evt) };
  websocket.onmessage = function(evt) { onMessage(evt) };
  websocket.onerror = function(evt) { onError(evt) };
}
function onOpen(evt)
{
  console.log("Connected");
  doSend_ticket();
}
function onClose(evt)
{
  // console.log("DISCONNECTED");
}
function onMessage(evt)
{
  var message_recv = JSON.parse(evt.data);
  console.log('RESPONSE: ' + message_recv);

  work_type = message_recv.work;

  if (message_recv.work==2)
  {
    writeToScreen("Dehumiditication is completed!") //습기제거 종료
    setTimeout(function() {location.href='index.html'}, 3000);
    doSend_ticket();

  }
}
function onError(evt)
{
  console.log('ERROR:'+ evt.data);
}
function doSend()
{
  var message_send = {
    "work" : "1"
};
console.log("SENT: " + JSON.stringify(message_send));
websocket.send(JSON.stringify(message_send));
}
function doSend_ticket()
{
  var message_send = {
      'work':'ticket'
  };
  console.log("SENT: " + JSON.stringify(message_send));
  websocket.send(JSON.stringify(message_send));
}
function writeToScreen(message)
{
   var pre = document.createElement("p");
   pre.style.wordWrap = "break-word";
   pre.innerHTML = message;
   output.appendChild(pre);
   console.log(message)
}
// Notification code will be put here
window.addEventListener("load", init, false);