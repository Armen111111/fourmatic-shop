// Рендер всех SVG из папки в PNG через Playwright/Chromium.
// Размер PNG берётся из атрибутов width/height корневого <svg>.
// Запуск: NODE_PATH=$(npm root -g) node brand/tools/render.js <папка_svg> <папка_png>
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");

const [srcDir, outDir] = process.argv.slice(2).map((p) => path.resolve(p));
if (!srcDir || !outDir) {
  console.error("usage: node render.js <svg_dir> <png_dir>");
  process.exit(1);
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  fs.mkdirSync(outDir, { recursive: true });
  for (const file of fs.readdirSync(srcDir).filter((f) => f.endsWith(".svg")).sort()) {
    const svg = fs.readFileSync(path.join(srcDir, file), "utf8");
    const root = svg.match(/<svg[^>]*>/)[0];
    const w = +root.match(/ width="(\d+(?:\.\d+)?)"/)[1];
    const h = +root.match(/ height="(\d+(?:\.\d+)?)"/)[1];
    const W = Math.round(w), H = Math.round(h);
    await page.setViewportSize({ width: W, height: H });
    await page.setContent(`<html><body style="margin:0">${svg}</body></html>`);
    const out = path.join(outDir, file.replace(/\.svg$/, ".png"));
    await page.screenshot({ path: out, omitBackground: true, clip: { x: 0, y: 0, width: W, height: H } });
    console.log("rendered", path.relative(process.cwd(), out), `${W}×${H}`);
  }
  await browser.close();
})();
