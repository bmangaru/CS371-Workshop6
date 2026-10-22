"""
CLOCK page replacement.
Frames form a circle; each has a referenced bit. On a fault the hand
sweeps: bit set -> clear it and move on (second chance);
bit clear -> evict that page.

Run on its own:  python3 clock.py
"""


def show(frames, ref_bit, hand):
    # e.g.  [1* 2  >3*]   * = referenced bit set, > = where the hand points
    parts = []
    for i, page in enumerate(frames):
        text = "-" if page is None else str(page)
        text += "*" if ref_bit[i] else " "
        if i == hand:
            text = ">" + text
        parts.append(text)
    return "[" + " ".join(parts) + "]"


def clock(refs, nframes, trace=False):
    frames = [None] * nframes           # circular array of pages
    ref_bit = [False] * nframes         # one referenced bit per frame
    hand = 0
    faults = 0

    for p in refs:
        if p in frames:
            ref_bit[frames.index(p)] = True   # hit: set bit, hand does NOT move
            if trace:
                print(f"  ref {p}:  HIT   {show(frames, ref_bit, hand)}")
            continue

        faults += 1
        if None in frames:                    # an empty slot is still available
            i = frames.index(None)
            frames[i] = p
            ref_bit[i] = True
        else:
            while True:                       # sweep for a victim
                if not ref_bit[hand]:
                    frames[hand] = p          # evict and replace
                    ref_bit[hand] = True
                    hand = (hand + 1) % nframes
                    break
                ref_bit[hand] = False         # second chance
                hand = (hand + 1) % nframes

        if trace:
            print(f"  ref {p}:  MISS  {show(frames, ref_bit, hand)}")

    if trace:
        print(f"  Total faults: {faults}")
    return faults


if __name__ == "__main__":
    lecture = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]

    print("CLOCK, lecture string, 3 frames (expected 9)")
    print("  frames in slot order;  * = referenced bit set,  > = hand position")
    clock(lecture, 3, trace=True)

    print("\nCLOCK, lecture string, 4 frames (expected 10)")
    clock(lecture, 4, trace=True)
