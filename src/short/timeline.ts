import { config, TransitionSpec } from "./config";
import type { Edl, FaceFrame, Transcript } from "./types";

export type Clip = {
  index: number;
  // Source frame range actually played (includes transition handles).
  srcFrom: number;
  srcTo: number;
  // Source frame range of the EDL's kept speech (no handles) - words map into this.
  keepFrom: number;
  keepTo: number;
  durationInFrames: number;
  outStart: number; // first output frame
  zoom: number; // punch-in level for this clip
  prevZoom: number;
  transitionIn: TransitionSpec | null;
};

export type TimedWord = {
  text: string;
  key: string; // normalised, for keyword / phrase matching
  startFrame: number; // output frames
  endFrame: number;
};

export type Timeline = {
  clips: Clip[];
  words: TimedWord[];
  durationInFrames: number;
};

export const normalise = (s: string) => s.toLowerCase().replace(/[^a-z0-9']/g, "");

export const buildTimeline = (edl: Edl, transcript: Transcript): Timeline => {
  const { fps } = config;
  const kept = edl.segments.filter((s) => s.keep);

  const clips: Clip[] = kept.map((s, i) => {
    const keepFrom = Math.round(s.start * fps);
    const keepTo = Math.round(s.end * fps);
    const zoom = i % 2 === 1 ? config.punchIn.zoom : 1;
    return {
      index: i,
      srcFrom: keepFrom,
      srcTo: keepTo,
      keepFrom,
      keepTo,
      durationInFrames: keepTo - keepFrom,
      outStart: 0,
      zoom,
      prevZoom: i === 0 ? zoom : i % 2 === 1 ? 1 : config.punchIn.zoom,
      transitionIn: null,
    };
  });

  // Attach each configured transition to the cut whose removed gap contains it,
  // and give both sides handles from that gap so voices never overlap mid-transition.
  for (const t of config.transitions) {
    const tf = t.atSourceTime * fps;
    const i = clips.findIndex(
      (c, k) => k + 1 < clips.length && c.keepTo <= tf + 1 && clips[k + 1].keepFrom >= tf - 1,
    );
    if (i === -1) {
      console.warn(`No cut found at source ${t.atSourceTime}s - transition ignored`);
      continue;
    }
    const a = clips[i];
    const b = clips[i + 1];
    const gap = b.keepFrom - a.keepTo;
    const half = Math.min(Math.ceil(t.durationInFrames / 2), Math.floor(gap / 2));
    const duration = Math.min(t.durationInFrames, half * 2 || t.durationInFrames);
    a.srcTo = a.keepTo + half;
    b.srcFrom = b.keepFrom - half;
    b.transitionIn = { ...t, durationInFrames: duration };
  }

  let cursor = 0;
  for (const c of clips) {
    c.durationInFrames = c.srcTo - c.srcFrom;
    if (c.transitionIn) cursor -= c.transitionIn.durationInFrames;
    c.outStart = cursor;
    cursor += c.durationInFrames;
  }
  const durationInFrames = cursor;

  // Map words into output time; words inside cut segments (fillers) are dropped.
  const words: TimedWord[] = [];
  for (const w of transcript.words) {
    const mid = ((w.start + w.end) / 2) * fps;
    const c = clips.find((cl) => mid >= cl.keepFrom && mid < cl.keepTo);
    if (!c) continue;
    const toOut = (srcFrame: number) =>
      c.outStart + (Math.min(Math.max(srcFrame, c.srcFrom), c.srcTo) - c.srcFrom);
    const text = config.captions.corrections[w.text] ?? w.text;
    words.push({
      text,
      key: normalise(text),
      startFrame: Math.round(toOut(w.start * fps)),
      endFrame: Math.max(Math.round(toOut(w.end * fps)), Math.round(toOut(w.start * fps)) + 2),
    });
  }

  return { clips, words, durationInFrames };
};

// Centred moving average of face centre + size, per source frame.
export const smoothFaces = (frames: FaceFrame[], window: number) => {
  const half = Math.floor(window / 2);
  const cx = frames.map((f) => f.x + f.w / 2);
  const cy = frames.map((f) => f.y + f.h / 2);
  const avg = (arr: number[], i: number) => {
    let sum = 0;
    let n = 0;
    for (let k = Math.max(0, i - half); k <= Math.min(arr.length - 1, i + half); k++) {
      sum += arr[k];
      n++;
    }
    return sum / n;
  };
  return frames.map((_, i) => ({ x: avg(cx, i), y: avg(cy, i) }));
};

// Output-frame speech mask -> ducked music volume with attack/release ramps.
export const musicVolumes = (words: TimedWord[], durationInFrames: number) => {
  const m = config.music;
  const speech = new Uint8Array(durationInFrames);
  const merge = Math.round(m.speechMergeGapSeconds * config.fps);
  for (let i = 0; i < words.length; i++) {
    const from = Math.max(0, words[i].startFrame - m.attackFrames); // duck slightly early
    const next = words[i + 1];
    const to = next && next.startFrame - words[i].endFrame <= merge ? next.startFrame : words[i].endFrame;
    for (let f = from; f < Math.min(durationInFrames, to); f++) speech[f] = 1;
  }
  const range = m.fullVolume - m.duckedVolume;
  const out = new Array<number>(durationInFrames);
  let v = speech[0] ? m.duckedVolume : m.fullVolume;
  for (let f = 0; f < durationInFrames; f++) {
    const target = speech[f] ? m.duckedVolume : m.fullVolume;
    const step = target < v ? range / m.attackFrames : range / m.releaseFrames;
    v = target < v ? Math.max(target, v - step) : Math.min(target, v + step);
    // short fade in/out at the very ends
    const edge = Math.min(1, f / 6, (durationInFrames - 1 - f) / 20);
    out[f] = v * Math.max(0, edge);
  }
  return out;
};
