import tkinter as tk
from tkinter import ttk, messagebox
import random
import time

def merge_sort_with_animations(arr):
    animations = []
    def merge_sort(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = merge_sort(arr[:mid])
        right = merge_sort(arr[mid:])
        return merge(left, right)

    def merge(left, right):
        i = j = 0
        merged = []
        while i < len(left) and j < len(right):
            animations.append(('compare', i, j))
            if left[i] <= right[j]:
                merged.append(left[i])
                animations.append(('overwrite', len(merged)-1, left[i]))
                i += 1
            else:
                merged.append(right[j])
                animations.append(('overwrite', len(merged)-1, right[j]))
                j += 1
        while i < len(left):
            merged.append(left[i])
            animations.append(('overwrite', len(merged)-1, left[i]))
            i += 1
        while j < len(right):
            merged.append(right[j])
            animations.append(('overwrite', len(merged)-1, right[j]))
            j += 1
        return merged

    sorted_arr = merge_sort(arr)
    return animations, sorted_arr

def insertion_sort_with_animations(arr):
    animations = []
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            animations.append(('compare', j, j+1))
            arr[j+1] = arr[j]
            animations.append(('overwrite', j+1, arr[j+1]))
            j -= 1
        arr[j+1] = key
        animations.append(('overwrite', j+1, key))
    return animations, arr

def counting_sort_with_animations(arr):
    animations = []
    if not arr:
        return animations, arr
    max_val = max(arr)
    count = [0] * (max_val + 1)
    output = [0] * len(arr)
    for num in arr:
        count[num] += 1
    for i in range(1, len(count)):
        count[i] += count[i-1]
    for i in range(len(arr) -1, -1, -1):
        val = arr[i]
        count[val] -= 1
        output[count[val]] = val
        animations.append(('overwrite', count[val], val))
    return animations, output

def selection_sort_with_animations(arr):
    animations = []
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            animations.append(('compare', j, min_idx))
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            animations.append(('swap', i, min_idx))
    return animations, arr.copy()


class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Visualizer")
        self.root.geometry("800x500")
        self.root.config(bg="#2c3e50")

        self.array = [] 
        self.speed = 150  

        control_frame = tk.Frame(self.root, bg="#34495e", pady=10)
        control_frame.pack(fill=tk.X)

        tk.Label(control_frame, text="Enter numbers (comma separated):", fg="white", bg="#34495e").pack(side=tk.LEFT, padx=5)
        self.entry = tk.Entry(control_frame, width=40)
        self.entry.pack(side=tk.LEFT, padx=5)

        self.generate_btn = tk.Button(control_frame, text="Generate Random", command=self.generate_random_array, bg="#2980b9", fg="white")
        self.generate_btn.pack(side=tk.LEFT, padx=5)

        self.sort_btn = tk.Button(control_frame, text="Sort", command=self.start_sorting, bg="#27ae60", fg="white")
        self.sort_btn.pack(side=tk.LEFT, padx=5)

        tk.Label(control_frame, text="Algorithm:", fg="white", bg="#34495e").pack(side=tk.LEFT, padx=5)
        self.algorithms = ["Merge Sort", "Insertion Sort", "Counting Sort", "Selection Sort"]
        self.alg_menu = ttk.Combobox(control_frame, values=self.algorithms, state="readonly")
        self.alg_menu.current(0)
        self.alg_menu.pack(side=tk.LEFT, padx=5)

        self.canvas = tk.Canvas(self.root, width=780, height=350, bg="#2d7688")
        self.canvas.pack(pady=10)

        self.time_label = tk.Label(self.root, text="", fg="white", bg="#2c3e50", font=("Arial", 14))
        self.time_label.pack()

        self.current_step = 0
        self.animations = []

        self.draw_array()

    def generate_random_array(self):
        size = random.randint(10, 20)
        self.array = [random.randint(1, 100) for _ in range(size)]
        self.entry.delete(0, tk.END)
        self.entry.insert(0, ", ".join(map(str, self.array)))
        self.draw_array()
        self.time_label.config(text="")
        self.current_step = 0
        self.animations = []

    def animate(self):
        if self.current_step >= len(self.animations):
            elapsed = time.perf_counter() - self.start_time
            self.time_label.config(text=f"Sorted in {elapsed:.4f} seconds")
            self.draw_array()  
            return

        action = self.animations[self.current_step]
        color_positions = {}

        if action[0] == 'compare':
            idx1, idx2 = action[1], action[2]
            if isinstance(idx1, int) and 0 <= idx1 < len(self.array):
                color_positions[idx1] = "#e74c3c"
            if isinstance(idx2, int) and 0 <= idx2 < len(self.array):
                color_positions[idx2] = "#e74c3c"

        elif action[0] == 'swap':
            idx1, idx2 = action[1], action[2]
            self.array[idx1], self.array[idx2] = self.array[idx2], self.array[idx1]
            color_positions[idx1] = "#27ae60"
            color_positions[idx2] = "#27ae60"

        elif action[0] == 'overwrite':
            idx, val = action[1], action[2]
            if 0 <= idx < len(self.array):
                self.array[idx] = val
                color_positions[idx] = "#27ae60"

        self.draw_array(color_positions)
        self.current_step += 1
        self.root.after(self.speed, self.animate)

    def start_sorting(self):
        input_str = self.entry.get().strip()
        if not input_str:
            messagebox.showerror("Error", "Please enter numbers or generate an array first.")
            return

        try:
            self.original_array = list(map(int, input_str.split(','))) 
        except ValueError:
            messagebox.showerror("Error", "Invalid input! Please enter integers separated by commas.")
            return

        if len(self.original_array) == 0:
            messagebox.showerror("Error", "Array is empty!")
            return

        self.time_label.config(text="Sorting...")
        self.current_step = 0

        alg = self.alg_menu.get()
        arr_copy = self.original_array.copy()

        if alg == "Merge Sort":
            self.animations, sorted_arr = merge_sort_with_animations(arr_copy)
        elif alg == "Insertion Sort":
            self.animations, sorted_arr = insertion_sort_with_animations(arr_copy)
        elif alg == "Counting Sort":
            self.animations, sorted_arr = counting_sort_with_animations(arr_copy)
        elif alg == "Selection Sort":
            self.animations, sorted_arr = selection_sort_with_animations(arr_copy)
        else:
            messagebox.showerror("Error", "Please select a valid algorithm.")
            return

        self.start_time = time.perf_counter()
        self.array = self.original_array.copy()
        self.sorted_arr = sorted_arr
        self.animate()


    def draw_array(self, color_positions={}):
        self.canvas.delete("all")
        if not self.array:
            return
        c_width = 780
        c_height = 350
        bar_width = c_width / len(self.array)
        max_val = max(self.array)

        for i, val in enumerate(self.array):
            x0 = i * bar_width
            y0 = c_height - (val / max_val) * (c_height - 20)
            x1 = (i + 1) * bar_width
            y1 = c_height

            color = color_positions.get(i, "#3498db")
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")
            self.canvas.create_text(x0 + bar_width/2, y0 - 10, text=str(val), fill="white", font=("Arial", 10, "bold"))

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()
