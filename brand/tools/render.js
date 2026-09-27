// Рендер SVG из brand/svg в PNG (brand/png) через Playwright/Chromium.
// Запуск: NODE_PATH=$(npm root -g) node brand/tools/render.js
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");

const root = path.resolve(__dirname, "..");
const jobs = [
  // [svg, png, ширина, высота]
  ["zapkit-avatar.svg", "zapkit-avatar-1024.png", 1024, 1024],
  ["zapkit-avatar-dark.svg", "zapkit-avatar-dark-1024.png", 1024, 1024],
  ["zapkit-mark.svg", "zapkit-mark-512.png", 512, 512],
  ["zapkit-logo-dark.svg", "zapkit-logo-dark.png", 1340, 268],
  ["zapkit-logo-light.svg", "zapkit-logo-light.png", 1340, 268],
  ["zapkit-logo-on-yellow.svg", "zapkit-logo-on-yellow.png", 1340, 268],
  ["zapkit-lockup-dark.svg", "zapkit-lockup-dark.png", 1340, 372],
  ["zapkit-lockup-light.svg", "zapkit-lockup-light.png", 1340, 372],
  ["avito-cover.svg", "avito-cover-1920x640.png", 1920, 640],
  ["kit-card-example.svg", "kit-card-example-1200x900.png", 1200, 900],
];

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  fs.mkdirSync(path.join(root, "png"), { recursive: true });
  for (const [src, out, w, h] of jobs) {
    const svg = fs.readFileSync(path.join(root, "svg", src), "utf8");
    await page.setViewportSize({ width: w, height: h });
    await page.setContent(`<html><body style="margin:0">${svg}</body></html>`);
    await page.screenshot({ path: path.join(root, "png", out), omitBackground: true, clip: { x: 0, y: 0, width: w, height: h } });
    console.log("rendered", out);
  }
  await browser.close();
})();
