import {
  AbsoluteFill,
  Easing,
  interpolate,
  Sequence,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { config, StatSpec } from "./config";
import { FONT_FAMILY } from "./fonts";
import { normalise, TimedWord } from "./timeline";

const stroke = {
  WebkitTextStroke: "14px black",
  paintOrder: "stroke fill",
  textShadow: "0 8px 0 rgba(0,0,0,0.45)",
} as const;

// ---------------------------------------------------------------- hook title
export const HookTitle: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { headline, tagline, durationInFrames } = config.hook;
  const out = interpolate(frame, [durationInFrames - 10, durationInFrames], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.in(Easing.cubic),
  });
  const words = headline.join(" \n").split(" ");
  const tagIn = spring({ frame: frame - 24, fps, config: { damping: 12, stiffness: 160 } });

  return (
    <AbsoluteFill
      style={{
        alignItems: "center",
        paddingTop: 170,
        fontFamily: FONT_FAMILY,
        fontWeight: 900,
        textTransform: "uppercase",
        opacity: out,
        transform: `scale(${interpolate(out, [0, 1], [1.08, 1])})`,
      }}
    >
      <div style={{ textAlign: "center", fontSize: 104, lineHeight: 1.02, color: "white", ...stroke }}>
        {words.map((w, i) => {
          const s = spring({ frame: frame - i * 3, fps, config: { damping: 10, stiffness: 200, mass: 0.5 } });
          const isLast = i >= words.length - 2; // "erases brands" in accent
          return (
            <span key={i}>
              {w.startsWith("\n") && <br />}
              <span
                style={{
                  display: "inline-block",
                  margin: "0 14px",
                  color: isLast ? config.accent : "white",
                  transform: `translateY(${(1 - s) * 60}px) scale(${interpolate(s, [0, 1], [0.6, 1])})`,
                  opacity: Math.min(1, s * 1.5),
                }}
              >
                {w.trim()}
              </span>
            </span>
          );
        })}
      </div>
      <div
        style={{
          marginTop: 34,
          padding: "14px 34px 16px",
          background: config.accent,
          color: "white",
          fontSize: 52,
          borderRadius: 14,
          letterSpacing: 1,
          transform: `scale(${tagIn}) rotate(${interpolate(tagIn, [0, 1], [-6, -2])}deg)`,
          boxShadow: "0 10px 0 rgba(0,0,0,0.35)",
        }}
      >
        {tagline}
      </div>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- lower third
export const LowerThird: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const inP = spring({ frame, fps, config: { damping: 200 }, durationInFrames: 14 });
  const outP = spring({ frame: frame - (durationInFrames - 12), fps, config: { damping: 200 }, durationInFrames: 12 });
  const p = inP - outP;
  const textIn = spring({ frame: frame - 6, fps, config: { damping: 200 }, durationInFrames: 12 }) - outP;

  return (
    <AbsoluteFill style={{ fontFamily: FONT_FAMILY }}>
      <div style={{ position: "absolute", left: 60, top: 1560, display: "flex", alignItems: "stretch" }}>
        <div style={{ width: 14, background: config.accent, transform: `scaleY(${p})`, transformOrigin: "bottom" }} />
        <div
          style={{
            overflow: "hidden",
            background: "rgba(255,255,255,0.96)",
            clipPath: `inset(0 ${(1 - p) * 100}% 0 0)`,
            padding: "18px 34px 20px 26px",
            boxShadow: "0 12px 30px rgba(0,0,0,0.35)",
          }}
        >
          <div style={{ fontWeight: 900, fontSize: 54, color: "#111", transform: `translateY(${(1 - textIn) * 30}px)`, opacity: textIn }}>
            {config.lowerThird.name}
          </div>
          <div
            style={{
              fontWeight: 800,
              fontSize: 30,
              color: config.accent,
              textTransform: "uppercase",
              letterSpacing: 2,
              marginTop: 4,
              transform: `translateY(${(1 - textIn) * 30}px)`,
              opacity: textIn,
            }}
          >
            {config.lowerThird.title}
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- stat pop-ins
const StatCard: React.FC<{ stat: StatSpec }> = ({ stat }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const pop = spring({ frame, fps, config: { damping: 8, stiffness: 170, mass: 0.6 } });
  const out = interpolate(frame, [durationInFrames - 6, durationInFrames], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const big =
    "value" in stat
      ? Math.round(interpolate(frame, [0, 12], [0, stat.value], { extrapolateRight: "clamp" })).toString()
      : stat.text;
  return (
    <AbsoluteFill style={{ alignItems: "center", paddingTop: 110, fontFamily: FONT_FAMILY, fontWeight: 900 }}>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          transform: `scale(${pop * out}) rotate(${interpolate(pop, [0, 1], [8, -3])}deg)`,
          opacity: out,
        }}
      >
        <div style={{ display: "flex", alignItems: "baseline", gap: 20, color: "white", ...stroke }}>
          <span style={{ fontSize: "value" in stat ? 180 : 116, lineHeight: 1 }}>{big}</span>
          {"value" in stat && <span style={{ fontSize: 84, color: config.accent }}>{stat.unit}</span>}
        </div>
        <div
          style={{
            marginTop: 10,
            background: "black",
            color: "white",
            fontSize: 40,
            fontWeight: 800,
            padding: "8px 22px",
            textTransform: "uppercase",
            letterSpacing: 2,
          }}
        >
          {stat.label}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// Place each stat at the output frame where its phrase is first spoken.
export const StatPops: React.FC<{ words: TimedWord[] }> = ({ words }) => {
  const hits = config.stats
    .map((stat) => {
      const phrase = stat.phrase.split(" ").map(normalise);
      const i = words.findIndex((_, k) => phrase.every((p, j) => words[k + j]?.key === p));
      return i === -1 ? null : { stat, from: words[i].startFrame };
    })
    .filter((x): x is { stat: StatSpec; from: number } => x !== null)
    .sort((a, b) => a.from - b.from);
  return (
    <>
      {hits.map((h, i) => {
        const next = hits[i + 1]?.from ?? Infinity;
        const from = Math.max(h.from, config.hook.durationInFrames);
        const duration = Math.min(next - from, 54);
        return duration > 8 ? (
          <Sequence key={h.stat.phrase} from={from} durationInFrames={duration}>
            <StatCard stat={h.stat} />
          </Sequence>
        ) : null;
      })}
    </>
  );
};

// ---------------------------------------------------------------- progress bar
export const ProgressBar: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const { position, height } = config.progressBar;
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 0, right: 0, [position]: 0, height, background: "rgba(255,255,255,0.25)" }}>
        <div
          style={{
            width: `${(frame / (durationInFrames - 1)) * 100}%`,
            height: "100%",
            background: config.accent,
            boxShadow: `0 0 18px ${config.accent}`,
          }}
        />
      </div>
    </AbsoluteFill>
  );
};
