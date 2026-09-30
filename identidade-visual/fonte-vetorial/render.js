// Render SVG files to PNG (transparent) or PDF (vector) with headless Chromium.
// usage: node render.js manifest.json
// manifest: [{ "svg": "a.svg", "png": "a.png", "width": 1200 } | { "svg": "a.svg", "pdf": "a.pdf" } | { "html": "x.html", "png": "x.png", "width": 1200, "height": 800 }]
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await chromium.launch();
  const page = await browser.newPage({ deviceScaleFactor: 1 });
  for (const j of jobs) {
    if (j.html) {
      await page.setViewportSize({ width: j.width, height: j.height });
      await page.goto('file://' + path.resolve(j.html));
      await page.waitForTimeout(150);
      await page.screenshot({ path: j.png, omitBackground: !!j.transparent });
      continue;
    }
    const svg = fs.readFileSync(j.svg, 'utf8');
    const m = svg.match(/viewBox="([\d.\-]+) ([\d.\-]+) ([\d.]+) ([\d.]+)"/);
    const vw = parseFloat(m[3]), vh = parseFloat(m[4]);
    if (j.png) {
      const w = j.width || 1000;
      const h = Math.round(w * vh / vw);
      await page.setViewportSize({ width: w, height: h });
      const bg = j.bg ? `background:${j.bg};` : 'background:transparent;';
      await page.setContent(`<html><body style="margin:0;${bg}">${svg.replace('<svg ', `<svg width="${w}" height="${h}" style="display:block" `)}</body></html>`);
      await page.screenshot({ path: j.png, omitBackground: !j.bg, clip: { x: 0, y: 0, width: w, height: h } });
    }
    if (j.pdf) {
      // 1 SVG unit = 1 CSS px; keep aspect, vector output
      const w = j.pdfWidth || vw, h = w * vh / vw;
      await page.setContent(`<html><head><style>@page{size:${w}px ${h}px;margin:0}html,body{margin:0}</style></head><body>${svg.replace('<svg ', `<svg width="${w}" height="${h}" style="display:block" `)}</body></html>`);
      await page.pdf({ path: j.pdf, width: `${w}px`, height: `${h}px`, printBackground: true, pageRanges: '1' });
    }
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
