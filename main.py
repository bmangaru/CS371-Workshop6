"""
CS 371 - Workshop 6: runs every task using the three algorithm files.
Keep fifo.py, lru.py, clock.py and this file in the same folder.

Run with:  python3 main.py
"""

from fifo import fifo
from lru import lru
from clock import clock


def check(name, func, refs, nframes, expected):
    got = func(refs, nframes)
    status = "PASS" if got == expected else "FAIL"
    print(f"  {status}  {name:5} {nframes} frames: got {got:2}, expected {expected}")


LECTURE = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
SECOND  = [2, 3, 4, 2, 1, 5, 2, 1, 3]
GRADED  = [3, 1, 4, 1, 5, 2, 4, 1, 5, 3, 2, 4, 1, 5, 3]

# Belady's Anomaly string (Part B Task 3).
# Needs >= 4 distinct pages, >= 12 references, and must not be the lecture string.
# Replace with your own construction if you build a different one.
BELADY = [4, 1, 3, 2, 4, 1, 4, 2, 5, 4, 1, 3, 2, 5]
BELADY_K = 3


print("=== Part A Task 1: Validation (3 frames) ===")
check("FIFO", fifo, LECTURE, 3, 9)
check("LRU",  lru,  LECTURE, 3, 10)
check("FIFO", fifo, SECOND,  3, 7)
check("LRU",  lru,  SECOND,  3, 6)

print("\n=== Part A Task 2: Graded data, 4 frames ===")
print("  Reference string:", GRADED)
print("\n  FIFO trace (oldest -> newest):")
fifo(GRADED, 4, trace=True)
print("\n  LRU trace (least recent -> most recent):")
lru(GRADED, 4, trace=True)

print("\n=== Part B Task 1: CLOCK validation (lecture string) ===")
check("CLOCK", clock, LECTURE, 3, 9)
check("CLOCK", clock, LECTURE, 4, 10)

print("\n=== Part B Task 2: Graded data, 4 frames ===")
print("  CLOCK trace (* = ref bit set, > = hand):")
clock(GRADED, 4, trace=True)
print("\n  Algorithm | Faults")
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
