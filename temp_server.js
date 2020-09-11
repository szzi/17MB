var express = require('express');
var http = require('http');

var app = express();
var server = http.createServer(app);
server.listen(1004);
 




//2. socket.io 서버 생성
var io = require('socket.io')(server);
/*
var Server = require('socket.io');
var io = new Server(httpServer);
*/

//3. client 접속 확인 ->connection event
io.on('connection',function(socket){
    console.log('클라이언트 접속함!!');


    
//클라이언트한테 받기 - object 형식
socket.on('response',function(data){
    var msg = data['work'];
    console.log(data);
    //아마 Im fine이라고 왔을 듯
});

    //접속하자마자 끝날 때 까지 처리
    socket.on('disconnect',function(){
        console.log('클라이언트 접속 끊김 ㅠㅠ');
    });


    

}); //io.on (연결된 클라이언트 대상으로 시행)


