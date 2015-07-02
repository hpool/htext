# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import six

from htext.ja import kana

DATA = [
    ("コーリャ", "こーりゃ"),
    ("アレクセイ・カラマーゾフ", "あれくせい・からまーぞふ"),
]


def test_invalid():
    def func(input, expected):
        output = kana.to_hiragana(input)
        assert isinstance(output, six.text_type) and output == expected

        output = kana.to_katakana(input)
        assert isinstance(output, six.text_type) and output == expected

    # not unicode
    for input, expected in (
            (1, '1'),
            (1.0, '1.0'),
            ('A', 'A'),
            (None, 'None')):
        yield func, input, expected

    # Neigther hiragana nor katakana
    for input in ("酒", "\u2200"):
        yield func, input, input


def test_to_hiragana():
    def func(input, expected):
        output = kana.to_hiragana(input)
        assert output == expected, "%s expected, got %s" % (expected, output)

    for i, e in DATA + [("ドウモト", "どうもと"),
                        ("ヴァスティッチ", "ばすてぃっち"),
                        ("イブラヒモヴィッチ", "いぶらひもびっち"),
                        ("ヴェンゲル", "べんげる"),
                        ("クリエイティヴ", "くりえいてぃぶ"),
                        ]:
        yield func, i, e


def test_to_katakana():
    def func(input, expected):
        output = kana.to_katakana(input)
        assert output == expected, "%s expected, got %s" % (expected, output)

    for e, i in DATA + [("ドウモト", "どうもと"),
                        ("バスティッチ", "ばすてぃっち"),
                        ("イブラヒモビッチ", "いぶらひもびっち"),
                        ("ベンゲル", "べんげる"),
                        ]:
        yield func, i, e


def test_to_hiragana_seion():
    def func(input, expected):
        output = kana.to_hiragana_seion(input)
        assert output == expected, "%s expected, got %s" % (expected, output)

    for i, e in [("どうもと", "とうもと"),
                 ("ばすてぃっち", "はすていつち"),
                 ("いぶらひもびっち", "いふらひもひつち"),
                 ("べんげる", "へんける"),
                 ]:
        yield func, i, e


def test_to_katakana_seion():
    def func(input, expected):
        output = kana.to_katakana_seion(input)
        assert output == expected, "%s expected, got %s" % (expected, output)

    for i, e in [("ドウモト", "トウモト"),
                 ("バスティッチ", "ハステイツチ"),
                 ("イブラヒモビッチ", "イフラヒモヒツチ"),
                 ("ベンゲル", "ヘンケル"),
                 ]:
        yield func, i, e


def test_hiragana_to_katakana_unchanged():
    def func(input, expected):
        output = kana.to_katakana(input)
        assert output == expected, "%s expected, got %s" % (expected, output)

    for e, i in DATA:
        yield func, e, e


def test_katakana_to_hiragana_unchanged():
    def func(input, expected):
        output = kana.to_hiragana(input)
        assert output == expected, "%s expected, got %s" % (expected, output)

    for e, i in DATA:
        yield func, i, i


def test_mixed():
    output = kana.to_hiragana("カラマーゾフの兄弟")
    assert output == "からまーぞふの兄弟"

    output = kana.to_katakana("からまーぞふの兄弟")
    assert output == "カラマーゾフノ兄弟"


def test_kana_group():
    def func(input, expected):
        output = kana.get_kana_group(input)
        assert output == expected, "%s expected, got %s" % (expected, output)

    for input, expected in (("アリョーシャ", "あ"),
                            ("コーリャ", "か"),
                            ("サムソーノフ", "さ"),
                            ("タチアナ", "た"),
                            ("ナスターシャ", "な"),
                            ("フィリッポーヴナ", "は"),
                            ("ミーチャ", "ま"),
                            ("ユヴゲーニ・パーベルビチ", "や"),
                            ("ポルフィーリ ペトロヴィッチ", "は"),
                            ):
        yield func, input, expected


def test_kana_group_invalid_chars():
    def func(input_value, expected):
        output_value = kana.get_kana_group(input_value)
        assert output_value == expected, "%s expected, got %s" % (expected, output_value)

    for input_value, expected in (
            ('酒', None),
            ('', None),
            (None, None),
            (0, None)):
        yield func, input_value, expected


def test_compare():
    def func(a, b, expected):
        output = kana.compare(a, b)
        assert output == expected, "%s expected, got %s" % (expected, output)

    for a, b, expected in (
            ('アンジェラ・アキ', 'アンジェラアキ', 0),
            ('アイドリング!!!', 'アイドリング', 0),
            ('ゆず', 'ユズ', 0),
            ('あらし', 'アザラシ', 1),
            ('あらし', 'アリクイ', -1)):
        yield func, a, b, expected


def test_hard_normalize():
    value = """
        あいうえお かきくけこ さしすせそ たちつてと なにぬねの
        はひふへほ まみむめも やゆよ らりるれろ わをん
        がぎぐげご ざじずぜぞ だぢづでど ばびぶべぼ ぱぴぷぺぽ
        ガギグゲゴ ザジズゼゾ ダヂヅデド バビブベボ パピプペポ ヴ
        ぁぃぅぇぉ っゃゅょ ゐゑ ァィゥェォ ヵヶッャュョ ヰヱ
        ABCDE FGHIJ KLMNO PQRST UVWXYZ
         '",.*=-、。・「」『』
    """
    output = kana.hard_normalize(value, ignores=""" '",.*=-、。・「」『』""")
    expected = (
        'アイウエオカキクケコサシスセソタチツテトナニヌネノ'
        'ハヒフヘホマミムメモヤユヨラリルレロワヲン'
        'カキクケコサシスセソタチツテトハヒフヘホハヒフヘホ'
        'カキクケコサシスセソタチツテトハヒフヘホハヒフヘホウ'
        'アイウエオツヤユヨイエアイウエオカケツヤユヨイエ'
        'abcdefghijklmnopqrstuvwxyz'
    )
    assert output == expected, "{} expected, got {}".format(expected, output)
