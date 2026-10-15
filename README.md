# Bug Band Practice Room 🎸

A tiny terminal idle game: recruit bug musicians, earn notes, hold concerts.

```
   🎸 chirp! boom-chick! glow-glow! 🎶
```

## Run

```bash
python3 band.py
```

Requires Python 3, no third-party dependencies.

## How to play

| Command | Action |
|---------|--------|
| `p` | Practice: the band plays together and earns notes |
| `r` | Recruit: spend notes to sign new bug musicians |
| `c` | Concert: needs 3+ members, earns cheering (even more notes) |
| `s` | Show band status |
| `q` | Save and quit (progress stored in `save.json`) |

Watch out for random **rain events** during practice: notes get halved, but the show goes on. 🌧

## Musicians

| Musician | Role | Signing fee (notes) | Output / round |
|----------|------|--------------------|----------------|
| Cicada | Guitarist | 0 (founding member) | 2 |
| Beetle | Drummer | 30 | 5 |
| Cricket | Vocalist | 80 | 12 |
| Firefly | Lighting | 150 | 25 |
| Ant | Bassist | 300 | 50 |

## Goal

Collect all 5 musicians, hold 10 concerts, become a legend among bug managers.
