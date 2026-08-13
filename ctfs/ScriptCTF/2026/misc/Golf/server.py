import subprocess, tempfile, pathlib, textwrap
from PIL import ImageFont, Image, ImageDraw
from rich.console import Console
from rich_pixels import Pixels

def check(code):
    font = ImageFont.truetype("DejaVuSans.ttf", 10, encoding='unic')

    if font.getlength(code) > 380:
        return "TOO LONG"

    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)
        lines = code.splitlines()
        width = int(max(font.getlength(line) for line in lines) + 4)
        height = len(lines) * 12 + 4

        img = Image.new("RGB", (width, height), "white")
        ImageDraw.Draw(img).multiline_text((2, 2), code, fill="black", font=font)

        img.save(td / "code.jpg")

        console = Console()
        pixels = Pixels.from_image_path(td / "code.jpg") 

        console.print(pixels)

        td = pathlib.Path(td)
        script = td / "submission.py"
        cfg = td / "nsjail.cfg"

        script.write_text(code, encoding="utf-8")

        cfg.write_text(textwrap.dedent(f"""
            name: "codecheck"
            mode: ONCE
            cwd: "/work"
            rlimit_as: 256
            rlimit_cpu: 1

            mount {{ src: "/lib", dst: "/lib", is_bind: true, rw: false }}
            mount {{ src: "/lib64", dst: "/lib64", is_bind: true, rw: false }}
            
            mount {{ src: "/usr/lib", dst: "/usr/lib", is_bind: true, rw: false }}
            mount {{ src: "/usr/bin/python3", dst: "/usr/bin/python3", is_bind: true, rw: false }}

            mount {{
              src: "{td}"
              dst: "/work"
              is_bind: true
              rw: true
            }}
        """).strip() + "\n", encoding="utf-8")

        out = subprocess.check_output(
            ["nsjail", "--config", str(cfg), "--", "/usr/bin/python3", "/work/submission.py"],
        ).decode().splitlines()
        goal =  [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                [35, 36, 37, 38, 39, 40, 41, 42, 43, 10],
                [34, 63, 64, 65, 66, 67, 68, 69, 44, 11],
                [33, 62, 83, 84, 85, 86, 87, 70, 45, 12],
                [32, 61, 82, 95, 96, 97, 88, 71, 46, 13],
                [31, 60, 81, 94, 99, 98, 89, 72, 47, 14],
                [30, 59, 80, 93, 92, 91, 90, 73, 48, 15],
                [29, 58, 79, 78, 77, 76, 75, 74, 49, 16],
                [28, 57, 56, 55, 54, 53, 52, 51, 50, 17],
                [27, 26, 25, 24, 23, 22, 21, 20, 19, 18]]
        good = True
        for i in range(10):
            good &= list(map(int, out[i].split())) == goal[i]
        return "flag" if good else "WA"

code = [input("Send python code (enter EOF when done):\n")]
while code[-1].strip() != "EOF":
    code.append(input())
print(check('\n'.join(code[:-1])))
