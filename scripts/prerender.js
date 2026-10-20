// Renders the page, then bakes the calculator's default output into the HTML so it shows without JavaScript.
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const file = require('path').join(__dirname,'..','src','protocol.html');
  let src = fs.readFileSync(file, 'utf8');
  const strip = (k) => { src = src.replace(new RegExp(`<!--pre:${k}-->[\\s\\S]*?<!--/pre:${k}-->`), `<!--pre:${k}--><!--/pre:${k}-->`); };
  ['list','summary','limits','serving'].forEach(strip);
  fs.writeFileSync(file, src);
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + file); await p.waitForTimeout(400);
  const out = await p.evaluate(() => ({
    list: document.getElementById('list').innerHTML,
    summary: document.getElementById('summary').innerHTML,
    serving: document.getElementById('serving').innerHTML,
    limits: document.getElementById('limits').innerHTML,
  }));
  await b.close();
  for (const k of ['list','summary','limits','serving']) {
    const v = out[k].replace(/<!--\/?pre:\w+-->/g, '');
    src = src.replace(`<!--pre:${k}--><!--/pre:${k}-->`, `<!--pre:${k}-->${v}<!--/pre:${k}-->`);
  }
  fs.writeFileSync(file, src);
  console.log('baked', out.list.length, out.limits.length, out.serving.length);
})();
