import os
import pathlib

dir_p = pathlib.Path(input("Dir path:"))
if not dir_p.is_dir:
    raise Exception(f"Is not dir: {dir_p}")

start_i = int(input("Rename start index:"))
for item in sorted(dir_p.iterdir()):
    # print(f'{start_i:06}')
    print(item, item.suffix, type(item))
    item.rename(pathlib.Path(dir_p, f"{start_i:06}{item.suffix}"))
    start_i += 1
