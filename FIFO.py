def fifo(refs, nframes):
    queue, frames, faults = [], set(), 0
    for p in refs:
        if p in frames:
            continue                      # hit: FIFO does nothing
        faults += 1
        if len(frames) >= nframes:        # full -> evict oldest
            victim = queue.pop(0)
            frames.remove(victim)
        frames.add(p)
        queue.append(p)
    return faults