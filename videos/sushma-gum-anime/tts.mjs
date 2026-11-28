// Indian-English narration with Kokoro's Hindi female voice (hf_beta) but English phonemes, so the line edges stay clean.
//   node tts_indian.mjs lines.tsv outdir   (tsv: start<TAB>end<TAB>text) -> outdir/l<N>.wav
import fs from 'node:fs'; import path from 'node:path';
const EX = '/home/user/remotion-/tools/skill-repos/vincentsch_explainroo';
const { loadTTS, TTS_SAMPLE_RATE } = await import(path.join(EX, 'src/models.js'));
const { writeWav } = await import(path.join(EX, 'src/wav.js'));
const { phonemize } = await import(path.join(EX, 'node_modules/phonemizer/dist/phonemizer.js')).catch(() => import(path.join(EX, 'node_modules/phonemizer/index.js')));
const [tsv, out, voice = 'hf_beta', lang = 'en-us'] = process.argv.slice(2);
const tts = await loadTTS({ log: () => {} });
const lines = fs.readFileSync(tsv, 'utf8').trim().split('\n').map(l => l.split('\t')[2]);
let i = 0;
for (const text of lines) {
  i++;
  const ph = (await phonemize(text, lang)).join(' ').replace(/ʲ/g, 'j').replace(/r/g, 'ɹ').replace(/x/g, 'k').replace(/ɬ/g, 'l').trim()
    .replace('sɹˌiː sˈʌʃmə', 'ʃɹˈiː sˈʊʃmaː').replace(/m[ˈ]?oʊ[ɾt]i/g, 'mˈoːtiː');   // Indian pronunciation of the doctor's name: Shree Sush-maa
  const { input_ids } = tts.tokenizer(ph, { truncation: true });
  const audio = await tts.generate_from_ids(input_ids, { voice, speed: 1 });
  writeWav(path.join(out, `l${i}.wav`), audio.audio, audio.sampling_rate || TTS_SAMPLE_RATE);
  console.log(i, ph);
}
