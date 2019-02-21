from bearlibterminal import terminal


def handle_input(key=None):
    if key is None:
        if terminal.has_input():
            key = terminal.read()

    if key == terminal.TK_H or key == terminal.TK_KP_4 or key == terminal.TK_LEFT:
        return {"move": (-1, 0)}
    elif key == terminal.TK_L or key == terminal.TK_KP_6 or key == terminal.TK_RIGHT:
        return {"move": (1, 0)}
    elif key == terminal.TK_K or key == terminal.TK_KP_8 or key == terminal.TK_UP:
        return {"move": (0, -1)}
    elif key == terminal.TK_J or key == terminal.TK_KP_2 or key == terminal.TK_DOWN:
        return {"move": (0, 1)}
    elif key == terminal.TK_Y or key == terminal.TK_KP_7:
        return {"move": (-1, -1)}
    elif key == terminal.TK_U or key == terminal.TK_KP_9:
        return {"move": (1, -1)}
    elif key == terminal.TK_B or key == terminal.TK_KP_1:
        return {"move": (-1, 1)}
    elif key == terminal.TK_N or key == terminal.TK_KP_3:
        return {"move": (1, 1)}
    elif key == terminal.TK_PERIOD or key == terminal.TK_KP_0 or key == terminal.TK_KP_PERIOD:
        return {"move": (0, 0)}
    elif key == terminal.TK_ESCAPE or key == terminal.TK_CLOSE:
            return {"exit": True}

    return {}
