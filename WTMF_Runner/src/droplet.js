const childProcess = require('child_process');
const config = require('../config');
const api = require('./api');
const dropletAccessCommand = 'ssh -i secrets/do_id_rsa -o StrictHostKeyChecking=no ';
const dropletSCPAccessCommand = 'scp -i secrets/do_id_rsa -o StrictHostKeyChecking=no ';
class Droplet {
  constructor(id, details) {
    this.id = id;
    this.ip = details.droplet.networks.v4[0].ip_address;
    //this.deleteTimeoutId = setTimeout(async() => {
    //  await Droplet.destroy();
    //  Droplet.instance = null;
    //}, config.serverDestroyTimeout * 59 * 60 * 1000);
  }

  static async getInstance() {
    if (Droplet.instance)
      return Droplet.instance;
    let id = await api.getDropletIdByTag();
    if (!id) {
      let droplet = await this.recreate();
      id = droplet.id;
    } else
      console.log('Droplet exists!');
    const details = await api.getDropletDetails(id);
    Droplet.instance = new Droplet(id, details);
    return Droplet.instance;
  }

  static async recreate() {
    try {
      let id = await api.getDropletIdByTag();
      if (id)
        await api.deleteDroplet(id);
      let dropletDetails = await api.createDroplet();
      id = dropletDetails.droplet.id;
      let ip = null;
      let details;
      while (!ip) {
        details = await api.getDropletDetails(id);
        if (details && details.droplet.networks && details.droplet.networks.v4 && details.droplet.networks.v4[0]) {
          ip = details.droplet.networks.v4[0].ip_address;
          console.log('IP assigned: ', ip);
        }
      }
      Droplet.instance = new Droplet(id, details);
      return Droplet.instance;
    } catch (err) {
      console.log(err);
    }
  }

  static async destroy() {
    let id = await api.getDropletIdByTag();
    if (id)
      await api.deleteDroplet(id);
    Droplet.instance = null;
  }

  async getDetails() {
    return new Promise(async(resolve, reject) => {
      let details = await api.getDropletDetails(this.id);
      resolve(details);
    });
  }

  async getIP() {
    return new Promise(async(resolve, reject) => {
      let ip = null;
      let details = await this.getDetails();
      if (details && details.droplet.networks && details.droplet.networks.v4 && details.droplet.networks.v4[0])
        ip = details.droplet.networks.v4[0].ip_address;
      resolve(ip);
    });
  }

  copyFile(sourcePath, destinationPath) {
    childProcess.execSync(`${dropletSCPAccessCommand} ${sourcePath} root@${this.ip}:${destinationPath}`);
    console.log(`"${sourcePath}" copied!`);
  }

  copyFileFromDroplet(sourcePath, destinationPath) {
    childProcess.execSync(`${dropletSCPAccessCommand} root@${this.ip}:${sourcePath} ${destinationPath}`);
    console.log(`"${sourcePath}" copied!`);
  }

  copyDirectory(sourcePath, destinationPath) {
    childProcess.execSync(`${dropletSCPAccessCommand} -r ${sourcePath} root@${this.ip}:${destinationPath}`);
    console.log(`"${sourcePath}" copied!`);
  }

  async waitUntilBecomeAvailable() {
    let droplet = this;
    return new Promise((resolve, reject) => {
      let intervalId = setInterval(async() => {
        try {
          await droplet.executeCommand('ls');
          console.log('Droplet available: ', this.ip);
          clearInterval(intervalId);
          resolve();
        } catch (err) {
          console.log('Droplet not available: ', this.ip);
        }
      }, 1000);
    });
  }

  executeCommand(command, options) {
    let output = childProcess.execSync(`${dropletAccessCommand} root@${this.ip}  "${command}"`, { stdio: [0, 1, 2] });
    console.log(`"${command}" executed!`);
    return String(output);
  }

  executeCommandAndGetOutput(command) {
    return new Promise((resolve, reject) => {
      childProcess.exec(`${dropletAccessCommand} root@${this.ip}  "${command}"`, (err, stdout) => {
        console.log(`"${command}" executed!`);
        if (err)
          reject(err);
        else
          resolve(stdout);
      });

    });
  }

}

module.exports = { Droplet, dropletAccessCommand };
