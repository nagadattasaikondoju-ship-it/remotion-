// node tts.mjs <outdir> <voice> <phonemeLang a|b> <speed> <text|@file.json>
// Kokoro (local ONNX). The voice file can be any of the bundled embeddings; the phoneme language is chosen separately.
import fs from "node:fs";
const ER = process.env.EXPLAINROO_NODE_MODULES || "/home/user/remotion-/tools/skill-repos/vincentsch_explainroo/node_modules";
const T = await import(ER + "/@huggingface/transformers/dist/transformers.node.mjs").catch(() => import(ER + "/@huggingface/transformers/src/transformers.js"));
T.env.cacheDir = "/root/.cache/explainroo/models"; T.env.allowRemoteModels = false;
const { KokoroTTS } = await import(ER + "/kokoro-js/dist/kokoro.js");
const [out, voice, lang, speed, text] = process.argv.slice(2);
const tts = await KokoroTTS.from_pretrained("onnx-community/Kokoro-82M-v1.0-ONNX", { dtype: "fp32", device: "cpu" });
tts._validate_voice = () => lang;
const items = text.startsWith("@") ? JSON.parse(fs.readFileSync(text.slice(1), "utf8")) : [{ id: voice, text }];
for (const it of items) { const a = await tts.generate(it.text, { voice, speed: Number(speed) }); await a.save(`${out}/${it.id}.wav`); console.log(it.id, (a.audio.length / 24000).toFixed(2)); }
