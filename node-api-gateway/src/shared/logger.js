import * as log4js from 'log4js';

log4js.configure({
  appenders: {
    apiGateway: { type: 'file', filename: './logs/requests.log' },
    console: { type: 'console' }
  },
  categories: {
    default: {
      appenders: ['console', 'apiGateway'],
      level: process.env.LOG_LEVEL // level: 'ALL'
    }
  }
});

export const logger = log4js.getLogger('apiGateway');
