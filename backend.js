var events = require('events');
var eventEmitter = new events.EventEmitter();

eventEmitter.on('scream',function(){
    console.log('Im Screaming');
});

eventEmitter.on('hello', function(){
    console.log('Just a lil hello');
});

eventEmitter.emit('scream');
eventEmitter.emit('hello');
