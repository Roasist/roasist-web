import http from 'http';
import fs from 'fs';
import path from 'path';
import { chromium } from 'playwright';

const PUBLIC_DIR = '/home/antigravity/Roasist/roasist-web/public';

const mimeTypes = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.woff2': 'font/woff2',
  '.mp4': 'video/mp4'
};

const server = http.createServer((req, res) => {
  let reqPath = req.url.split('?')[0];
  if (reqPath === '/' || reqPath === '/index.html') reqPath = '/kota-roasist-local.html';
  const filePath = path.join(PUBLIC_DIR, reqPath);
  if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
    const ext = path.extname(filePath);
    res.writeHead(200, { 'Content-Type': mimeTypes[ext] || 'application/octet-stream' });
    fs.createReadStream(filePath).pipe(res);
  } else {
    res.writeHead(404);
    res.end('Not found');
  }
});

server.listen(4568, async () => {
  const browser = await chromium.launch({
    executablePath: '/usr/bin/chromium',
    args: ['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader']
  });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errors = [];
  page.on('pageerror', err => errors.push(err.message));

  await page.goto('http://localhost:4568/', { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(3000);
  await page.screenshot({ path: '/tmp/kota_verify_hero_v2.png' });

  // Scroll to First Service Card (Web tasarım & geliştirme)
  await page.evaluate(() => {
    const el = document.querySelector('.ServicesPanel_panel__YF4OS');
    if (el) el.scrollIntoView({ behavior: 'instant', block: 'center' });
  });
  await page.waitForTimeout(2000);
  await page.screenshot({ path: '/tmp/kota_verify_services_v2.png' });

  // Scroll to Approach (01 / 02 / 03)
  await page.evaluate(() => {
    const el = document.querySelector('.Approach_approach__kHR9Y');
    if (el) el.scrollIntoView({ behavior: 'instant', block: 'center' });
  });
  await page.waitForTimeout(1500);
  await page.screenshot({ path: '/tmp/kota_verify_approach_v2.png' });

  console.log('Errors:', errors);
  await browser.close();
  server.close();
});
