# Clip-OCR

<img width="50%" alt="SCR-20230502-nedr" src="https://tk-2025.oops.jp//git/Clip_OCR/images/Clip_OCR_Window.png">

## 目次
- [ダウンロード](#download)
- [使い方](#how_to_use)
- [プロジェクトについて](#project)
    - [概要](#description)
    - [製作のきっかけ](#reason_for_production)
    - [所感]
- [他のOCRアプリに対する優位性](#predominance)
    - [精度](#accuracy)
    - [改行とインデント](#new_line_and_indent)
    - [ショートカットキー](#short_cut_key)

---

<a id="download"></a>
以下のリンクからEXE化した本アプリをダウンロードすることができます。
- [ダウンロードリンク](https://tk-2025.oops.jp/app/ocr/Clip_OCR)（Windows10, 11でのみ動作確認済みです）

<a id="how_to_use"></a>

動画参照

---

<a id="description"></a>

#### 説明
- Windowsのスクリーンショット機能（Windows + Shift + S または PrintScreen など）からOCR（[Tesseract](https://ja.wikipedia.org/wiki/Tesseract_(%E3%82%BD%E3%83%95%E3%83%88%E3%82%A6%E3%82%A7%E3%82%A2))）機能を扱えるようにしたアプリのプログラムです。

<a id="reason_for_production"></a>

#### 製作のきっかけ

- プログラミングの授業で、教員のPC画面が配信され、記述されるプログラムを自身の環境に落とし込んでいくというものがありました。配信される画面をそのままOCR処理することができれば自身の負担を軽減できると考え、本アプリを製作するに至りました。

<!-- #### 所感 -->

---

<a id="accuracy"></a>

#### 精度
- 有名なOCRアプリのPower Toysと比較です。

![参考画像](https://tk-2025.oops.jp//git/Clip_OCR/images/image.png)
写真青色の部分をOCR処理して比較します。

Power Toys (Text Extractor)：
`テキスト抽出子は、 OCR バックがインスト ー ルされている言語のみを認識できます。サポ ー トされている言語に関する詳細情報`

Clip OCR：
`テキスト抽出子は、OCRパックがインストールされている言語のみを認識できます。サポートされている言語に関する詳細情報`

Power Toysでは`OCRパック`が`OCR バック`となっていたり、ー（長音記号）に不要なスペース（`インスト ー ル`, `サポ ー ト`）が入ってしまっていますが、Clip OCRでは問題なく再現することができています。

---

<a id="new_line_and_indent"></a>

#### 改行とインデント

- ソースコードでの例です。以下のように複雑な改行やインデントがある場合でも問題なくOCR処理を行うことができます。（優先する言語を英語にした場合）

```python
while True:
    try:#極稀に画像参照時に謎のエラーが出ることがある繰り返すとエラーは出ない
        new_image = ImageGrab.grabclipboard()
        #画像じゃやないときcontinue
        if not new_image:
            return
        break
    except:
        continue
```
<!-- （ここに動画） -->

---

<a id="short_cut_key"></a>

#### ショートカットキー
- アプリを起動してスクリーンショットを撮るだけなので、新しいショートカットキーを覚えておく必要はありません。
スクリーンショット後`Windows + V`を使うことで、スクリーンショットの写真とOCR処理した内容をどちらも扱うことができます。