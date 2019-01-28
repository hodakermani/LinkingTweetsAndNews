const main = require('./src/main');

let mainMethod = main.remote;

if (process.argv[2] === 'local')
  mainMethod = main.local;

mainMethod();