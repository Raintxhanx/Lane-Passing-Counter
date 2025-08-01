class Counter:
    def __init__(self):
        self.count = 0
        self.is_counting = False

    def start_counting(self):
        self.is_counting = True

    def stop_counting(self):
        self.is_counting = False

    def get_count(self):
        return self.count

    def increment_count(self):
        if self.is_counting:
            self.count += 1

    def reset_count(self):
        self.count = 0