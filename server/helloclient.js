// helloclient.js
// Subscribe & cancel subscription to helloService's heartbeat method
var Service = require('webos-service');
var pmloglib = require('pmloglib'); // For use pmlog, pmlog is wirted /var/log/messages

var context = new pmloglib.Context("helloClient"); // Create context of pmlog
var service = new Service("com.example.helloclient"); // Register com.example.helloworld

console.log("simple call");
//Change @SERVICE-NAME@ to real service name
/*
service.call("luna://@SERVICE-NAME@/hello", {}, function(message) {
    context.log(pmloglib.LOG_INFO, "SERVICE_CALL",{}, "call @SERVICE-NAME@/hello");
    console.log("message payload: " + JSON.stringify(message.payload));
    var sub = service.subscribe("luna://@SERVICE-NAME@/heartbeat", {subscribe: true});
    var count = 0;
    var max = 10;
    sub.addListener("response", function(msg) {
        console.log(JSON.stringify(msg.payload));
        if (++count >= max) {
            sub.cancel();
            setTimeout(function(){
                console.log(max+" responses received, exiting...");
                process.exit(0);
            }, 1000);
        }
    });
});
*/

/**************************************** */
var http = require('http');
var fs = require('fs');
var app = http.createServer(function(request,response){
    var url = request.url;
    if(request.url == '/'){
      url = '/index.html';
    }
    if(request.url == '/favicon.ico'){
      return response.writeHead(404);
    }
    response.writeHead(200);
    console.log(__dirname + url);
    response.end(fs.readFileSync(__dirname + url));
    //사용자에게 전송할 데이터를 생성한다
 
});
app.listen(3000);