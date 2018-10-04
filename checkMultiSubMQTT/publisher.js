const mqtt = require('mqtt');
const client = mqtt.connect('mqtt://{ip}:1883');
let payload = JSON.stringify({
  anything: 'youwant'
});

client.on('connect', err => {
  client.publish('multi', payload, {
    qos: 2,
    retain: false,
    dup: false
  }, err => {
    if (err) {
      throw new Error(err);
    }
  });
  client.end();
});

client.on('packetreceive', packet => {
  if (packet.cmd === 'pubcomp') {
    console.log('success');
  }
});
