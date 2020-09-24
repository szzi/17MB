// See https://github.com/dialogflow/dialogflow-fulfillment-nodejs
// for Dialogflow fulfillment library docs, samples, and to report issues
'use strict';

const functions = require('firebase-functions');
const { WebhookClient } = require('dialogflow-fulfillment');
const { Card, Suggestion } = require('dialogflow-fulfillment');

// // The Firebase Admin SDK to access the Firebase Realtime Database.
const admin = require('firebase-admin');
admin.initializeApp({
  credential: admin.credential.applicationDefault(),
  databaseURL: 'ws://mb-73eca.firebaseio.com/'
});

process.env.DEBUG = 'dialogflow:debug'; // enables lib debugging statements

exports.dialogflowFirebaseFulfillment = functions.https.onRequest((request, response) => {
  const agent = new WebhookClient({ request, response });
  console.log('Dialogflow Request headers: ' + JSON.stringify(request.headers));
  console.log('Dialogflow Request body: ' + JSON.stringify(request.body));

  const styler = admin.database().ref('styler');
  const users = admin.database().ref('users');
  const cycle = admin.database().ref('cycle');

  function setCycle(agent) {
    //const sub = agent.parameters.sub;
    return styler.once('value').then((snapshot) => {
      const main = agent.parameters.main.toString();
      const sub = agent.parameters.sub.toString();
      var attr = snapshot.val();

      if (!attr.working) {
        if (sub == 'Time Dry') {
          styler.update({ time: 30 });
          agent.add('Drying time is set to 30 mintues. Do you want to start it right away?');
        }
        else {
          styler.update({ main: main, sub: sub });
          agent.add('Do you want to start ' + main + ' ' + sub + ' cycle right away?');

          var mainRef = cycle.child(main);
          var subRef = mainRef.child(sub);
          return subRef.once('value').then((snapshot) => {
            var ref = snapshot.val();
            styler.update({ time: ref.time });
            agent.add('It takes ' + ref.time + ' minutes.');

            var userRef = users.child(attr.user).orderByChild('main').equalTo(main);
            var exist = false;
            return userRef.once('value').then((snapshot) => {
              if (snapshot.exists()) {
                snapshot.forEach(child => {
                  if (child.val().sub == sub) {
                    exist = true;
                    var cnt = child.val().cnt;
                    cnt = cnt+1;
                    users.child(attr.user).child(child.key).update({ cnt: cnt});
                    agent.add('Got it!');
                  }
                });
                if(!exist){
                  // same main, different sub
                  var newRef = users.child(attr.user).push({
                    main: main,
                    sub: sub,
                    cnt: 1
                  });
                //agent.add('(same main exist)new cycle is added');
                }
              } else {
                var realnewRef = users.child(attr.user).push({
                      main: main,
                      sub: sub,
                      cnt: 1
                    });
                //agent.add('new cycle is added');
              }
            });
          });
        }
      } else {
        if (sub == 'Time Dry') {
          styler.update({ time: attr.time + 30 });
          agent.add('30 minutes have been added for the dry.');
        } else {
          agent.add('Sorry, ' + attr.main + ' ' + attr.sub + ' cycle is already running.');
          agent.add('It\'ll be finished after ' + attr.time + ' minutes.');
        }
      }
    });
  }

  function setDelay(agent) {
    return styler.once("value").then((snapshot) => {
      var time = agent.parameters.duration;
      var attr = snapshot.val();

      snapshot.update({ time: attr.time + time, working: 2 });
      agent.add(attr.main + ' ' + attr.sub + ' cycle is going to start after ' + time + ' minutes.');
    });
  }

  function startNow(agent) {
    const main = agent.contexts[0].parameters.main;
    const sub = agent.contexts[0].parameters.sub;

    styler.update({ working: 1 });
    agent.add(main + ' ' + sub + ' cycle is running now.');
  }

  function getTime(agent) {
    return styler.once("value").then((snapshot) => {
      var c_info = snapshot.val();
      //agent.add(c_info.time+' is left');
      if ((c_info.time / 60) >= 1) {
        var hours = c_info.time / 60;
        var minutes = c_info.time % 60;
      	agent.add(Math.floor(hours) + 'hour ' + minutes + 'minutes left for' + c_info.main + ' ' + c_info.sub + ' cycle to finish');
      } else {
        agent.add(c_info.time + ' left for ' + c_info.main + ' ' + c_info.sub + ' cycle to finish ');
      }
      
      if((c_info.working == 0)){
        agent.add(`The styler is idle now.`);
      }
    });
  }

  function recommendCycle(agent) {
    return styler.once("value").then((snapshot) => {
      var user = snapshot.val();
      if (user.user != null) {
        agent.add(user.user + ' is using now');

        if (!user.working) {
          return users.child(user.user)
            .orderByChild('cnt')
            .limitToLast(1)
            .once("child_added")
            .then((data) => {
              var personal = data.val();
              var p_main = personal.main;
              var p_sub = personal.sub;
              agent.add(p_main + ' ' + p_sub + ' would be good for you. Would you like to proceed with this?');
              styler.update({main:p_main, sub:p_sub});
            });
        } else {
          agent.add('Sorry, ' + user.main + ' ' + user.sub + ' cycle is already running.');
          agent.add('It will be finished after ' + user.time + ' minutes.');
        }
      }
    });
  }

  function recommendYes(agent) {
    return styler.once("value").then((snapshot) => {
      var s_styler = snapshot.val();
      //agent.add(`recommend yes!`);
      //agent.add(`main is ` + s_styler.main + ` sub is ` + s_styler.sub);
      agent.add(`OK, I'll get `+s_styler.main+` `+s_styler.sub+` cycle started.`);
      var main = s_styler.main;
      var sub = s_styler.sub;
      return cycle.child(main).child(sub).once("value").then((snapshot) => {
        var time = snapshot.val();
        styler.update({working:1,time:time.time});
      });
    });
  }

  function welcome(agent) {
    agent.add(`Hi, may I help you?`);
  }

  function getAgentNameHandler(agent) {
    agent.add('From fulfillment: My name is Dialogflow!');
  }

  function fallback(agent) {
    agent.add(`I didn't understand`);
    agent.add(`I'm sorry, can you try again?`);
  }

  // Run the proper function handler based on the matched Dialogflow intent name
  let intentMap = new Map();
  intentMap.set('Default Welcome Intent', welcome);
  intentMap.set('Default Fallback Intent', fallback);
  intentMap.set('get-agent-name', getAgentNameHandler);
  intentMap.set('StylingCycle', setCycle);
  intentMap.set('StartNow', startNow);
  intentMap.set('DelayStart', setDelay);
  intentMap.set('StylingTime', getTime);
  intentMap.set('recommend', recommendCycle);
  intentMap.set('recommend - yes', recommendYes);
  agent.handleRequest(intentMap);
});