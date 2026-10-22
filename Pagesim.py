"""
CS 371 - Workshop 6: Page-Replacement Simulator
FIFO, LRU, and CLOCK page replacement, with validation runs,
graded runs, and a Belady's Anomaly check.

Run with:  python3 pagesim.py
"""


# ======================================================================
# Algorithms - each takes (reference string, number of frames)
# and returns the total number of page faults.
# Every call starts with fresh, empty state.
# ======================================================================

def fifo(refs, nframes):
    queue = []          # residency order, oldest first
    frames = set()      # which pages are resident (fast lookup only)
    faults = 0
    for p in refs:
        if p in frames:
            continue                    # hit: FIFO changes nothing
        faults += 1
        if len(frames) >= nframes:      # frames full -> evict the oldest
            victim = queue.pop(0)
            frames.remove(victim)
        frames.add(p)
        queue.append(p)
    return faults


def lru(refs, nframes):
    order = []          # least recently used first, most recent last
    frames = set()
    faults = 0
    for p in refs:
        if p in frames:
            order.remove(p)
            order.append(p)             # a HIT also updates recency
            continue
        faults += 1
        if len(frames) >= nframes:      # frames full -> evict least recently used
            victim = order.pop(0)
            frames.remove(victim)
        frames.add(p)
        order.append(p)
    return faults


def clock(refs, nframes):
    frames = [None] * nframes           # circular array of pages
    ref_bit = [False] * nframes         # one referenced bit per frame
    hand = 0
    faults = 0
    for p in refs:
        if p in frames:
            ref_bit[frames.index(p)] = True   # hit: set bit, hand does NOT move
            continue
        faults += 1
        if None in frames:                    # an empty slot is still available
            i = frames.index(None)
            frames[i] = p
            ref_bit[i] = True
            continue
        while True:                           # sweep for a victim
            if not ref_bit[hand]:
                frames[hand] = p              # evict and replace
                ref_bit[hand] = True
                hand = (hand + 1) % nframes
                break
            ref_bit[hand] = False             # second chance
            hand = (hand + 1) % nframes
    return faults


# ======================================================================
# Helper for validation
# ======================================================================

def check(name, func, refs, nframes, expected):
    got = func(refs, nframes)
    status = "PASS" if got == expected else "FAIL"
    print(f"  {status}  {name:5} {nframes} frames: got {got:2}, expected {expected}")


# ======================================================================
# Reference strings
# ======================================================================

LECTURE = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
SECOND  = [2, 3, 4, 2, 1, 5, 2, 1, 3]
GRADED  = [3, 1, 4, 1, 5, 2, 4, 1, 5, 3, 2, 4, 1, 5, 3]

# Belady's Anomaly string (Part B Task 3).
# Must have >= 4 distinct pages, >= 12 references, and not be the lecture string.
# Replace this with your own construction if you build a different one.
BELADY = [4, 1, 3, 2, 4, 1, 4, 2, 5, 4, 1, 3, 2, 5]
BELADY_K = 3


if __name__ == "__main__":

    print("=== Part A Task 1: Validation (3 frames) ===")
    check("FIFO", fifo, LECTURE, 3, 9)
    check("LRU",  lru,  LECTURE, 3, 10)
    check("FIFO", fifo, SECOND,  3, 7)
    check("LRU",  lru,  SECOND,  3, 6)

    print("\n=== Part A Task 2: Graded data, 4 frames ===")
    print("  Reference string:", GRADED)
    print(f"  FIFO faults: {fifo(GRADED, 4)}")
    print(f"  LRU  faults: {lru(GRADED, 4)}")

    print("\n=== Part B Task 1: CLOCK validation (lecture string) ===")
    check("CLOCK", clock, LECTURE, 3, 9)
    check("CLOCK", clock, LECTURE, 4, 10)

    print("\n=== Part B Task 2: Comparison table (graded data, 4 frames) ===")
    print("  Algorithm | Faults")
    print("  ----------+-------")
    for name, func in [("FIFO", fifo), ("LRU", lru), ("CLOCK", clock)]:
        print(f"  {name:9} | {func(GRADED, 4)}")

    print("\n=== Part B Task 3: Belady's Anomaly ===")
    k = BELADY_K
    print("  Reference string:", BELADY)
    print(f"  Length {len(BELADY)}, distinct pages {len(set(BELADY))}")
    f_k, f_k1 = fifo(BELADY, k), fifo(BELADY, k + 1)
    c_k, c_k1 = clock(BELADY, k), clock(BELADY, k + 1)
    print(f"  FIFO : {k} frames -> {f_k} faults, {k+1} frames -> {f_k1} faults"
          f"   anomaly: {'YES' if f_k1 > f_k else 'no'}")
    print(f"  CLOCK: {k} frames -> {c_k} faults, {k+1} frames -> {c_k1} faults"
          f"   anomaly: {'YES' if c_k1 > c_k else 'no'}")

    print("\n=== Part B Task 4: Graded data at other frame counts (for the report) ===")
    print("  Frames | FIFO | LRU | CLOCK")
    for n in [3, 4, 5]:
        print(f"  {n:6} | {fifo(GRADED, n):4} | {lru(GRADED, n):3} | {clock(GRADED, n):5}")