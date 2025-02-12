from aqt import mw
from aqt.utils import qconnect
from aqt.qt import *
import re

kanji_regex = re.compile(r"[\u4e00-\u9faf\u3400-\u4dbf]")


class TaggingDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)

        config = mw.addonManager.getConfig(__name__)

        self.setWindowTitle("Quick Tag Kanji")
        self.layout = QVBoxLayout()

        self.deckSelect = QLineEdit()
        self.deckSelect.setText(config["deck"])
        self.layout.addWidget(QLabel("Deck"))
        self.layout.addWidget(self.deckSelect)

        self.fieldSelect = QLineEdit()
        self.fieldSelect.setText(config["field"])
        self.layout.addWidget(QLabel("Field"))
        self.layout.addWidget(self.fieldSelect)

        self.tagEdit = QLineEdit()
        self.tagEdit.setText(config["tag"])
        self.layout.addWidget(QLabel("Tag"))
        self.layout.addWidget(self.tagEdit)

        self.targetKanji = QPlainTextEdit()
        self.targetKanji.setPlainText(config["targets"])
        self.layout.addWidget(QLabel("Target Kanji"))
        self.layout.addWidget(self.targetKanji)

        buttonLayout = QHBoxLayout()
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.reject)
        buttonLayout.addWidget(self.cancelButton)

        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.saveConfig)
        buttonLayout.addWidget(self.saveButton)

        self.button = QPushButton("Save and Tag Notes")
        self.button.clicked.connect(self.tagNotes)
        self.button.setDefault(True)
        buttonLayout.addWidget(self.button)
        self.layout.addLayout(buttonLayout)

        self.setLayout(self.layout)

    def buildNewConfig(self):
        return {
            "targets": self.targetKanji.toPlainText(),
            "deck": self.deckSelect.text(),
            "field": self.fieldSelect.text(),
            "tag": self.tagEdit.text(),
        }

    def saveConfig(self):
        mw.addonManager.writeConfig(__name__, self.buildNewConfig())

    def tagNotes(self):
        self.saveConfig()
        config = self.buildNewConfig()

        note_ids = mw.col.find_notes(f"deck:{config['deck']}")
        for note_id in note_ids:
            note = mw.col.get_note(note_id)
            field = note[config["field"]]
            filtered = "".join(kanji_regex.findall(field))

            ok = True
            note["Notes"] += filtered
            mw.col.update_note(note)
            for kanji in filtered:

                if kanji not in config["targets"]:
                    ok = False
                    break

            if ok:
                note.add_tag(config["tag"])
                mw.col.update_note(note)


def showTaggingDialog():
    mw.taggingDialog = dialog = TaggingDialog()
    dialog.show()


def init():
    action = QAction("Quick Tag Kanji", mw)
    qconnect(action.triggered, showTaggingDialog)
    mw.form.menuTools.addAction(action)


init()
