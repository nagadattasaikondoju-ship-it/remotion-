import { linearTiming, TransitionPresentation, TransitionSeries } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { useMemo } from "react";
import { AbsoluteFill, Audio, Easing, Sequence, staticFile } from "remotion";
import { Captions } from "./short/Captions";
import { config } from "./short/config";
import { FaceFramedClip } from "./short/FaceFramedClip";
import "./short/fonts";
import { HookTitle, LowerThird, ProgressBar, StatPops } from "./short/Graphics";
import { buildTimeline, musicVolumes, smoothFaces } from "./short/timeline";
import type { ShortData } from "./short/types";
import { whip } from "./short/whip";

export type MyVideoProps = { data: ShortData | null };

export const MyVideo: React.FC<MyVideoProps> = ({ data }) => {
  const timeline = useMemo(() => data && buildTimeline(data.edl, data.transcript), [data]);
  const faceTrack = useMemo(
    () => data && smoothFaces(data.faces.frames, config.face.smoothingWindow),
    [data],
  );
  const volumes = useMemo(
    () => timeline && musicVolumes(timeline.words, timeline.durationInFrames),
    [timeline],
  );
  if (!data || !timeline || !faceTrack || !volumes) {
    return <AbsoluteFill style={{ backgroundColor: "black" }} />;
  }
  const fps = config.fps;

  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      {/* Cut list: only keep:true segments, with explicit transitions on chosen cuts. */}
      <TransitionSeries>
        {timeline.clips.flatMap((clip) => {
          const t = clip.transitionIn;
          const items = [];
          if (t) {
            items.push(
              <TransitionSeries.Transition
                key={`t${clip.index}`}
                timing={linearTiming({ durationInFrames: t.durationInFrames, easing: Easing.inOut(Easing.cubic) })}
                presentation={
                  (t.type === "whip" ? whip() : fade()) as TransitionPresentation<Record<string, unknown>>
                }
              />,
            );
          }
          items.push(
            <TransitionSeries.Sequence key={`c${clip.index}`} durationInFrames={clip.durationInFrames}>
              <FaceFramedClip clip={clip} faceTrack={faceTrack} />
            </TransitionSeries.Sequence>,
          );
          return items;
        })}
      </TransitionSeries>

      {/* Light vignette to focus the eye and seat the captions. */}
      <AbsoluteFill
        style={{
          background:
            "radial-gradient(ellipse at 50% 40%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.45) 100%), linear-gradient(to bottom, rgba(0,0,0,0) 60%, rgba(0,0,0,0.35) 100%)",
        }}
      />

      <Captions words={timeline.words} />
      <StatPops words={timeline.words} />

      <Sequence durationInFrames={config.hook.durationInFrames}>
        <HookTitle />
      </Sequence>

      <Sequence
        from={Math.round(config.lowerThird.fromSeconds * fps)}
        durationInFrames={Math.round(config.lowerThird.durationInSeconds * fps)}
      >
        <LowerThird />
      </Sequence>

      <ProgressBar />

      <Audio src={staticFile(config.music.src)} loop volume={(f) => volumes[Math.min(f, volumes.length - 1)]} />
    </AbsoluteFill>
  );
};
