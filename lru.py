"""
LRU page replacement.
Evicts whichever resident page was referenced longest ago.
A HIT also updates recency (moves the page to the most-recent end).

Run on its own:  python3 lru.py
"""


def lru(refs, nframes, trace=False):
    order = []          # least recently used first, most recent last
    frames = set()
    faults = 0

    for p in refs:
        if p in frames:
            order.remove(p)
            order.append(p)             # a HIT also updates recency
            if trace:
                print(f"  ref {p}:  HIT   {' '.join(map(str, order))}")
            continue

        faults += 1
        if len(frames) >= nframes:      # frames full -> evict least recently used
            victim = order.pop(0)
            frames.remove(victim)
        frames.add(p)
        order.append(p)

        if trace:
            print(f"  ref {p}:  MISS  {' '.join(map(str, order))}")

    if trace:
        print(f"  Total faults: {faults}")
    return faults


if __name__ == "__main__":
    lecture = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    second = [2, 3, 4, 2, 1, 5, 2, 1, 3]

    print("LRU, lecture string, 3 frames (expected 10)")
    print("  list shown least recent -> most recent")
    lru(lecture, 3, trace=True)

    print("\nLRU, lecture string, 4 frames")
    lru(lecture, 4, trace=True)

    print("\nLRU, second validation string, 3 frames (expected 6)")
    lru(second, 3, trace=True)
