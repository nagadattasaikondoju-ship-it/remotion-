import type { TransitionPresentation, TransitionPresentationComponentProps } from "@remotion/transitions";
import { AbsoluteFill } from "remotion";

type WhipProps = { blur: number };

// Whip-pan: both shots slide left fast with horizontal motion blur that peaks mid-move.
const Whip: React.FC<TransitionPresentationComponentProps<WhipProps>> = ({
  children,
  presentationDirection,
  presentationProgress: p,
  passedProps,
}) => {
  const entering = presentationDirection === "entering";
  const x = entering ? (1 - p) * 100 : -p * 100;
  const blur = Math.sin(p * Math.PI) * passedProps.blur;
  return (
    <AbsoluteFill style={{ transform: `translateX(${x}%)`, filter: `blur(${blur}px)` }}>
      {children}
    </AbsoluteFill>
  );
};

export const whip = (props: WhipProps = { blur: 28 }): TransitionPresentation<WhipProps> => ({
  component: Whip,
  props,
});
