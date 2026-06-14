TYPE_RULES = [
    ("Safety", ["shall not","prevent","hazard","risk","collision","emergency"]),
    ("Functional", ["detect","control","activate","perform","ensure","comply"]),
    ("HMI", ["display","warning","signal","indicator","driver"]),
    ("Sensing", ["sensor","detect","monitor","perception"]),
    ("DataRecording", ["record","store","log","data"]),
    ("Documentation", ["documentation","declare","evidence"]),
    ("Verification", ["verify","tested","demonstrate","spot checks","audit","annex"]),
]


def is_requirement(s):
    s = s.lower()

    has_modal = any(k in s for k in ["shall", "must", "required"])
    has_action = any(k in s for k in [
        "detect","ensure","provide","prevent","activate","disable",
        "control","perform","comply","monitor","generate","implement",
        "record","store","declare","verify","assess","display"
    ])

    return has_modal and has_action


def classify_requirement(text):
    s = text.lower()

    for t, kws in TYPE_RULES:
        if any(k in s for k in kws):
            return t

    return "General"