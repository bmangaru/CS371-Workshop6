def lru(refs, nframes):
    order, frames, faults = [], set(), 0   # front = least recently used
    for p in refs:
        if p in frames:
            order.remove(p)
            order.append(p)               # <- the line people forget
            continue
        faults += 1
        if len(frames) >= nframes:
            victim = order.pop(0)
            frames.remove(victim)
        frames.add(p)
        order.append(p)
    return faults