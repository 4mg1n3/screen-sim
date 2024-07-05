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


x0 = 15
y0 = 0
x1 = 0
y1 = 30
x2 = 31
y2 = 30
x3 = 0
y3 = 30
x4 = 31
y4 = 30


def draw_on_canvas():
    canvas.delete("all")
    for i in range(32):
        for j in range(32):
            if screen[j][i]:
                canvas.create_rectangle(i*20, j*20, (i+1)*20, (j+1)*20, fill="white")
            else:
                canvas.create_rectangle(i*20, j*20, (i+1)*20, (j+1)*20, fill="black")

def set_pixel(x, y):
    global screen

    screen[y][x] = 1

def clear_pixel(x, y):
    global screen

    screen[y][x] = 0

def clear_screen():
    global screen

    screen = [[0 for _ in range(32)] for _ in range(32)]

def link_pixels(x1, y1, x2, y2):
    global screen

    dx = x2 - x1
    dy = y2 - y1

    if dx == 0:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            screen[y][x1] = 1
    elif dy == 0:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            screen[y1][x] = 1
    else:
        m = dy / dx
        b = y1 - m * x1

        if abs(dx) >= abs(dy):
            for x in range(min(x1, x2), max(x1, x2) + 1):
                y = math.floor(m * x + b)
                screen[y][x] = 1
        else:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                x = math.floor((y - b) / m)
                screen[y][x] = 1

def update_screen():
    global x1, y1, x2, y2, x3, y3, x4, y4

    set_pixel(x0, y0)

    clear_pixel(x1, y1)
    x1 = math.floor(15 + 15 * math.cos(time.time()))
    set_pixel(x1, y1)
    x2 = math.floor(15 + 15 * math.cos(time.time() + math.pi))
    set_pixel(x2, y2)
    x3 = math.floor(15 + 15 * math.cos(time.time() + math.pi / 2))
    set_pixel(x3, y3)
    x4 = math.floor(15 + 15 * math.cos(time.time() + 3 * math.pi / 2))
    set_pixel(x4, y4)

    link_pixels(x0, y0, x1, y1)
    link_pixels(x0, y0, x2, y2)
    link_pixels(x0, y0, x3, y3)
    link_pixels(x0, y0, x4, y4)

    link_pixels(x1, y1, x2, y2)
    link_pixels(x2, y2, x3, y3)
    link_pixels(x3, y3, x4, y4)
    link_pixels(x4, y4, x1, y1)
    

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