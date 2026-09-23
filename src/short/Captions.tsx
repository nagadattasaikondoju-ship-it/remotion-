import { AbsoluteFill, interpolate, Sequence, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { config } from "./config";
import { FONT_FAMILY } from "./fonts";
import type { TimedWord } from "./timeline";

type Page = { words: TimedWord[]; startFrame: number; endFrame: number };

const endsSentence = (w: TimedWord) => /[.?!,]$/.test(w.text);

// Group words into 2-4 word lines, breaking on punctuation, pauses and length.
export const buildPages = (words: TimedWord[]): Page[] => {
  const { maxWords, minWords, maxChars } = config.captions;
  const pages: Page[] = [];
  let cur: TimedWord[] = [];
  const flush = () => {
    if (cur.length) pages.push({ words: cur, startFrame: cur[0].startFrame, endFrame: 0 });
    cur = [];
  };
  words.forEach((w, i) => {
    const prev = words[i - 1];
    const chars = cur.reduce((n, x) => n + x.text.length + 1, 0) + w.text.length;
    const pause = prev ? w.startFrame - prev.endFrame > config.fps * 0.35 : false;
    if (cur.length && (cur.length >= maxWords || chars > maxChars || pause)) flush();
    cur.push(w);
    if (endsSentence(w) && cur.length >= minWords) flush();
  });
  flush();
  // No orphans: fold a lone word into the previous line if they belong to the same sentence.
  for (let i = pages.length - 1; i > 0; i--) {
    const prev = pages[i - 1];
    if (pages[i].words.length === 1 && prev.words.length < maxWords + 1 && !endsSentence(prev.words[prev.words.length - 1])) {
      prev.words.push(...pages[i].words);
      pages.splice(i, 1);
    }
  }
  pages.forEach((p, i) => {
    const last = p.words[p.words.length - 1];
    const next = pages[i + 1];
    const linger = last.endFrame + Math.round(config.fps * 0.4);
    p.endFrame = next ? Math.min(next.startFrame, linger) : linger;
  });
  return pages;
};

const Word: React.FC<{ word: TimedWord }> = ({ word }) => {
  const frame = useCurrentFrame(); // relative to the word's own <Sequence>
  const { fps } = useVideoConfig();
  const isKeyword = config.captions.keywords.includes(word.key);
  const pop = spring({
    frame,
    fps,
    config: isKeyword ? { damping: 9, stiffness: 180, mass: 0.6 } : { damping: 16, stiffness: 220 },
  });
  const scale = interpolate(pop, [0, 1], [isKeyword ? 0.4 : 0.75, 1]);
  return (
    <span
      style={{
        position: "absolute",
        left: 0,
        top: 0,
        whiteSpace: "nowrap",
        display: "inline-block",
        transform: `scale(${scale})`,
        opacity: Math.min(1, pop * 2),
        color: isKeyword ? config.accent : "white",
      }}
    >
      {word.text}
    </span>
  );
};

const CaptionPage: React.FC<{ page: Page }> = ({ page }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const enter = spring({ frame, fps, config: { damping: 200 }, durationInFrames: 6 });
  return (
    <AbsoluteFill style={{ alignItems: "center" }}>
      <div
        style={{
          position: "absolute",
          top: 1230,
          width: 960,
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          columnGap: 26,
          rowGap: 6,
          fontFamily: FONT_FAMILY,
          fontWeight: 900,
          fontSize: 92,
          lineHeight: 1.12,
          textTransform: "uppercase",
          textAlign: "center",
          WebkitTextStroke: "16px black",
          paintOrder: "stroke fill",
          textShadow: "0 8px 0 rgba(0,0,0,0.45)",
          transform: `translateY(${(1 - enter) * 24}px)`,
        }}
      >
        {page.words.map((w) => (
          // Invisible copy reserves the word's final width so the line never reflows;
          // the visible copy mounts in its own <Sequence> at the moment it's spoken.
          <span key={w.startFrame} style={{ position: "relative", display: "inline-block" }}>
            <span style={{ visibility: "hidden" }}>{w.text}</span>
            <Sequence from={w.startFrame - page.startFrame} layout="none">
              <Word word={w} />
            </Sequence>
          </span>
        ))}
      </div>
    </AbsoluteFill>
  );
};

export const Captions: React.FC<{ words: TimedWord[] }> = ({ words }) => (
  <>
    {buildPages(words).map((p) => (
      <Sequence key={p.startFrame} from={p.startFrame} durationInFrames={p.endFrame - p.startFrame}>
        <CaptionPage page={p} />
      </Sequence>
    ))}
  </>
);
