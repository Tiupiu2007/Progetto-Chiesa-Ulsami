

import tkinter as tk
import ctypes

# Fix DPI
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

class VectorBoard(tk.Tk):
    def __init__(self, width=800, height=600):
        super().__init__()
        self.title("Lavagna Vettoriale")
        self.geometry("1000x700")
        self.configure(bg="#1e1e1e")

        # Font e DPI
        self.option_add("*Font", ("Segoe UI", 12))
        try:
            dpi = self.winfo_fpixels('1i')
            self.tk.call("tk", "scaling", dpi / 72.0)
        except:
            pass

        # --- Main frame con grid ---
        main_frame = tk.Frame(self, bg="#1e1e1e")
        main_frame.pack(fill="both", expand=True)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(2, weight=1)  # canvas espande

        # Toolbar
        self.toolbar = tk.Frame(main_frame, bg="#252526", width=220)
        self.toolbar.grid(row=0, column=0, sticky="ns")
        self.toolbar.grid_propagate(False)  # importante per width fissa
        self.toolbar.grid_rowconfigure(0, weight=0)
        self.toolbar.grid_rowconfigure(1, weight=0)
        self.toolbar.grid_rowconfigure(2, weight=1)  # spazio vuoto in basso
        self.toolbar.grid_columnconfigure(0, weight=1)

        # Controlli toolbar con grid
        tk.Label(self.toolbar, text="Larghezza:", fg="#d4d4d4", bg="#252526").grid(row=0, column=0, sticky="w", padx=10, pady=(15, 5))
        self.width_entry = tk.Entry(self.toolbar, bg="#1e1e1e", fg="#d4d4d4", insertbackground="#d4d4d4", relief="flat")
        self.width_entry.insert(0, str(width))
        self.width_entry.grid(row=1, column=0, sticky="ew", padx=10, pady=5, ipady=4)

        tk.Label(self.toolbar, text="Altezza:", fg="#d4d4d4", bg="#252526").grid(row=2, column=0, sticky="w", padx=10, pady=(15, 5))
        self.height_entry = tk.Entry(self.toolbar, bg="#1e1e1e", fg="#d4d4d4", insertbackground="#d4d4d4", relief="flat")
        self.height_entry.insert(0, str(height))
        self.height_entry.grid(row=3, column=0, sticky="ew", padx=10, pady=5, ipady=4)

        tk.Button(self.toolbar, text="Applica", command=self.resize_paper,
                  bg="#0e639c", fg="#ffffff", activebackground="#1177bb", relief="flat").grid(row=4, column=0, sticky="ew", padx=10, pady=20, ipady=5)

        # Divider
        divider = tk.Frame(main_frame, bg="#3c3c3c", width=4, cursor="sb_h_double_arrow")
        divider.grid(row=0, column=1, sticky="ns")
        divider.bind("<ButtonPress-1>", self.start_resize)
        divider.bind("<B1-Motion>", self.do_resize)

        # Canvas
        self.canvas = tk.Canvas(main_frame, bg="#1e1e1e", highlightthickness=0)
        self.canvas.grid(row=0, column=2, sticky="nsew")

        # Foglio
        self.paper_width = width
        self.paper_height = height
        self.paper = self.canvas.create_rectangle(0, 0, 0, 0, fill="#f3f3f3", outline="#cccccc", width=1)

        # Spazio infinito
        BIG = 10000
        self.canvas.configure(scrollregion=(-BIG, -BIG, BIG, BIG))
        self.bind("<Configure>", lambda e: self.center_paper())

        # Pan e zoom
        self.canvas.bind("<ButtonPress-2>", self.start_pan)
        self.canvas.bind("<B2-Motion>", self.do_pan)
        self.canvas.bind("<MouseWheel>", self.zoom)
        self.canvas.bind("<Button-4>", self.zoom)
        self.canvas.bind("<Button-5>", self.zoom)

        self.zoom_factor = 1.0

    # --- Resize toolbar ---
    def start_resize(self, event):
        self._resize_start_x = self.winfo_pointerx()
        self._toolbar_orig_width = self.toolbar.winfo_width()

    def do_resize(self, event):
        delta = self.winfo_pointerx() - self._resize_start_x
        new_width = self._toolbar_orig_width + delta
        new_width = max(100, min(500, new_width))
        self.toolbar.config(width=new_width)

    # --- Altri metodi ---
    def center_paper(self):
        cw = self.canvas.winfo_width()
        ch = self.canvas.winfo_height()
        x0 = (cw - self.paper_width) // 2
        y0 = (ch - self.paper_height) // 2
        x1 = x0 + self.paper_width
        y1 = y0 + self.paper_height
        self.canvas.coords(self.paper, x0, y0, x1, y1)

    def resize_paper(self):
        try:
            w = int(self.width_entry.get())
            h = int(self.height_entry.get())
            self.paper_width = w
            self.paper_height = h
            self.center_paper()
        except ValueError:
            print("Inserisci numeri validi")

    def start_pan(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def do_pan(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def zoom(self, event):
        if event.num == 4 or event.delta > 0:
            factor = 1.1
        elif event.num == 5 or event.delta < 0:
            factor = 0.9
        else:
            return
        self.zoom_factor *= factor
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.canvas.scale("all", x, y, factor, factor)


if __name__ == "__main__":
    app = VectorBoard()
    app.mainloop() 