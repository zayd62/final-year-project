# Python 3, function
# Author: J.Hadida (jhadida87 at ggooglemail)
# https://gist.github.com/Sheljohn/68ca3be74139f66dbc6127784f638920

# RED_BOLD_UNDERLINE = '\x1b[1;4;31m{}\x1b[0m'
# BLUE_UNDERLINE = '\x1b[4;34m{}\x1b[0m'
# GREEN = '\x1b[32m{}\x1b[0m'
def cstring(fmt, fg=None, bg=None, style=None):
    """
    Colour-printer.

    cstring('Hello!' )                             # normal
    cstring('Hello!', fg='g' )                     # green
    cstring('Hello!', fg='r', style='bx' )         # bold red blinking

    List of colours (for fg and bg):
        k   black
        r   red
        g   green
        y   yellow
        b   blue
        m   magenta
        c   cyan
        w   white

    List of styles:
        b   bold
        i   italic
        u   underline
        s   strikethrough
        x   blinking
        r   reverse
        y   fast blinking
        f   faint
        h   hide
    """

    COLCODE = {
        'k': 0,  # black
        'r': 1,  # red
        'g': 2,  # green
        'y': 3,  # yellow
        'b': 4,  # blue
        'm': 5,  # magenta
        'c': 6,  # cyan
        'w': 7  # white
    }

    FMTCODE = {
        'b': 1,  # bold
        'f': 2,  # faint
        'i': 3,  # italic
        'u': 4,  # underline
        'x': 5,  # blinking
        'y': 6,  # fast blinking
        'r': 7,  # reverse
        'h': 8,  # hide
        's': 9,  # strikethrough
    }

    # properties
    props = []
    if isinstance(style, str):
        props = [FMTCODE[s] for s in style]
    if isinstance(fg, str):
        props.append(30 + COLCODE[fg])
    if isinstance(bg, str):
        props.append(40 + COLCODE[bg])

    # display
    props = ';'.join([str(x) for x in props])
    if props:
        return('\x1b[%sm%s\x1b[0m' % (props, fmt))
    else:
        return(fmt)

def strip_dir(path):
    """
    take an absolute path and return just the filename
    """
    return os.path.basename(path)