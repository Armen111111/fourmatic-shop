// Рендер SVG из brand/svg в PNG (brand/png) через Playwright/Chromium.
// Запуск: NODE_PATH=$(npm root -g) node brand/tools/render.js
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");

const root = path.resolve(__dirname, "..");
const jobs = [
  // [svg, png, ширина, высота]
  ["vporu-avatar.svg", "vporu-avatar-1024.png", 1024, 1024],
  ["vporu-avatar-dark.svg", "vporu-avatar-dark-1024.png", 1024, 1024],
  ["vporu-mark.svg", "vporu-mark-512.png", 512, 512],
  ["vporu-wordmark-dark.svg", "vporu-wordmark-dark.png", 1736, 512],
  ["vporu-wordmark-light.svg", "vporu-wordmark-light.png", 1736, 512],
  ["vporu-lockup-dark.svg", "vporu-lockup-dark.png", 1736, 688],
  ["vporu-lockup-light.svg", "vporu-lockup-light.png", 1736, 688],
  ["avito-cover.svg", "avito-cover-1920x640.png", 1920, 640],
];

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  fs.mkdirSync(path.join(root, "png"), { recursive: true });
  for (const [src, out, w, h] of jobs) {
    const svg = fs.readFileSync(path.join(root, "svg", src), "utf8");
    await page.setViewportSize({ width: w, height: h });
    await page.setContent(
      `<html><body style="margin:0">${svg.replace(/width="\d+" height="\d+"/, `width="${w}" height="${h}"`)}</body></html>`
    );
    await page.screenshot({ path: path.join(root, "png", out), omitBackground: true, clip: { x: 0, y: 0, width: w, height: h } });
    console.log("rendered", out);
  }
  await browser.close();
})();
