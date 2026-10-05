import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

// Self-hosted (Google Fonts may be unreachable at render time). SIL OFL.
export const FONT_FAMILY = "Montserrat";

for (const weight of ["800", "900"]) {
  loadFont({
    family: FONT_FAMILY,
    url: staticFile(`fonts/montserrat-latin-${weight}-normal.woff2`),
    weight,
  });
}
