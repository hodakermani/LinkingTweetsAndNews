const Droplet = require('./droplet').Droplet;

const dropletAccessCommand = require('./droplet').dropletAccessCommand;
const config = require('../config');
const path = require('path');
const fs = require('fs');

const scriptsDir = './scripts';

function exportEnvironment() {
  let content = '';
  for (let k in RemoteRunner.env) {
    let line = `export ${k}=${RemoteRunner.env[k]}`;
    content += line + '\n';
  }
  fs.writeFileSync('./scripts/remote/environment.sh', content);
}

class RemoteRunner {
  static runOnDroplet(method) {
    return new Promise(async(resolve, reject) => {
      try {
        let droplet = await RemoteRunner.waitForDroplet();
        method(droplet);
        resolve();
      } catch (error) {
        reject(error);
      }
    });
  }

  static waitForDroplet() {
    return new Promise(async(resolve, reject) => {
      try {
        let droplet = await Droplet.getInstance();
        console.log('Waiting for droplet to get ready ...');
        await droplet.waitUntilBecomeAvailable();
        resolve(droplet);
      } catch (error) {
        reject(error);
      }
    });
  }

  static redeployScripts() {
    return new Promise(async(resolve, reject) => {
      try {
        let droplet = await RemoteRunner.waitForDroplet();
        droplet.executeCommand('rm -f -r ./scripts ./config_files');
        droplet.copyDirectory('scripts/remote', 'scripts');
        droplet.copyDirectory('config_files', 'config_files');
        resolve();
      } catch (error) {
        reject(error);
      }
    });
  }

  static deploy() {
    return new Promise(async(resolve, reject) => {
      try {
        let droplet = await RemoteRunner.waitForDroplet();
        console.log(`Access droplet: ${dropletAccessCommand} root@${droplet.ip}`);
        droplet.executeCommand('rm -f -r ./scripts ./config_files');
        droplet.copyDirectory('scripts/remote', 'scripts');
        droplet.copyDirectory('config_files', 'config_files');
        droplet.executeCommand('source ./scripts/deploy.sh');
        console.log('Droplet IP: ', droplet.ip);
        resolve();
      } catch (error) {
        reject(error);
      }
    });
  }

  static update() {
    return new Promise(async(resolve, reject) => {
      try {
        let droplet = await RemoteRunner.waitForDroplet();
        droplet.executeCommand(`source ./scripts/update.sh`);
        resolve();
      } catch (error) {
        reject(error);
      }
    });
  }

  static checkIfIsFinished() {
    return new Promise(async(resolve, reject) => {
      let droplet = await RemoteRunner.waitForDroplet();
      let out = await droplet.executeCommandAndGetOutput('head -n 10 ~/WTMFG/out.log');
      let found = out.match(/.*user.*system.*elapsed/g);
      if (found) {
        console.log('Finished');
        resolve(true);
      }
      else {
        console.log('Not Finished');
        resolve(false);
      }
    });
  }

  static poll() {
    let timeOutId;
    return new Promise((resolve, reject) => {
      function doPoll() {
        timeOutId = setTimeout(async() => {
          console.log('Polling...');
          let isFinished = await RemoteRunner.checkIfIsFinished();
          if (isFinished) {
            console.log('Polling Finished');
            resolve();
          }
          else {
            doPoll();
          }
        }, config.pollInterval);
      }

      return doPoll();
    });
  }

  static cat() {
    return new Promise(async(resolve, reject) => {
      try {
        let droplet = await RemoteRunner.waitForDroplet();
        console.log('Waiting for droplet to get ready ...');
        droplet.executeCommand(`cat ~/WTMFG/out.log`);
        resolve();
      } catch (error) {
        reject(error);
      }
    });
  }

  static recreate() {
    return new Promise(async(resolve, reject) => {
      try {
        await Droplet.recreate();
        resolve();
      } catch (error) {
        reject(error);
      }
    });
  }

  static run(numOfProcessors) {
    return new Promise(async(resolve, reject) => {
      try {
        let droplet = await RemoteRunner.waitForDroplet();
        exportEnvironment();
        droplet.copyFile('./scripts/remote/environment.sh', '~/.ssh/environment');
        droplet.executeCommand(`source ./scripts/run.sh ${numOfProcessors}`);
        resolve();
      } catch (error) {
        console.log('Error!');
        reject(error);
      }
    });
  }

  static runBatch() {
    let batchConfig = require('batchConfig');
    batchConfig.forEach(conf => {
      return new Promise(async(resolve, reject) => {
        try {
          let droplet = await RemoteRunner.waitForDroplet();
          RemoteRunner.env = conf;
          exportEnvironment();
          droplet.copyFile('./scripts/remote/environment.sh', '~/.ssh/environment');
          droplet.executeCommand(`source ./scripts/run.sh ${numOfProcessors}`);
          await RemoteRunner.poll();
          resolve();
        } catch (error) {
          console.log('Error!');
          reject(error);
        }
      });
    });
  }

  static setenv(key, value) {
    if (!value) {
      console.log('Invalid value');
      return;
    }
    if (!key) {
      console.log('Invalid key');
      return;
    }
    RemoteRunner.env[key] = value;
  }

  static getenv(key) {
    return RemoteRunner.env[key];
  }

  static clearenv() {
    RemoteRunner.env = {};
  }

  static rundev(numOfProcessors) {
    return new Promise(async(resolve, reject) => {
      try {
        let droplet = await RemoteRunner.waitForDroplet();
        droplet.executeCommand(`source ./scripts/rundev.sh ${numOfProcessors}`);
        resolve();
      } catch (error) {
        console.log('Error!');
        reject(error);
      }
    });
  }

  static getIP() {
    return new Promise(async(resolve, reject) => {
      let droplet = await Droplet.getInstance();
      let ip = await droplet.getIP();
      resolve(ip);
    });
  }

  static tail() {
    return new Promise(async(resolve, reject) => {
      let droplet = await Droplet.getInstance();
      droplet.executeCommand(`tail -f ./WTMFG/${config.outputPath}`);
      resolve();
    });
  }

  static destroy() {
    return Droplet.destroy();
  }

  static kill() {
    return new Promise(async(resolve, reject) => {
      try {
        let droplet = await RemoteRunner.waitForDroplet();
        try {
          droplet.executeCommand('pkill -f python');
          droplet.executeCommand('pkill -f wtmf');
        } catch (err) {
          console.log('No python process is running!');
        }
        resolve();
      } catch (error) {
        reject(error);
      }
    });
  }

  static jupyter() {
    return new Promise(async(resolve, reject) => {
      try {
        let droplet = await RemoteRunner.waitForDroplet();
        ;
        console.log('Droplet IP: ', droplet.ip);
        console.log('Waiting for droplet to get ready ...');
        droplet.executeCommand('source ./scripts/jupyter.sh');
        resolve();
      } catch (error) {
        reject(error);
      }
    });
  }

  static download() {
    return new Promise(async(resolve, reject) => {
      try {
        let droplet = await RemoteRunner.waitForDroplet();
        droplet.copyFileFromDroplet('~/WTMFG/out.log', './out.log');
        resolve();
      } catch (error) {
        reject(error);
      }
    });
  }
}

module.exports = RemoteRunner;