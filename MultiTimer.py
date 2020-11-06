from time import perf_counter


class MultiTimer:
    def __init__(self):
        self.labels = []
        self.times = []
        self.flags = []
        self.record('[START]')

    def record(self, label, flags=0):
        now = perf_counter()
        self.labels.append(label)
        self.times.append(now)
        self.flags.append(flags)

    def report(self, prefix=""):
        self.record("[STOP]")
        max_label_width = max([len(label) for label in self.labels])
        record_count = len(self.labels)
        total_time = self.times[-1] - self.times[0];

        lines = ["---"]
        for i in range(record_count):
            line = prefix
            line += f"{self.labels[i]:{max_label_width}} {self.times[i]:13.9f}"
            if i < record_count - 1:
                local_time = self.times[i + 1] - self.times[i]
                percentage = local_time / total_time * 100.0
                line += f"  {local_time:13.9f} {percentage:9.2f}"
            else:
                line += f" [{total_time:13.9f}]"
            if self.flags[i] > 0:
                line += " " + "*" * self.flags[i]
            lines.append(line)
        print("\n".join(lines), flush=True)
