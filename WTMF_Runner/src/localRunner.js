const childProcess = require('child_process');
const config = require('../config');

class RemoteRunner {
    static install() {
        return new Promise(async (resolve, reject) => {
            try {
                childProcess.execSync(`source scripts/local/install.sh`, {
                    env: {
                        'HOME': process.env["HOME"],
                        'LOCAL_DIR': config.localDirectory,
                        'ROOT_DIR': `${config.localDirectory}/acl2013`,
                        'SCRIPTS_DIR': `${config.localDirectory}/acl2013/scripts`
                    }, stdio: [0, 1, 2]
                });
                resolve();
            } catch (error) {
                console.log(error);
                console.log('error');
                reject(error);
            }
        });
    }

    static run(numOfProcessors) {
        return new Promise(async (resolve, reject) => {
            try {
                childProcess.execSync(`source scripts/local/run.sh`, {
                    env: {
                        'LOCAL_DIR': config.localDirectory,
                        'ROOT_DIR': `${config.localDirectory}/acl2013`,
                        'SCRIPTS_DIR': `${config.localDirectory}/acl2013/scripts`
                    }, stdio: [0, 1, 2]
                });
                resolve();
            } catch (error) {
                console.log(error);
                console.log('error');
                reject(error);
            }
        });
    }

    static htop() {
        return new Promise(async (resolve, reject) => {
            try {
                let droplet = await Droplet.getInstance();
                console.log('Waiting for droplet to get ready ...');
                await droplet.waitUntilBecomeAvailable();
                console.log('Waiting for droplet to get ready ...');
                droplet.executeCommand('htop');
                resolve();
            } catch (error) {
                reject(error);
            }
        });
    }

    static jupyter() {
        return new Promise(async (resolve, reject) => {
            try {
                let droplet = await Droplet.getInstance();
                console.log('Waiting for droplet to get ready ...');
                await droplet.waitUntilBecomeAvailable();
                console.log('Droplet IP: ', droplet.ip);
                console.log('Waiting for droplet to get ready ...');
                droplet.executeCommand('source ./scripts/jupyter.sh');
                resolve();
            } catch (error) {
                reject(error);
            }
        });
    }

}

module.exports = RemoteRunner;