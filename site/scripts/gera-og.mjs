/** Gera public/og.png (1200x630): wordmark da marca centrado sobre fundo Breu. */
import sharp from "sharp";

const wordmark = await sharp("../marca/wordmark-escuro.svg", { density: 300 })
  .resize({ width: 840 })
  .png()
  .toBuffer();

await sharp({
  create: { width: 1200, height: 630, channels: 4, background: "#0a0a09" },
})
  .composite([{ input: wordmark, gravity: "center" }])
  .png()
  .toFile("public/og.png");

console.log("public/og.png gerado");
