export type EdlSegment = {
  id: number;
  start: number;
  end: number;
  keep: boolean;
  reason: string;
  text: string;
};
export type Edl = { sourceDuration: number; segments: EdlSegment[] };

export type Word = { text: string; start: number; end: number };
export type Transcript = { duration: number; words: Word[] };

export type FaceFrame = { f: number; x: number; y: number; w: number; h: number };
export type Faces = { width: number; height: number; fps: number; frames: FaceFrame[] };

export type ShortData = { edl: Edl; transcript: Transcript; faces: Faces };
