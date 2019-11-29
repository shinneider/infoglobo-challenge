import sls from 'serverless-http';
import { config } from 'dotenv-flow';
config();

import app from './app';

export const handler = sls(app);
