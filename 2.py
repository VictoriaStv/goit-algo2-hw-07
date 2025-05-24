import timeit
import matplotlib.pyplot as plt
from functools import lru_cache

import pandas as pd

class SplayNode:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.left = None
        self.right = None

class SplayTree:
    def __init__(self):
        self.root = None

    def _right_rotate(self, x):
        y = x.left
        x.left = y.right
        y.right = x
        return y

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def _splay(self, root, key):
        if not root or root.key == key:
            return root
        if key < root.key:
            if not root.left:
                return root
            if key < root.left.key:
                root.left.left = self._splay(root.left.left, key)
                root = self._right_rotate(root)
            elif key > root.left.key:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right:
                    root.left = self._left_rotate(root.left)
            return self._right_rotate(root) if root.left else root
        else:
            if not root.right:
                return root
            if key > root.right.key:
                root.right.right = self._splay(root.right.right, key)
                root = self._left_rotate(root)
            elif key < root.right.key:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left:
                    root.right = self._right_rotate(root.right)
            return self._left_rotate(root) if root.right else root

    def search(self, key):
        self.root = self._splay(self.root, key)
        return self.root.val if self.root and self.root.key == key else None

    def insert(self, key, val):
        if not self.root:
            self.root = SplayNode(key, val)
            return
        self.root = self._splay(self.root, key)
        if self.root.key == key:
            return
        new_node = SplayNode(key, val)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None
        self.root = new_node

# з кешем LRU
@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n <= 1:
        return n
    return fibonacci_lru(n-1) + fibonacci_lru(n-2)

# з Splay Tree
def fibonacci_splay(n, tree):
    cached = tree.search(n)
    if cached is not None:
        return cached
    if n <= 1:
        tree.insert(n, n)
        return n
    val = fibonacci_splay(n-1, tree) + fibonacci_splay(n-2, tree)
    tree.insert(n, val)
    return val





n_values = list(range(0, 1000, 50))
lru_times = []
splay_times = []

for n in n_values:
    lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=1)
    lru_times.append(lru_time)

    tree = SplayTree()
    splay_time = timeit.timeit(lambda: fibonacci_splay(n, tree), number=1)
    splay_times.append(splay_time)


df = pd.DataFrame({
    "n": n_values,
    "LRU Cache Time (s)": lru_times,
    "Splay Tree Time (s)": splay_times
})
print("\nРезультати порівняння:\n")
print(df.to_string(index=False))


plt.figure(figsize=(10, 6))
plt.plot(n_values, lru_times, marker='o', linestyle='-', label='LRU Cache')
plt.plot(n_values, splay_times, marker='x', linestyle='-', label='Splay Tree')
plt.title('Порівняння часу виконання для LRU Cache та Splay Tree')
plt.xlabel('Число Фібоначчі (n)')
plt.ylabel('Середній час виконання (секунди)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
