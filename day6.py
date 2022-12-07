from collections import deque
import unittest

def nwise(iterator, n):
    deq = deque((),n)
    for x in iterator:
        deq.append(x)
        if len(deq)==n: yield deq

def start_marker(buffer, n):
    for idx, sequence in enumerate(nwise(buffer, n)):
        if len(set(sequence))==n:
            return idx+n

class TestStartMarker(unittest.TestCase):
    def test_start_marker(self):
        with open("test6.txt") as f:
            cases = [line.strip().split(", ") for line in f]
        for text, marker, seq_len in cases:
            self.assertEqual(start_marker(text, int(seq_len)), int(marker))

if __name__=="__main__":
    unittest.main(exit=False)
    with open("input6.txt") as f:
        text = f.readline().strip()
        print(start_marker(text, 4))
        print(start_marker(text, 14))