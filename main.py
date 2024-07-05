import time
import tkinter as tk
import math
import win32api

screen = [[0 for _ in range(32)] for _ in range(32)]
screen_str = ""

window = tk.Tk()
window.title("LED Matrix")
window.geometry("640x640")
window.configure(bg='black')

canvas = tk.Canvas(window, width=640, height=640, bg='black')
canvas.pack()

class Pixel:
    def __init__(self, x, y):
        self.x = x
        self.y = y

PIXELS = [
    Pixel(15, 0),
    Pixel(0, 30),
    Pixel(0, 15),
    Pixel(30, 30),
    Pixel(30, 15)
]


def draw_on_canvas():
    canvas.delete("all")
    for i in range(32):
        for j in range(32):
            if screen[j][i]:
                canvas.create_rectangle(i*20, j*20, (i+1)*20, (j+1)*20, fill="white")
            else:
                canvas.create_rectangle(i*20, j*20, (i+1)*20, (j+1)*20, fill="black")

def set_pixel(p):
    global screen

    screen[p.y][p.x] = 1

def clear_pixel(p):
    global screen

    screen[p.y][p.x] = 0

def clear_screen():
    global screen

    screen = [[0 for _ in range(32)] for _ in range(32)]

def link_pixels(p1, p2):
    global screen

    dx = p2.x - p1.x
    dy = p2.y - p1.y

    if abs(dx) > abs(dy):
        if dx > 0:
            for x in range(p1.x, p2.x + 1):
                if dx != 0:
                    y = p1.y + dy * (x - p1.x) // dx
                    screen[y][x] = 1
        else:
            for x in range(p2.x, p1.x + 1):
                if dx != 0:
                    y = p2.y + dy * (x - p2.x) // dx
                    screen[y][x] = 1
    else:
        if dy > 0:
            for y in range(p1.y, p2.y + 1):
                if dy != 0:
                    x = p1.x + dx * (y - p1.y) // dy
                    screen[y][x] = 1
        else:
            for y in range(p2.y, p1.y + 1):
                if dy != 0:
                    x = p2.x + dx * (y - p2.y) // dy
                    screen[y][x] = 1

def update_screen():

    set_pixel(PIXELS[0])

    clear_pixel(PIXELS[1])
    PIXELS[1].x = math.floor(15 + 15 * math.cos(time.time()))
    set_pixel(PIXELS[1])
    PIXELS[2].x = math.floor(15 + 15 * math.cos(time.time() + math.pi / 2))
    set_pixel(PIXELS[2])
    PIXELS[3].x = math.floor(15 + 15 * math.cos(time.time() + math.pi))
    set_pixel(PIXELS[3])
    PIXELS[4].x = math.floor(15 + 15 * math.cos(time.time() + 3 * math.pi / 2))
    set_pixel(PIXELS[4])

    link_pixels(PIXELS[0], PIXELS[1])
    link_pixels(PIXELS[0], PIXELS[2])
    link_pixels(PIXELS[0], PIXELS[3])
    link_pixels(PIXELS[0], PIXELS[4])

    link_pixels(PIXELS[1], PIXELS[2])
    link_pixels(PIXELS[2], PIXELS[3])
    link_pixels(PIXELS[3], PIXELS[4])
    link_pixels(PIXELS[4], PIXELS[1])

    

def main():
    global screen

    while not win32api.GetAsyncKeyState(0x20):
        update_screen()
        draw_on_canvas()
        window.update()
        clear_screen()
        time.sleep(0.01)

if __name__ == '__main__':
    main()