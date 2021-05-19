import numpy as np
import win32clipboard
import tempfile


def np_from_clipboard(delimiter=None):
    with tempfile.TemporaryFile() as tf:
        win32clipboard.OpenClipboard()
        tf.write(win32clipboard.GetClipboardData().encode())
        tf.seek(0)
        win32clipboard.CloseClipboard()

        return np.genfromtxt(tf, delimiter=delimiter)


def np_to_clipboard(arr):
    with tempfile.TemporaryFile() as tf:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        np.savetxt(tf, arr)
        tf.seek(0)
        s = tf.read().decode()
        print(s)
        win32clipboard.SetClipboardText(s.strip())
        win32clipboard.CloseClipboard()
