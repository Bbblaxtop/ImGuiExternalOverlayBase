import glfw
import OpenGL.GL as gl
import imgui
from imgui.integrations.glfw import GlfwRenderer
import win32gui
import win32con
import keyboard
import math

menu = True

def toggleMenu():
    global menu
    menu = not menu
    if menu:
        print("menu = True")
    else:
        print("menu = False")

def main():
    if not glfw.init():
        raise Exception("Could not initialize GLFW")
    
    glfw.window_hint(glfw.FLOATING, True)
    glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, True)
    glfw.window_hint(glfw.DECORATED, False)

    monitor = glfw.get_primary_monitor()
    video_mode = glfw.get_video_mode(monitor)
    screen_width, screen_height = video_mode.size.width, video_mode.size.height
    
    window = glfw.create_window(screen_width,screen_height-1, "Overlay", None, None)
    glfw.set_window_pos(window,0,0)
    glfw.make_context_current(window)

    hwnd = glfw.get_win32_window(window)
    ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    win32gui.SetWindowLong(
        hwnd,
        win32con.GWL_EXSTYLE,
        ex_style | win32con.WS_EX_LAYERED | win32con.WS_EX_TOPMOST,
    )
    win32gui.SetLayeredWindowAttributes(hwnd, 0x000000, 255, win32con.LWA_COLORKEY)

    keyboard.add_hotkey("insert",toggleMenu)

    imgui.create_context()
    impl = GlfwRenderer(window)

    slider_value = .5

    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()
        imgui.new_frame()

        if menu:
            imgui.begin("Cool ImGui")
            imgui.text("Hello world, from ImGui")
            imgui.text(f"FPS: {math.floor(imgui.get_io().framerate)}")
            if imgui.button("Click me!"):
                print("Button clicked!")
        
            changed, slider_value = imgui.slider_float("Slider", slider_value,0.0,0.1)
            if changed:
                print(f"Slider value: {slider_value:.2f}")
    
            imgui.end()

        gl.glClearColor(0,0,0,0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)
        

    impl.shutdown()
    glfw.terminate()

if __name__ == "__main__":
    main()