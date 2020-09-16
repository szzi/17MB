// See https://github.com/dialogflow/dialogflow-fulfillment-nodejs
// for Dialogflow fulfillment library docs, samples, and to report issues
'use strict';
 
const functions = require('firebase-functions');
const {WebhookClient} = require('dialogflow-fulfillment');
const {Card, Suggestion} = require('dialogflow-fulfillment');

// // The Firebase Admin SDK to access the Firebase Realtime Database.
const admin = require('firebase-admin');
admin.initializeApp({
  credential: admin.credential.applicationDefault(),
  databaseURL: 'ws://mb-73eca.firebaseio.com/'
});

process.env.DEBUG = 'dialogflow:debug'; // enables lib debugging statements
 
exports.dialogflowFirebaseFulfillment = functions.https.onRequest((request, response) => {
  const agent = new WebhookClient({request, response});  
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
      const user = "Seojin";
      
      if (!attr.working) {
        styler.update({ main: main, sub: sub, user: user, working: 1 });
        if (main == 'Delay Start') {
          agent.add('How much do you want to delay?');
          styler.update({ time: 180 });
          agent.add('OK, it\'ll start after 3 hours.');
        }
        else if (sub == 'Time Dry') {
          agent.add('Drying time is set to 30 minutes.');
          styler.update({ time : 30 });
        }
        else {
          agent.add('OK, I will get the ' + main + ' ' + sub + ' cycle started.');
          
          var mainRef = cycle.child(main);
          var subRef = mainRef.child(sub);
          return subRef.once('value').then((snapshot) => {
            var ref = snapshot.val();
            styler.update({ time : ref.time});
            agent.add('It takes ' + ref.time + ' minutes.');
          });
        }
      } else {
        agent.add('Sorry, ' + attr.main + ' ' + attr.sub + ' cycle is already running.');
      }
    });
  }

  function welcome(agent) {
    agent.add(`Hi, may I help you?`);
  }
  
  /*function startCycle(agent) {
   	const allContext = agent.contexts;
    const context = agent.getContext('stylingcycle-followup');
    console.log('context : ' + JSON.stringify(allContext));
    
    agent.add("the cycle you chose is");
  }*/
  
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
  agent.handleRequest(intentMap);
});