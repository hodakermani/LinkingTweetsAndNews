module.exports = {
  remoteRunner: {
    start: '############################### Remote Runner ###############################',
    invalidCommandMessage: 'Invalid Command!\nAvailable commands:\n\t deploy: Deploy' +
    '\n\t recreate: Create droplet again\n\t destroy: Destroy droplet ' +
    '\n\t tail: Print tail of output file\n\t run: Run the test' +
    '\n\t ip: get droplet ip\n\t kill: Kill the running test'
  },
  localRunner: {
    start: '############################### Local Runner ###############################',
    invalidCommandMessage: 'Invalid Command!\nAvailable commands:\n\t install: install' +
    '\n\t run [num of threads] : Run test with specified num of threads'
  },
  command: {
    start: '--------------------------------- Running ---------------------------------',
    end:   '---------------------------------- Done -----------------------------------'
  }
};