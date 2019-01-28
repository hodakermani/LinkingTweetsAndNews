const RemoteRunner = require('./remoteRunner');
const LocalRunner = require('./localRunner');
const dropletAccessCommand = require('./droplet').dropletAccessCommand;
const config = require('../config');
const messages = require('./messages');

async function remote() {
  RemoteRunner.env = {};
  console.log(messages.remoteRunner.start);
  process.stdin.on('data', async(data) => {
    data = String(data).split('\n')[0];
    console.log(messages.command.start);
    let command = data.split(' ')[0];
    if (command === 'run')
      await RemoteRunner.run(data.split(' ')[1]);
    else if(command === 'rundev')
      await RemoteRunner.rundev(data.split(' ')[1]);
    else if (command === 'ip')
      console.log(`Access droplet: \n ${dropletAccessCommand} root@${await RemoteRunner.getIP()}`);
    else if(command === 'setenv')
      await RemoteRunner.setenv(data.split(' ')[1], data.split(' ')[2]);
    else if(command === 'getenv')
      console.log(await RemoteRunner.getenv(data.split(' ')[1]));
    else {
      let methodToBeCalled = RemoteRunner[command];
      if (!methodToBeCalled)
        console.log(messages.remoteRunner.invalidCommandMessage);
      else
        await methodToBeCalled(data);
    }
    console.log(messages.command.end);
  });
}

async function local() {
  console.log(messages.localRunner.start);
  process.stdin.on('data', async(data) => {
    data = String(data).split('\n')[0];
    console.log(messages.command.start);
    let command = data.split(' ')[0];
    let methodToBeCalled = LocalRunner[command];
    if (!methodToBeCalled)
      console.log(messages.remoteRunner.invalidCommandMessage);
    else
      await methodToBeCalled(data);
    console.log(methodToBeCalled.localRunner.end);
  });
}

module.exports = {
  local, remote
};