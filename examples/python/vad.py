"""New energy gate, NOT Huwen or a speech classifier. Scores are mean amplitudes."""

class EnergyGate:
    def __init__(self, start=0.2, stop=0.1, hangover=3):
        if not (0 <= stop < start <= 1) or not isinstance(hangover, int) or hangover < 1:
            raise ValueError('require 0 <= stop < start <= 1, positive hangover')
        self.start, self.stop, self.hangover = start, stop, hangover
        self.active = False
        self.quiet = 0

    def feed(self, pcm):
        if not pcm or any(not isinstance(v, int) or not -32768 <= v <= 32767 for v in pcm):
            raise ValueError('expected nonempty signed 16-bit samples')
        score = sum(abs(v) for v in pcm) / (32768 * len(pcm))
        if not self.active:
            if score >= self.start:
                self.active = True
                return 'start'
            return 'silence'
        self.quiet = self.quiet + 1 if score < self.stop else 0
        if self.quiet >= self.hangover:
            self.active, self.quiet = False, 0
            return 'end'
        return 'active'

if __name__ == '__main__':
    gate = EnergyGate()
    events = [gate.feed(frame) for frame in [[0]*320, [12000]*320, [0]*320, [0]*320, [0]*320]]
    print(' '.join(events))
