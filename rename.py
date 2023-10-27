import pathlib
from distutils.util import strtobool
from pprint import pprint
from time import localtime, sleep, strftime
from typing import TYPE_CHECKING, Optional

from tkinter import Button, Entry, Frame, Label, Tk, filedialog
from tkinter.ttk import Combobox, Progressbar
from tkinter.messagebox import showinfo, showerror

if TYPE_CHECKING:
    from tkinter import Misc


SINGLE_DIR_MODE = "Single dir"
INCLUDE_DIRS_MODE = "Include dirs"
PARALLEL_DIRS_MODE = "Parallel dirs"


class ProgressSelfBar(Progressbar):
    def update_percent(self, percent: float):
        """Percentage update progress bar."""
        self["value"] = percent * 100
        self.master.update()


class App(Frame):
    def __init__(self) -> None:
        master = Tk()
        master.title("Rename executor")

        width = master.winfo_screenwidth()
        height = master.winfo_screenheight()
        if width > 600 * 1.3 and height > 450 * 1.3:
            geometry_str = f"600x450+{width//2}+0"
        else:
            geometry_str = "%dx%d+%d+0" % (
                master.winfo_screenwidth() / 2,
                master.winfo_screenheight() / 2,
                master.winfo_screenwidth() / 2,
            )

        master.geometry(geometry_str)

        super().__init__(master=master)

        master.protocol("WM_DELETE_WINDOW", self.before_quit)
        self.master = master
        self.pack()  # 创建各个窗口组件

        self.comic_dir: Optional[pathlib.Path] = None
        self.comic_subdirs = []

        self.include_types = []

        self.modes = (SINGLE_DIR_MODE, INCLUDE_DIRS_MODE, PARALLEL_DIRS_MODE)

        self.total = 0
        self.current = 0

        self.create_widgets()

    def before_quit(self):
        super().quit()

    def create_widgets(self):
        self.progressbar = ProgressSelfBar(self, length=450, mode="determinate")
        self.progressbar.pack(pady=[5, 15])

        # 获取文件
        self.choose_dir_bt = Button(
            self, font=("黑体", 16), width=20, height=1, text="选择目录", command=self.get_dir
        )
        self.choose_dir_bt.pack(side="top")

        _ = Label(self, text="书名", anchor="w", width=55, font=("黑体", 14)).pack()
        self.et_title = Entry(self, show=None, width=50, font=("黑体", 16))
        self.et_title.pack()
        self.et_title.insert(0, "")

        _ = Label(self, text="Start Idx", anchor="w", width=55, font=("黑体", 14)).pack()
        self.idx_et = Entry(self, show=None, width=50, font=("黑体", 16))
        self.idx_et.pack()
        self.idx_et.insert(0, "1")

        _ = Label(
            self, text="Include Type", anchor="w", width=55, font=("黑体", 14)
        ).pack()
        self.include_et = Entry(self, show=None, width=50, font=("黑体", 16))
        self.include_et.pack()
        self.include_et.insert(0, ".jpg|.jpeg|.png")

        _ = Label(self, text="Date", anchor="w", width=55, font=("黑体", 14)).pack()
        self.date_et = Entry(self, show=None, width=50, font=("黑体", 16))
        self.date_et.pack()
        self.date_et.insert(0, strftime("%Y-%m-%d", localtime()))

        self.mode_box = Combobox(self, values=self.modes, state="readonly")
        self.mode_box.current(0)
        self.mode_box.pack(side="left")

        _ = Button(
            self,
            text="RENAME",
            font=("黑体", 16),
            width=20,
            height=1,
            command=self.do_rename,
        ).pack(side="bottom")

        _ = Button(
            self,
            text="CHECKING",
            font=("黑体", 16),
            width=20,
            height=1,
            command=self.do_checking,
        ).pack(side="bottom")

    def get_dir(self):
        comic_dir_str = str(filedialog.askdirectory(title="选择文件", initialdir=""))
        self.comic_dir = pathlib.Path(comic_dir_str)

        if not self.comic_dir:
            return

        print(f"Info:: Directory: {self.comic_dir}")

        self.et_title.insert(0, self.comic_dir.name)

    def refresh_include_type(self):
        self.include_types.clear()
        self.include_types.extend(self.include_et.get().strip().split("|"))

    def sub_rename(self, dir: pathlib.Path, start: int, target: pathlib.Path) -> int:
        print(f"Info:: Start rename [{dir}] ...")

        i = start
        for item in sorted(dir.iterdir()):
            # print("---", item, item.suffix)

            if item.suffix not in self.include_types:
                continue

            # rename to root dir.
            item.rename(pathlib.Path(target, f"{i:06}{item.suffix}"))
            i += 1
            self.current += 1
            self.progressbar.update_percent(self.current / self.total)

        print("Info:: End rename.")
        return i - start

    def do_rename(self):
        if not self.comic_dir:
            print("Warn:: No select directory.")
            return

        # refresh the types that need to be processed.
        self.refresh_include_type()

        cur_mode = self.modes[self.mode_box.current()]
        print(f"Info:: mode is [{cur_mode}]")

        i = int(self.idx_et.get())  # get start index

        if cur_mode == SINGLE_DIR_MODE:
            with self:
                self.sub_rename(self.comic_dir, i, self.comic_dir)
        elif cur_mode == INCLUDE_DIRS_MODE:
            with self:
                # only watch sub-dir.
                for sub_dir in sorted(self.comic_dir.iterdir()):
                    if sub_dir.is_dir():
                        print(f"Info:: Find sub-dir: {sub_dir}")
                        count = self.sub_rename(sub_dir, i, self.comic_dir)
                        i += count
        elif cur_mode == PARALLEL_DIRS_MODE:
            # only watch sub-dir.
            for sub_dir in sorted(self.comic_dir.iterdir()):
                if not sub_dir.is_dir():
                    continue

                with self:
                    print(f"Info:: Find sub-dir: {sub_dir}")
                    count = self.sub_rename(sub_dir, i, sub_dir)
        else:
            showerror("", "Not support mode.")

        # Reset bar.
        sleep(0.2)
        self.progressbar.update_percent(0)
        # showinfo("", "Finished rename!")

        # recheck = True
        # if recheck:
        #     for item in sorted(self.comic_dir.iterdir()):
        #         print("---", item, item.suffix)

        #     recheck_res = strtobool(input("Report:"))
        #     if not recheck_res:
        #         return

    def do_checking(self):
        pprint(sorted(self.comic_dir.iterdir()))

    def __enter__(self):
        # get new total.
        self.total = len(list(self.comic_dir.rglob("*")))
        print(f"Info: total page is {self.total}")

    def __exit__(self, type, value, trace):
        # Reset count index.
        self.current = 0


if __name__ == "__main__":
    app = App()
    try:
        app.mainloop()
    except BaseException:
        pass
    finally:
        app.before_quit()


#############################
# TODO：
