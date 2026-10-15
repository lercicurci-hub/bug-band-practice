#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""虫鸣乐队练习室：终端放置小游戏。招募昆虫乐手，攒音符，开演唱会。"""

import json
import os

SAVE = "save.json"
CONCERT_FEE = 200  # 开演唱会的宣传费（音符）

BUGS = {
    "蝉":   {"role": "吉他手", "cost": 0,   "rate": 2,  "line": "吱——吱吱！"},
    "甲虫": {"role": "鼓手",   "cost": 30,  "rate": 5,  "line": "咚咚锵！"},
    "蟋蟀": {"role": "主唱",   "cost": 80,  "rate": 12, "line": "瞿瞿瞿～"},
    "萤火虫": {"role": "灯光师", "cost": 150, "rate": 25, "line": "biubiu✨"},
    "蚂蚁": {"role": "贝斯手", "cost": 300, "rate": 50, "line": "嗡嗡嗡……"},
}


def load():
    if os.path.exists(SAVE):
        with open(SAVE, encoding="utf-8") as f:
            return json.load(f)
    return {"notes": 0, "band": ["蝉"], "concerts": 0}


def save(state):
    with open(SAVE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def practice(state):
    gain = sum(BUGS[b]["rate"] for b in state["band"])
    state["notes"] += gain
    print(f"练习结束！乐队合奏 +{gain} 音符（共 {state['notes']}）")
    for b in state["band"]:
        print(f"  {b}（{BUGS[b]['role']}）：{BUGS[b]['line']}")


def recruit(state):
    print("可招募：")
    for name, info in BUGS.items():
        owned = "（已在队）" if name in state["band"] else f"（{info['cost']} 音符）"
        print(f"  {name}·{info['role']} {owned}")
    name = input("招募谁？（输入名字，回车跳过）> ").strip()
    if not name:
        return
    if name not in BUGS:
        print("没有这位乐手。")
        return
    if name in state["band"]:
        print("他已经在乐队了！")
        return
    cost = BUGS[name]["cost"]
    if state["notes"] < cost:
        print(f"音符不够（需要 {cost}，现有 {state['notes']}）。")
        return
    state["notes"] -= cost
    state["band"].append(name)
    print(f"{name} 加入了乐队！{BUGS[name]['line']}")


def concert(state):
    if len(state["band"]) < 3:
        print("乐队至少要 3 位乐手才能开演唱会，先去招募吧。")
        return
    if state["notes"] < CONCERT_FEE:
        print(f"宣传费不够（需要 {CONCERT_FEE} 音符）。")
        return
    state["notes"] -= CONCERT_FEE
    state["concerts"] += 1
    cheer = 150 + 50 * state["concerts"]
    state["notes"] += cheer
    print("🎸 演唱会开演！")
    print("  " + " ".join(f"{b}{BUGS[b]['line']}" for b in state["band"]))
    print(f"观众欢呼！收获 {cheer} 音符（累计开演 {state['concerts']} 场）")


def status(state):
    print(f"音符：{state['notes']}｜乐队：{len(state['band'])}/{len(BUGS)} 人｜"
          f"演唱会：{state['concerts']} 场")
    for b in state["band"]:
        print(f"  - {b}（{BUGS[b]['role']}，每轮 +{BUGS[b]['rate']}）")


def main():
    state = load()
    print("=== 虫鸣乐队练习室 ===")
    print("指令：p 练习 / r 招募 / c 演唱会 / s 查看 / q 存档退出")
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
            print("已存档，下次继续排练！")
            break
        else:
            print("指令：p 练习 / r 招募 / c 演唱会 / s 查看 / q 存档退出")


if __name__ == "__main__":
    main()
