import { interpolate, OffthreadVideo, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { config } from "./config";
import type { Clip } from "./timeline";

type Props = {
  clip: Clip;
  faceTrack: { x: number; y: number }[];
};

// One kept segment of the source, framed so the (pre-smoothed) face stays on
// target, with a spring punch-in between alternating zoom levels at the cut.
export const FaceFramedClip: React.FC<Props> = ({ clip, faceTrack }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  const punch = spring({
    frame,
    fps,
    durationInFrames: config.punchIn.frames,
    config: { damping: 200 },
  });
  const zoom = config.face.baseZoom * interpolate(punch, [0, 1], [clip.prevZoom, clip.zoom]);

  const srcFrame = Math.min(faceTrack.length - 1, clip.srcFrom + frame);
  const face = faceTrack[Math.max(0, srcFrame)];

  // Visible window (in normalised source coords) that puts the face on target, clamped to the frame.
  const maxOffset = 1 - 1 / zoom;
  const left = Math.min(Math.max(face.x - config.face.targetX / zoom, 0), maxOffset);
  const top = Math.min(Math.max(face.y - config.face.targetY / zoom, 0), maxOffset);

  return (
    <div style={{ position: "absolute", inset: 0, overflow: "hidden", backgroundColor: "black" }}>
      <div
        style={{
          width,
          height,
          transformOrigin: "0 0",
          transform: `translate(${-left * width * zoom}px, ${-top * height * zoom}px) scale(${zoom})`,
        }}
      >
        <OffthreadVideo
          src={staticFile(config.media.video)}
          trimBefore={clip.srcFrom}
          style={{ width, height, objectFit: "cover", filter: config.colorGrade }}
        />
      </div>
    </div>
  );
};
