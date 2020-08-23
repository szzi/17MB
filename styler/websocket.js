// need to change to websocket server's address
var wsUri = "ws://192.168.43.6:9999";
var output;

function init()
{
  output = document.getElementById("output");
  console.log("init");
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
  writeToScreen("CONNECTED");
  console.log("Connected");
  doSend();
}

function onClose(evt)
{
  writeToScreen("DISCONNECTED");
}

function onMessage(evt)
{
  // var message = JSON.parse(evt.data);
  var message = evt.data;
  writeToScreen('<span style="color: blue;">RESPONSE: ' + message +'</span>');
  // Call Notification method here
  console.log(message)
  print(message);
  websocket.close();
}

function onError(evt)
{
  writeToScreen('<span style="color: red;">ERROR:</span> ' + evt.data);
}

function doSend()
{
  var message = {
      "ip_address" : "192.168.43.23"
  };

  writeToScreen("SENT: " + JSON.stringify(message));
  websocket.send(JSON.stringify(message));
}

function writeToScreen(message)
{
  var pre = document.createElement("p");
  pre.style.wordWrap = "break-word";
  pre.innerHTML = message;
  output.appendChild(pre);
}

// Notification code will be put here

window.addEventListener("load", init, false);