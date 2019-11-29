import httpProxy from 'express-http-proxy';
import { proxyConfig } from './proxy';

export const AuthRoute = httpProxy(process.env.AUTH_URL, proxyConfig);
export const AccountRoute = httpProxy(process.env.ACCOUNT_URL, proxyConfig);
export const RssRoute = httpProxy(process.env.RSS_URL, proxyConfig);
