from anki import hooks
from aqt import mw
from aqt.qt import QDesktopServices, QUrl

QUESTION_KANJI_DETAILS_SEARCH_KEY = "8"
# search Jisho for the details of kanji in the question field of this card

SEARCH_URL = 'http://jisho.org/search/%s%%20%%23words'
SEARCH_KANJI_DETAILS_URL = 'http://jisho.org/search/%s%%20%%23kanji'


def add_shortcuts(shortcuts):
    additions = (
        (QUESTION_KANJI_DETAILS_SEARCH_KEY, lambda: lookup_online(SEARCH_KANJI_DETAILS_URL, filter_kanji(mw.reviewer.card.q()))),
    )
    shortcuts += additions

def filter_kanji(text):
    # filters out everything but kanji
    kanji = [x for x in text if 19968 <= ord(x) <= 40895]
    return ''.join(kanji)

def filter_kana(text):
    # filters out everything but kanji and kana
    kana = [x for x in text if 19968 <= ord(x) <= 40895 or 12353 <= ord(x) <= 12438 or 12449 <= ord(x) <= 12538 or ord(x) == 12293]
    return ''.join(kana)

def lookup_online(url, searchterm):
    # searches based on a url and a term
    if searchterm: QDesktopServices.openUrl(QUrl(url % searchterm))

def add_lookup_action(view, menu):
    # context menu, search for kanji info or for word definitions
    selected = view.page().selectedText()
    if not selected:
        return
    selectedkanji = filter_kanji(selected)
    selectedkana = filter_kana(selected)
    if selectedkanji:
        suffixkanji = (selectedkanji[:20] + '..') if len(selectedkanji) > 20 else selectedkanji
        a = menu.addAction('Search "' + suffixkanji + '" for kanji')
        a.triggered.connect(lambda: lookup_online(SEARCH_KANJI_DETAILS_URL, selectedkanji))
    if selectedkana:
        suffixkana = (selectedkana[:20] + '..') if len(selectedkana) > 20 else selectedkana
        b = menu.addAction('Search "' + suffixkana + '" for definitions')
        b.triggered.connect(lambda: lookup_online(SEARCH_URL, selectedkana))

hooks.addHook("AnkiWebView.contextMenuEvent", add_lookup_action)
hooks.addHook("reviewStateShortcuts", add_shortcuts)
