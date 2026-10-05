import "./index.css";
import { CalculateMetadataFunction, Composition, staticFile } from "remotion";
import { MyVideo, MyVideoProps } from "./MyVideo";
import { config } from "./short/config";
import { buildTimeline } from "./short/timeline";
import type { Edl, Faces, ShortData, Transcript } from "./short/types";

const load = async <T,>(path: string): Promise<T> => {
  const res = await fetch(staticFile(path));
  if (!res.ok) throw new Error(`Missing ${path} - run \`npm run prep -- <video>\` first`);
  return res.json();
};

// Pipeline JSON is loaded once here; the duration comes from the cut list.
const calculateMetadata: CalculateMetadataFunction<MyVideoProps> = async () => {
  const [edl, transcript, faces] = await Promise.all([
    load<Edl>(config.media.edl),
    load<Transcript>(config.media.words),
    load<Faces>(config.media.faces),
  ]);
  const data: ShortData = { edl, transcript, faces };
  return {
    durationInFrames: buildTimeline(edl, transcript).durationInFrames,
    props: { data },
  };
};

export const RemotionRoot: React.FC = () => (
  <Composition
    id="Short"
    component={MyVideo}
    width={config.width}
    height={config.height}
    fps={config.fps}
    durationInFrames={config.fps}
    defaultProps={{ data: null }}
    calculateMetadata={calculateMetadata}
  />
);
