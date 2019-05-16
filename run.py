import tkinter as tk
from tkinter import *
import speedtest  # speedtest-cli by Matt Martz
import time

VERBOSE = True
# TO_FILE = True  # TODO: implement


def one_test(decimal_places=2):
    servers = []
    s = speedtest.Speedtest()
    s.get_servers(servers)
    s.get_best_server()
    dt = str(time.ctime())
    s.download()
    s.upload()
    results = s.results.dict()
    # units for following are Mb/s [megabits per second]
    up = str(round(results['upload'] / (1024 * 1024), decimal_places))
    down = str(round(results['download'] / (1024 * 1024), decimal_places))
    if VERBOSE:
        print(dt + "\tDOWN\t" + down + "\tUP\t" + up)
    return up, down


def raise_above_all(window):
    window.attributes('-topmost', 1)
    window.attributes('-topmost', 0)
    window.focus_force()


class Application(tk.Frame):
    up_results = None
    down_results = None

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('Speed Test Application')
        self.master.geometry("300x120")
        self.master.resizable(False, False)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.info1 = tk.Text(self)
        self.info1["height"] = 2
        self.info1["width"] = 35
        self.set_info("Welcome!\nPress 'Run Test!' to begin")
        self.info1.config(state=DISABLED)
        self.info1.pack(side="top")

        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Run Test!"
        self.hi_there["command"] = self.get_results
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="Quit", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def get_results(self):
        self.set_info("Starting test...\n(this will take a bit)")
        self.update()
        up, down = one_test()
        # self.up_results, self.down_results = one_test()  # TODO: threading
        self.set_info(None, up, down)
        raise_above_all(root)
        # TODO: threading
        # self.info1.config(state=NORMAL)
        # self.info1.delete(1.0, END)
        # self.info1.insert(INSERT, "DOWNLOAD\t" + self.down_results + units)
        # self.info1.insert(INSERT, "\nUPLOAD\t" + self.up_results + units)
        # self.info1.config(state=DISABLED)

    def set_info(self, msg, up=None, dow=None):
        if msg is not None:
            self.info1.config(state=NORMAL)
            self.info1.delete(1.0, END)
            self.info1.insert(INSERT, msg)
            self.info1.config(state=DISABLED)
        else:
            assert up is not None
            assert dow is not None
            uni = "\tMb/s"
            self.set_info("DOWNLOAD\t" + dow + uni + "\nUPLOAD\t" + up + uni)


def main():
    app.pack()
    app.mainloop()
    # print(one_test())  # for testing
    pass


root = Tk()
app = Application(master=root)
main()
