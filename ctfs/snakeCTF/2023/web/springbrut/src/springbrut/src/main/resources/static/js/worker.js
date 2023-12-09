const setMetric = (name) => {
  fetch(`/actuator/metrics/${name}`).then(res => res.json()).then(json => {
    console.log({json});
    self.postMessage({name, value: json.measurements[0].value});
  });
};
const updateAll = () => {
  console.log('updating...');
  setMetric('disk.free');
  setMetric('http.server.requests');
  setMetric('process.cpu.usage');
  setMetric('system.load.average.1m');
  setMetric('process.uptime');
};
updateAll();
setTimeout(updateAll, 1000);