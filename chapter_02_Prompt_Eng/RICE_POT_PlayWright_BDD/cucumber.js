const dotenv = require('dotenv');
const fs = require('fs');

dotenv.config();

const reportPath = process.env.REPORT_PATH || 'reports';
fs.mkdirSync(reportPath, { recursive: true });

const defaultConfig = {
  requireModule: ['ts-node/register'],
  require: ['src/steps/**/*.ts', 'src/hooks/**/*.ts'],
  paths: ['src/features/**/*.feature'],
  format: [
    'progress-bar',
    `html:${reportPath}/cucumber-report.html`,
    `json:${reportPath}/cucumber-report.json`,
  ],
  formatOptions: { snippetInterface: 'async-await' },
  publishQuiet: true,
  parallel: parseInt(process.env.PARALLEL_WORKERS || '1', 10),
  retry: parseInt(process.env.RETRIES || '0', 10),
};

if (process.env.CUCUMBER_TAGS) {
  defaultConfig.tags = process.env.CUCUMBER_TAGS;
}

module.exports = { default: defaultConfig };
