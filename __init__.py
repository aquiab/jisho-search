from anki import hooks
from aqt import mw
from aqt.qt import QDesktopServices, QUrl

config = mw.addonManager.getConfig(__name__)

QUESTION_KANJI_DETAILS_SEARCH_KEY = config["QUESTION_KANJI_DETAILS_SEARCH_KEY"]
# search Jisho for the details of kanji in the question field of this card

SEARCH_URL = 'http://jisho.org/search/%s'
SEARCH_KANJI_DETAILS_URL = 'http://jisho.org/search/%s%%20%%23kanji'
KANJI_TO_IGNORE = config["KANJI_TO_IGNORE"]

def add_shortcuts(shortcuts):
    additions = (
        (QUESTION_KANJI_DETAILS_SEARCH_KEY, lambda: lookup_online(SEARCH_KANJI_DETAILS_URL, keep_kanji(mw.reviewer.card.q()))),
    )
    shortcuts += additions

def filter_kanji_to_ignore(text):
    # filters out the substrings defined in KANJI_TO_IGNORE
    for substring in KANJI_TO_IGNORE:
        text = text.replace(substring, '')
    return text

def keep_kanji(text):
    # filters out everything but kanji
    text = filter_kanji_to_ignore(text)
    kanji = [x for x in text if 19968 <= ord(x) <= 40895]
    return ''.join(kanji)

def keep_kanji_kana(text):
    # filters out everything but kanji and kana
    text = filter_kanji_to_ignore(text)
    kanji_kana = [x for x in text if 19968 <= ord(x) <= 40895 or 12353 <= ord(x) <= 12438 or 12449 <= ord(x) <= 12538 or ord(x) == 12293]
    return ''.join(kanji_kana)

def lookup_online(url, searchterm):
    # searches based on a url and a term
    if searchterm: QDesktopServices.openUrl(QUrl(url % searchterm))

def add_lookup_action(view, menu):
    # context menu, search for kanji info or for word definitions
    selected = view.page().selectedText()
    if not selected:
        return
    selected_kanji = keep_kanji(selected)
    selected_kanji_kana = keep_kanji_kana(selected)
    if selected_kanji:
        suffix_kanji = (selected_kanji[:20] + '..') if len(selected_kanji) > 20 else selected_kanji
        a = menu.addAction('Search "' + suffix_kanji + '" for kanji')
        a.triggered.connect(lambda: lookup_online(SEARCH_KANJI_DETAILS_URL, selected_kanji))
    if selected_kanji_kana:
        suffix_kana = (selected_kanji_kana[:20] + '..') if len(selected_kanji_kana) > 20 else selected_kanji_kana
        b = menu.addAction('Search "' + suffix_kana + '" for definitions')
        b.triggered.connect(lambda: lookup_online(SEARCH_URL, selected_kanji_kana))

hooks.addHook("AnkiWebView.contextMenuEvent", add_lookup_action)
hooks.addHook("reviewStateShortcuts", add_shortcuts)