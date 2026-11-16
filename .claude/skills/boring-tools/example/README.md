# Example data

These files preserve the real text contracts from one finished 60-second edit.

- `cuts-60.tsv` records the selected source ranges, framing labels and face identifiers.
- `timeline-60.tsv` records the generated output timeline.
- `broll-60.tsv` records the screen schedule.
- `subject-edge.tsv` records the measured subject edge.
- `rebuild.sh` shows the full dependency order for all six output formats.

This folder is a reference, not a runnable demo.

The exact missing inputs are:

- The original source recording and its cleaned local copy.
- `faces.tsv`, which holds the measured face position for each cut.
- `cuts-15.tsv` and `cuts-30.tsv`.
- `broll-15.tsv` and `broll-30.tsv`.
- `assets/screens/04-exercise.png`.
- `assets/screens/05-resultsheet.png`.
- `assets/screens/07-playbook.png`.
- `assets/screens/03-learn-path.png`.
- `assets/app-icon.png` and `assets/wordmark.png`.

The PNG files are private Jayla product images from the original ad shoot.

Use these files to understand the format. Use your own footage and assets for a build.

Run the repository tests for an independent synthetic verification:

```bash
python3 -m unittest discover -s tests -v
```
