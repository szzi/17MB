// need to change to websocket server's address
var wsUri = "ws://192.168.43.6:9999";
var output;
var work,username;
var server_status;
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
  console.log("Connected");
  doSend_ticket();
}
function onClose(evt)
{
  console.log("DISCONNECTED");
}
function onMessage(evt)
{
  var message_recv = JSON.parse(evt.data);
  console.log('RESPONSE: ' + message_recv);
  // Call Notification method humere  
  console.log("work name: "+ message_recv.work); //작업의 종류
  console.log("user recognized: "+message_recv.username); //인식된 사람 일므

  work_type = message_recv.work;
  person = message_recv.username;

  if (message_recv.work==0) //detected
  {
    console.log("Human detected! camera opening..");
    location.href ='MicSpeak.html'
    console.log(person);
    
  }

  else if (message_recv.work==1)// working
  {
    // location.reload(true);
    location.href ='Dehumidification.html'
    // history.go(0);
  }
  else //humidity
  {
    location.reload(true);
    location.href ='Dehumidification.html'
    history.go(0);
  }
  console.log("user name: "+message_recv.username); //카메라로 인식한 사람의 이름
  server_status = message_recv.work; //서버 상태 저장 (일하는 중 or idle)
  // websocket.close();
  doSend_ticket();
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
  // var pre = document.createElement("p");
  // pre.style.wordWrap = "break-word";
  // pre.innerHTML = message;
  // output.appendChild(pre);
  // console.log(message)
}
// Notification code will be put here
window.addEventListener("load", init, false);