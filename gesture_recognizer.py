class GestureRecognizer:

 def recognize(self, fingers):
    """
    Recognize a gesture from the finger-state list.

    Finger order:

    [Thumb, Index, Middle, Ring, Pinky]
    """

    if fingers is None or len(fingers) != 5:
        return "Unknown"

    # Convert everything to int
    fingers = [int(x) for x in fingers]

    # --------------------------------------------------
    # FIST
    # --------------------------------------------------

    if fingers == [0, 0, 0, 0, 0]:
        return "Fist"

    # --------------------------------------------------
    # OPEN PALM
    # --------------------------------------------------

    if fingers == [1, 1, 1, 1, 1]:
        return "Open Palm"

    # --------------------------------------------------
    # INDEX FINGER
    # --------------------------------------------------

    if fingers == [0, 1, 0, 0, 0]:
        return "Index"

    # --------------------------------------------------
    # INDEX + MIDDLE
    # --------------------------------------------------

    if fingers == [0, 1, 1, 0, 0]:
        return "Two Fingers"

    # --------------------------------------------------
    # THUMB
    # --------------------------------------------------

    if fingers == [1, 0, 0, 0, 0]:
        return "Thumb"

    # --------------------------------------------------
    # INDEX + MIDDLE + RING
    # --------------------------------------------------

    if fingers == [0, 1, 1, 1, 0]:
        return "Three Fingers"

    # --------------------------------------------------
    # INDEX + MIDDLE + RING + PINKY
    # --------------------------------------------------

    if fingers == [0, 1, 1, 1, 1]:
        return "Four Fingers"

    # --------------------------------------------------
    # THUMB + INDEX
    # --------------------------------------------------

    if fingers == [1, 1, 0, 0, 0]:
        return "Thumb + Index"

    # --------------------------------------------------
    # THUMB + PINKY
    # --------------------------------------------------

    if fingers == [1, 0, 0, 0, 1]:
        return "Thumb + Pinky"

    # --------------------------------------------------
    # THUMB + INDEX + MIDDLE
    # --------------------------------------------------

    if fingers == [1, 1, 1, 0, 0]:
        return "Thumb + Index + Middle"

    # --------------------------------------------------
    # THUMB + INDEX + MIDDLE + RING
    # --------------------------------------------------

    if fingers == [1, 1, 1, 1, 0]:
        return "Thumb + Index + Middle + Ring"

    # --------------------------------------------------
    # UNKNOWN
    # --------------------------------------------------

    return "Unknown"