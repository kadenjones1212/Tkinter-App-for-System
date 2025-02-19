import tkinter as tk, time

class Stopwatch:
    def __init__(s, r):
        s.t = s.e = 0
        s.r, s.run = r, False
        r.title("Stopwatch")
        s.l = tk.Label(r, text="00:00:000", font=("Arial", 30))
        s.l.pack(pady=20)
        for t, c in [("Start", s.start), ("Stop", s.stop), ("Reset", s.reset)]:
            tk.Button(r, text=t, command=c, width=10).pack(side="left", padx=5)
        s.update()

    def start(s): s.t, s.run = time.perf_counter() - s.e, True
    def stop(s): s.e, s.run = time.perf_counter() - s.t, False
    def reset(s): s.e, s.run = 0, False; s.l.config(text="00:00:000")

    def update(s):
        if s.run: s.e = time.perf_counter() - s.t
        m, ms = divmod(int(s.e * 1000), 60000)
        s.l.config(text=f"{m:02}:{(ms//1000)%60:02}:{ms%1000:03}")
        s.r.after(10, s.update)

Stopwatch(tk.Tk()).r.mainloop()
