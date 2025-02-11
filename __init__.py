from aqt import mw
from aqt.utils import qconnect
from aqt.qt import QAction
import re

kanji_regex = re.compile(r"[\u4e00-\u9faf\u3400-\u4dbf]")


def tagNotes():
    config = mw.addonManager.getConfig(__name__)

    note_ids = mw.col.find_notes(f"deck:{config['deck']}")
    for note_id in note_ids:
        note = mw.col.get_note(note_id)
        field = note[config["field"]]
        filtered = kanji_regex.findall(field)

        ok = True
        for kanji in filtered:
            if kanji not in config["targets"]:
                ok = False
                break

        if ok:
            note.add_tag(config["tag"])
            mw.col.update_note(note)


def init():
    action = QAction("test", mw)
    qconnect(action.triggered, tagNotes)
    mw.form.menuTools.addAction(action)


init()
