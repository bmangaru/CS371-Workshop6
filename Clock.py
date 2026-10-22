def clock(refs, nframes):
    frames = [None] * nframes
    ref_bit = [False] * nframes
    hand, faults = 0, 0
    for p in refs:
        if p in frames:
            ref_bit[frames.index(p)] = True   # hit: set bit, hand does NOT move
            continue
        faults += 1
        if None in frames:                    # empty slot available
            i = frames.index(None)
            frames[i], ref_bit[i] = p, True
            continue
        while True:                           # sweep for a victim
            if not ref_bit[hand]:
                frames[hand], ref_bit[hand] = p, True
                hand = (hand + 1) % nframes
                break
            ref_bit[hand] = False             # second chance
            hand = (hand + 1) % nframes
    return faults