"""
FIFO page replacement.
Evicts whichever page has been resident the longest (insertion order).

Run on its own:  python3 fifo.py
"""


def fifo(refs, nframes, trace=False):
    queue = []          # residency order, oldest first
    frames = set()      # which pages are resident (fast lookup only)
    faults = 0

    for p in refs:
        if p in frames:
            # hit: FIFO changes nothing
            if trace:
                print(f"  ref {p}:  HIT   {' '.join(map(str, queue))}")
            continue

        faults += 1
        if len(frames) >= nframes:      # frames full -> evict the oldest
            victim = queue.pop(0)
            frames.remove(victim)
        frames.add(p)
        queue.append(p)

        if trace:
            print(f"  ref {p}:  MISS  {' '.join(map(str, queue))}")

    if trace:
        print(f"  Total faults: {faults}")
    return faults


if __name__ == "__main__":
    lecture = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    second = [2, 3, 4, 2, 1, 5, 2, 1, 3]

    print("FIFO, lecture string, 3 frames (expected 9)")
    print("  list shown oldest -> newest")
    fifo(lecture, 3, trace=True)

    print("\nFIFO, lecture string, 4 frames (expected 10)")
    fifo(lecture, 4, trace=True)

    print("\nFIFO, second validation string, 3 frames (expected 7)")
    fifo(second, 3, trace=True)
