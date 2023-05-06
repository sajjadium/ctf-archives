function makeGaugeInstance(id) {
  var opts = {
    angle: -0.22, // The span of the gauge arc
    lineWidth: 0.18, // The line thickness
    radiusScale: 1, // Relative radius
    pointer: {
      length: 0.5, // // Relative to gauge radius
      strokeWidth: 0.062, // The thickness
      color: '#000000' // Fill color
    },
    limitMax: false,     // If false, max value increases automatically if value > maxValue
    limitMin: false,     // If true, the min value of the gauge will be fixed
    colorStart: '#6F6EA0',   // Colors
    colorStop: '#C0C0DB',    // just experiment with them
    strokeColor: '#EEEEEE',  // to see which ones work best for you
    generateGradient: true,
    highDpiSupport: true,     // High resolution support
    // renderTicks is Optional
    renderTicks: {
      divisions: 4,
      divWidth: 1.3,
      divLength: 0.61,
      divColor: '#333333',
      subDivisions: 2,
      subLength: 0.55,
      subWidth: 0.6,
      subColor: '#666666'
    },
    staticLabels: {
      font: "9px sans-serif",  // Specifies font
      labels: [25, 50, 75],  // Print labels at these values
      color: "#000000",  // Optional: Label text color
      fractionDigits: 0  // Optional: Numerical precision. 0=round off.
    },
    staticZones: [
      {strokeStyle: "#30B32D", min: 0, max: 30}, // Green
      {strokeStyle: "#FFDD00", min: 30, max: 70}, // Yellow
      {strokeStyle: "#F03E3E", min: 70, max: 100}  // Red
    ],
  };
  var target = document.getElementById(id); // your canvas element
  var gauge = new Gauge(target).setOptions(opts); // create sexy gauge!
  gauge.maxValue = 100; // set max gauge value
  gauge.setMinValue(0);  // Prefer setter over gauge.minValue = 0
  gauge.animationSpeed = 31; // set animation speed (32 is default value)
  return gauge;
}


new Vue({
  el: '#app',
  delimiters: ['##', '##'],
  data: {
    system_information: false,
    instances: {
      cpu: false,
      ram: false
    }
  },
  methods: {
    formatPercentage(value) {
      return parseFloat(value).toFixed(2);
    },
    getSystemInformation() {
      fetch("/api/system_info", {
        method: "POST"
      }).then(d => d.json()).then(system_information => {
        this.system_information = system_information;
        console.log(this.system_information);
        this.instances.cpu.set(this.system_information.cpu_usage);
        this.instances.ram.set(this.system_information.ram_usage);
      })
    }
  },
  mounted() {
    this.instances.cpu = makeGaugeInstance("cpu");
    this.instances.ram = makeGaugeInstance("ram");
    this.getSystemInformation();
    setInterval(this.getSystemInformation, 10000);
  }
})