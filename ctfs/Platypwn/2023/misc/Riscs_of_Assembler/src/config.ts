export type Config = {
  tempPath: string;
  port: number;
  challengePath: string;
  ripesPath: string;
};

const config: Config = {
  tempPath: process.env.TEMP_PATH || "tmp",
  port: parseInt(process.env.PORT || "3000"),
  challengePath: process.env.TASK_PATH || "./challenges",
  ripesPath: process.env.RIPES_PATH || "./lib/ripes",
};

export default config;
