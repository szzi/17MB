// need to change to websocket server's address
var wsUri = "ws://192.168.43.6:9999";
var output;
var flag;

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
  //flag : 최초인지아닌지 분간용
  flag=0;
  console.log("Connected");
  doSend();
 
}

function onClose(evt)
{
  console.log("DISCONNECTED");
}

function onMessage(evt)
{
  /*
  if (flag)
  {
    //cnt값으로 판별 -> 숫자가 적으면 카메라 열고, 숫자가 크면 걍 무시...
    //type1->cnt 값으로 판별, type2->문열기
    
    if(cnt<5)
    {
        console.log("camera open!");
        location.href="../../"
    }
    else
    {

    }
  }
  else //flag=0 -> initial connection msg
  {
    setTimeout(function() {doSend();}, 5000);
    flag=1;
  }*/
  //var message = JSON.parse(evt.data);
  var message = evt.data;
  writeToScreen('<span style="color: blue;">RESPONSE: ' + message +'</span>');
  // Call Notification method here
  console.log(message)
  /*
  console.log(message.type);
  console.log(message.state);
*/
  // websocket.close();

  /*message parsing */
/*
  if (message.type=="1")
  {
    console.log("type1");
  }
  else if (message.type=="2")
  {
    console.log("type2");
  }
  else if(message.type=="3")
  {
    console.log("type3");
  }
  else{
    console.log("what?!");
  }
*/
setTimeout(function() {doSend();}, 5000);
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