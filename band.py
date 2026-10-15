#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bug Band Practice Room: a tiny terminal idle game.
Recruit bug musicians, earn notes, hold concerts."""

import json
import os
import random

SAVE = "save.json"
CONCERT_FEE = 200  # publicity cost (notes) to hold a concert
RAIN_CHANCE = 0.2  # chance of a rain event during practice

BUGS = {
    "Cicada":  {"role": "Guitarist", "cost": 0,   "rate": 2,  "line": "Chirp—chirp!"},
    "Beetle":  {"role": "Drummer",   "cost": 30,  "rate": 5,  "line": "Boom-chick!"},
    "Cricket": {"role": "Vocalist",  "cost": 80,  "rate": 12, "line": "Chirpy-chirp~"},
    "Firefly": {"role": "Lighting",  "cost": 150, "rate": 25, "line": "Glow-glow ✨"},
    "Ant":     {"role": "Bassist",   "cost": 300, "rate": 50, "line": "Hum-hum-hum..."},
}


def load():
    if os.path.exists(SAVE):
        with open(SAVE, encoding="utf-8") as f:
            state = json.load(f)
        # drop band members saved by older non-English versions
        state["band"] = [b for b in state.get("band", []) if b in BUGS]
        if not state["band"]:
            state["band"] = ["Cicada"]
        return state
    return {"notes": 0, "band": ["Cicada"], "concerts": 0}


def save(state):
    with open(SAVE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def practice(state):
    gain = sum(BUGS[b]["rate"] for b in state["band"])
    if random.random() < RAIN_CHANCE:
        gain //= 2
        print("🌧 It's raining! The bugs play on as the audience opens "
              "umbrellas — notes halved this round")
    state["notes"] += gain
    print(f"Practice done! The band played together +{gain} notes "
          f"({state['notes']} total)")
    for b in state["band"]:
        print(f"  {b} ({BUGS[b]['role']}): {BUGS[b]['line']}")


def recruit(state):
    print("Available musicians:")
    for name, info in BUGS.items():
        owned = "(in band)" if name in state["band"] else f"({info['cost']} notes)"
        print(f"  {name} · {info['role']} {owned}")
    name = input("Recruit whom? (name, Enter to skip) > ").strip()
    if not name:
        return
    # be forgiving about case
    match = next((n for n in BUGS if n.lower() == name.lower()), None)
    if not match:
        print("No such musician.")
        return
    name = match
    if name in state["band"]:
        print("Already in the band!")
        return
    cost = BUGS[name]["cost"]
    if state["notes"] < cost:
        print(f"Not enough notes (need {cost}, have {state['notes']}).")
        return
    state["notes"] -= cost
    state["band"].append(name)
    print(f"{name} joined the band! {BUGS[name]['line']}")


def concert(state):
    if len(state["band"]) < 3:
        print("Need at least 3 musicians for a concert. Go recruit first.")
        return
    if state["notes"] < CONCERT_FEE:
        print(f"Not enough publicity budget (need {CONCERT_FEE} notes).")
        return
    state["notes"] -= CONCERT_FEE
    state["concerts"] += 1
    cheer = 150 + 50 * state["concerts"]
    state["notes"] += cheer
    print("🎸 Concert time!")
    print("  " + " ".join(f"{b}: {BUGS[b]['line']}" for b in state["band"]))
    print(f"The crowd goes wild! +{cheer} notes "
          f"({state['concerts']} concerts so far)")


def status(state):
    print(f"Notes: {state['notes']} | Band: {len(state['band'])}/{len(BUGS)} | "
          f"Concerts: {state['concerts']}")
    for b in state["band"]:
        print(f"  - {b} ({BUGS[b]['role']}, +{BUGS[b]['rate']}/round)")


def main():
    state = load()
    print("=== Bug Band Practice Room ===")
    print("Commands: p practice / r recruit / c concert / s status / q save & quit")
    while True:
        cmd = input("> ").strip().lower()
        if cmd == "p":
            practice(state)
        elif cmd == "r":
            recruit(state)
        elif cmd == "c":
            concert(state)
        elif cmd == "s":
            status(state)
        elif cmd == "q":
            save(state)
            print("Progress saved. See you at the next rehearsal!")
            break
        else:
            print("Commands: p practice / r recruit / c concert / "
                  "s status / q save & quit")


if __name__ == "__main__":
    main()
