const main = '5740ff9a8615fc4ce6b75027f99ab889548ffb99c332122e38426e0444786049';
const dev = '5d35c8e8304d8a26dca8d4b39f75c0e66a14c043f463b5c41edccad05bbd28ed';

const core2 = '2gb';
const core32 = 'c-32';

const newYork = 'nyc1';
module.exports = {
  serverDestroyTimeout: 3,
  size: core32,
  token: main,
  region: newYork,
  outputPath: 'out.log',
  localDirectory: process.env["LOCAL_DIR"]
};
