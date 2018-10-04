const fs = require('fs');

const dirname = 'logs/'; //your folder path (views is an example folder)
const jsonpath = 'time.json';
let payload = [];
let changed = null;
let json = JSON.parse(fs.readFileSync(jsonpath).toString('utf8'));
let errors = [];

function getRst(data, first = false, act = false) {
  if (first) {
    errors.push({
      msg: 'no data yet'
    });
    if (act) {
      errors.push({
        msg: 'generating new json'
      });
    }
  } else {
    if (!!data.length && data.length !== json.length) {
      errors.push({
        matchTime: Date.now().toLocaleString(),
        msg: 'missing messages, only records were updated',
        records: data
      });
    } else if (!data.length || data.length === json.length) {
      errors.push({
        msg: 'all messages were delivered'
      });
    }
  }
  console.log(JSON.stringify(errors, null, 2));
}
readFiles(dirname, getRst);


function readFiles(dirname, cb) {

  fs.readdir(dirname, async (err, files) => {
    if (err) {
      console.error(err);
      return;
    }
    payload = await Promise.all(files.map(file => {
      let r = undefined;
      r = fs.statSync(dirname + file)
      return {
        name: file,
        mtime: r.mtime.toLocaleString()
      };
    }));
    if (!json.length) {
      recordMtime(payload);
      cb([], true);
    } else if (payload.length > json.length) {
      setNewJson(payload);
      cb([], true, true);
    } else {
      changed = match(payload, json);
      recordMtime(payload);
      cb(changed);
    }
  });
}

function setNewJson(payload) {
  fs.writeFileSync(jsonpath, JSON.stringify(payload, null, 2));
}

function match(payload, json) {
  let newer = payload.filter((e, i) => {
    if (json[i].mtime < e.mtime) {
      return e;
    }
  });

  return newer;
}

function recordMtime(payload) {
  fs.writeFileSync(jsonpath, JSON.stringify(payload, null, 2));
}
