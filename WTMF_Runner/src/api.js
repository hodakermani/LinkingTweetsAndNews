const request = require('request');
const config = require('../config');

function createDroplet() {
  return new Promise((resolve, reject) => {
    request.post({
      url: 'https://api.digitalocean.com/v2/droplets',
      headers: {
        'Authorization': `Bearer ${config.token}`
      },
      json: {
        'name': 'W1',
        'region': config.region,
        'size': config.size,
        'image': 'ubuntu-16-04-x64',
        'ssh_keys': ['a4:6f:7d:33:42:9e:46:03:10:99:92:d1:24:60:cb:40'],
        'backups': false,
        'ipv6': true,
        'user_data': null,
        'private_networking': null,
        'volumes': null,
        'tags': ['WTMFG']
      }
    }, function optionalCallback(err, httpResponse, body) {
      if (err)
        return reject(err);
      if(body.message)
        return reject(body);
      console.log('New droplet created!');
      resolve(body);
    });
  });
}

function getDropletsListByTag() {
  return new Promise((resolve, reject) => {
    request.get({
      url: 'https://api.digitalocean.com/v2/droplets/?tag_name=WTMFG',
      headers: {
        'Authorization': `Bearer ${config.token}`
      }
    }, function optionalCallback(err, httpResponse, body) {
      if (err)
        reject(err);
      body = JSON.parse(body);
      if (body.droplets.length === 0)
        resolve(null);
      else
        resolve(body.droplets);
    });
  });
}

function getDropletIdByTag() {
  return new Promise((resolve, reject) => {
    request.get({
      url: 'https://api.digitalocean.com/v2/droplets/?tag_name=WTMFG',
      headers: {
        'Authorization': `Bearer ${config.token}`
      }
    }, function optionalCallback(err, httpResponse, body) {
      if (err)
        reject(err);
      body = JSON.parse(body);
      if (body.droplets.length === 0)
        resolve(null);
      else
        resolve(body.droplets[0].id);
    });
  });
}

function getDropletDetails(id) {
  return new Promise((resolve, reject) => {
    request.get({
      url: `https://api.digitalocean.com/v2/droplets/${id}`,
      headers: {
        'Authorization': `Bearer ${config.token}`
      }
    }, function optionalCallback(err, httpResponse, body) {
      if (err)
        reject(err);
      resolve(JSON.parse(body));
    });
  });
}

function deleteDroplet(id) {
  return new Promise((resolve, reject) => {
    request.delete({
      url: `https://api.digitalocean.com/v2/droplets/${id}`,
      headers: {
        'Authorization': `Bearer ${config.token}`
      }
    }, function optionalCallback(err, httpResponse, body) {
      if (err)
        reject(err);
      console.log('Droplet deleted!');
      resolve(body);
    });
  });
}

module.exports = {
  createDroplet, deleteDroplet, getDropletDetails, getDropletIdByTag, getDropletsListByTag
};