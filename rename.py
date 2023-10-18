import pathlib
from distutils.util import strtobool
from time import localtime, sleep, strftime
from typing import TYPE_CHECKING, Optional

from tkinter import Button, Checkbutton, Entry, Frame, IntVar, Label, Tk, filedialog

if TYPE_CHECKING:
    from tkinter import _Cursor, _Relief, _ScreenUnits, _TakeFocusValue, Misc


class App(Frame):
    def __init__(self, master: Optional["Misc"] = None) -> None:
        super().__init__(master=master)

        master.protocol("WM_DELETE_WINDOW", self.before_quit)
        self.master = master
        self.pack()  # 创建各个窗口组件

        self.comic_dir: Optional[pathlib.Path] = None
        self.comic_subdirs = []

        self.include_types = []

        self.create_widgets()

    def before_quit(self):
        pass

    def create_widgets(self):
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

        self.is_multi_dir = IntVar()
        multi_dir_bt = Checkbutton(self, text="多文件夹", variable=self.is_multi_dir)
        multi_dir_bt.pack(side="left")

        _ = Button(
            self,
            text="RENAME",
            font=("黑体", 16),
            width=20,
            height=1,
            command=self.do_rename,
        ).pack(side="bottom")

    def get_dir(self):
        comic_dir_str = str(filedialog.askdirectory(title="选择文件", initialdir=""))
        self.comic_dir = pathlib.Path(comic_dir_str)

        if not self.comic_dir:
            return

        print(f"Info:: Directory: {self.comic_dir}")

        self.et_title.insert(0, self.comic_dir.name)

        # for dir in os.listdir(self.comic_dir):
        #     # print(dir)
        #     if os.path.isdir(self.comic_dir + os.sep + dir):
        #         self.quick_flag = True
        #         print(f"检测到目录 : {dir}")
        #         self.comic_subdirs.append(self.comic_dir + os.sep + dir)
        # # print(self.subdirs)

        # if self.quick_flag:
        #     print("即将进入快速制作书籍模式")
        #     sleep(3)
        # else:
        #     self.comic_subdirs.clear()
        #     self.comic_subdirs.append(self.comic_dir)

        # for subdir in self.comic_subdirs:
        #     # 初始化
        #     self.initNewBook()

        #     self.comic_dir = subdir

        #     self.et_title.delete(0, "end")
        #     if self.quick_flag:
        #         self.et_title.insert(
        #             0, self.comic_dir[self.comic_dir.rfind(os.sep) + 1 :]
        #         )
        #     else:
        #         self.et_title.insert(
        #             0, self.comic_dir[self.comic_dir.rfind("/") + 1 :]
        #         )

        #     # 生成目录结构，复制两个固定文件
        #     # start_new_thread(self.createDirectoryTree,())
        #     self.createDirectoryTree()

    def refresh_include_type(self):
        self.include_types.clear()
        self.include_types.extend(self.include_et.get().strip().split("|"))

    def sub_rename(self, dir: pathlib.Path, start: int) -> int:
        print(f"Info:: Start rename [{dir}] ...")

        i = start
        for item in sorted(self.comic_dir.iterdir()):
            print("---", item, item.suffix)

            # rename to root dir.
            item.rename(pathlib.Path(self.comic_dir, f"{i:06}{item.suffix}"))
            i += 1

        print("Info:: End rename.")
        return i - start

    def do_rename(self):
        if not self.comic_dir:
            print("Warn:: No select directory.")
            return

        # refresh the types that need to be processed.
        self.refresh_include_type()

        is_multi = self.is_multi_dir.get() == 1
        i = int(self.idx_et.get())  # get start index

        if is_multi:
            for sub_dir in sorted(self.comic_dir.iterdir()):
                if sub_dir.is_dir():
                    count = self.sub_rename(sub_dir, i)
                    i += count
        else:
            self.sub_rename(self.comic_dir, i)

        # recheck = True
        # if recheck:
        #     for item in sorted(self.comic_dir.iterdir()):
        #         print("---", item, item.suffix)

        #     recheck_res = strtobool(input("Report:"))
        #     if not recheck_res:
        #         return


if __name__ == "__main__":
    master = Tk()
    master.title("Rename")
    # root.geometry("500x400+650+300")
    master.geometry(
        "%dx%d+%d+0"
        % (
            master.winfo_screenwidth() / 2,
            master.winfo_screenheight(),
            master.winfo_screenwidth() / 2,
        )
    )
    app = App(master=master)
    try:
        app.mainloop()
    except BaseException:
        pass
    finally:
        app.beforeQuit()
