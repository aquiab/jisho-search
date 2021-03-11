from anki import hooks
from aqt import mw
from aqt.qt import *

QUESTION_KANJI_DETAILS_SEARCH_KEY = "8"
# search Jisho for the details of kanji in the question field of this card

SEARCH_URL = 'http://jisho.org/search/%s'
SEARCH_KANJI_DETAILS_URL = 'http://jisho.org/search/%s%%20%%23kanji'


def add_shortcuts(shortcuts):
    additions = (
            (QUESTION_KANJI_DETAILS_SEARCH_KEY, lambda: search_question_kanji()),
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
    # searches based on an url and a term
    QDesktopServices.openUrl(QUrl(url % searchterm))


def search_question_kanji():
    # get everything on question side, filter and search for kanji
    q = mw.reviewer.card.q()
    filtered = filter_kanji(q)
    lookup_online(SEARCH_KANJI_DETAILS_URL, filtered)


def add_lookup_action(view, menu):
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
