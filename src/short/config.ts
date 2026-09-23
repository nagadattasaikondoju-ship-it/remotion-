// Everything creative lives here: brand, copy, timings, which cuts get transitions.
// Times in `transitions` are SOURCE seconds (as in source.edl.json); everything
// else that is time-based is resolved against the edited output.

export const config = {
  fps: 30,
  width: 1080,
  height: 1920,

  media: {
    video: "media/source.mp4",
    edl: "media/source.edl.json",
    words: "media/source.words.json",
    faces: "media/source.faces.json",
  },

  accent: "#FF3B30",

  hook: {
    headline: ["Playing it safe", "erases brands"],
    tagline: "Be impossible to ignore",
    durationInFrames: 72,
  },

  lowerThird: {
    // Placeholder from the repo owner's GitHub profile - change to the speaker.
    name: "Naga Datta",
    title: "Product Manager · Oneloop",
    fromSeconds: 4.2, // output time
    durationInSeconds: 3.6,
  },

  captions: {
    maxWords: 4,
    minWords: 2,
    maxChars: 24,
    // Words (lower-case, no punctuation) drawn in the accent colour with a bigger pop.
    keywords: [
      "career", "millions", "collapsed", "overnight", "bigger", "nobody",
      "safe", "erases", "remember", "careful", "scared", "opposite",
      "impossible", "ignore", "remembered", "scrolled",
    ],
    // Fix mis-heard words without touching the transcript file.
    corrections: { "Dub.": "that." } as Record<string, string>,
  },

  // Kinetic number pop-ins, triggered when `phrase` is spoken.
  stats: [
    { phrase: "three weeks", value: 3, unit: "WEEKS", label: "career on pause" },
    { phrase: "millions of followers", text: "MILLIONS", label: "of followers" },
    { phrase: "one month later", value: 1, unit: "MONTH", label: "later: bigger than before" },
  ] as StatSpec[],

  // Explicit transitions on chosen cuts (Remotion can't find match points itself).
  // `atSourceTime` = any time inside the removed gap between the two clips.
  transitions: [
    { atSourceTime: 19.3, type: "whip", durationInFrames: 10 }, // "...It erases it" -> "The brands people remember"
    { atSourceTime: 28.3, type: "crossfade", durationInFrames: 14 }, // "...everyone else was scared" -> "So when a brand comes to us"
  ] as TransitionSpec[],

  punchIn: { zoom: 1.15, frames: 8 },

  face: {
    baseZoom: 1.12, // headroom so the frame can pan to follow the face
    targetX: 0.5, // where the face centre should sit in the output (0-1)
    targetY: 0.36,
    smoothingWindow: 21, // source frames in the moving average (~0.7s)
  },

  music: {
    src: "media/music.wav",
    fullVolume: 0.35,
    duckedVolume: 0.07,
    attackFrames: 4,
    releaseFrames: 12,
    speechMergeGapSeconds: 0.3,
  },

  // Light grade on the video layer only (overlays stay pure).
  colorGrade: "brightness(1.07) contrast(1.1) saturate(1.18)",

  progressBar: { position: "bottom" as "top" | "bottom", height: 12 },
};

export type StatSpec = {
  phrase: string;
  label: string;
} & ({ value: number; unit: string } | { text: string });

export type TransitionSpec = {
  atSourceTime: number;
  type: "whip" | "crossfade";
  durationInFrames: number;
};
