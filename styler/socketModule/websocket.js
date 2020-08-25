// need to change to websocket server's address
var wsUri = "ws://192.168.43.6:9999";
var output;
var flag=0;
var connected;

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
  // writeToScreen("CONNECTED");
  flag=0;
  connected=0;
  console.log("Connected");
  doSend();
 
}

function onClose(evt)
{
  console.log("DISCONNECTED");
}

function onMessage(evt)
{
  //var message = JSON.parse(evt.data);
  var message_recv = JSON.parse(evt.data);
  writeToScreen('<span style="color: blue;">RESPONSE: ' + message +'</span>');

  // Call Notification method here  
  console.log(message_recv.type);
  console.log(message_recv.state);

  // websocket.close();
  if(connected) //after second connection
{
  switch(message_recv.type){
    case "1":
            if(flag<20)
            {
              flag++;
              console.log("detecting now..");
            }
            else
            {
              flag=0;
              console.log("mic speaking");
            }
            break;
    case "2":
            console.log("door is opening~~~");
    default:
            console.log(message_recv);
            console.log(message_recv)
  }
}
else
  connected=1;
  setTimeout(function() {doSend();}, 2500);
}

function onError(evt)
{
  writeToScreen('<span style="color: red;">ERROR:</span> ' + evt.data);
}

function doSend()
{
  var message_send = {
      "ip_address" : "192.168.43.23"
  };

  writeToScreen("SENT: " + JSON.stringify(message_send));
  websocket.send(JSON.stringify(message_send));
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