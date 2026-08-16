import dotenv from 'dotenv';
import path from 'path';

dotenv.config({ path: path.resolve(process.cwd(), '.env') });

export const config = {
  baseUrl: process.env.BASE_URL ?? 'https://login.salesforce.com/?locale=in',
  username: process.env.SF_USERNAME ?? '',
  password: process.env.SF_PASSWORD ?? '',
  browser: (process.env.BROWSER ?? 'chromium') as 'chromium' | 'firefox' | 'webkit',
  headless: (process.env.HEADLESS ?? 'true') !== 'false',
  env: process.env.ENV ?? 'qa',
  defaultTimeout: parseInt(process.env.DEFAULT_TIMEOUT ?? '30000', 10),
  navigationTimeout: parseInt(process.env.NAVIGATION_TIMEOUT ?? '60000', 10),
  parallelWorkers: parseInt(process.env.PARALLEL_WORKERS ?? '1', 10),
  retries: parseInt(process.env.RETRIES ?? '0', 10),
  screenshotOnFailure: (process.env.SCREENSHOT_ON_FAILURE ?? 'true') !== 'false',
  video: process.env.VIDEO ?? 'off',
  trace: process.env.TRACE ?? 'off',
  reportPath: process.env.REPORT_PATH ?? 'reports',
  logLevel: process.env.LOG_LEVEL ?? 'info',
};
