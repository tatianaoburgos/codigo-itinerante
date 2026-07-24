/** Gera public/favicon-32.png (fallback do favicon.svg) e public/apple-touch-icon.png
 * (monograma sobre fundo Breu, mesmo padrão de gera-og.mjs). */
import sharp from "sharp";

await sharp("public/favicon.svg", { density: 384 })
  .resize({ width: 32, height: 32, fit: "contain", background: { r: 0, g: 0, b: 0, alpha: 0 } })
  .png()
  .toFile("public/favicon-32.png");

const monograma = await sharp("../marca/monograma-escuro.svg", { density: 300 })
  .resize({ width: 120 })
  .png()
  .toBuffer();

await sharp({
  create: { width: 180, height: 180, channels: 4, background: "#0a0a09" },
})
  .composite([{ input: monograma, gravity: "center" }])
  .png()
  .toFile("public/apple-touch-icon.png");

console.log("public/favicon-32.png e public/apple-touch-icon.png gerados");
