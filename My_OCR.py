from PIL import ImageGrab#, Image
import pyperclip
import pyocr
import os

class OCR():
    
    # def image_resizer(self, image, width_size:int=0, hight_size:int=0):
    #     """
    #     画像を黒色でパディングする

    #     Args:
    #         image (ndarray):
    #             numpy 配列の画像

    #         width_size (int, optional): 
    #             画像の幅が設定値よりも小さい場合に設定値のサイズでパディングする

    #         hight_size (int, optional): 
    #             画像の高さが設定値よりも小さい場合に設定値のサイズでパディングする

    #     Returns:
    #         パディングした画像を返却
    #     """
        
    #     y, x = image.shape[:2]
        
    #     if width_size:
    #         width_size -= x
    #         width_size = int(width_size / 2) if width_size > 0 else 0
        
    #     if hight_size:
    #         hight_size -= y
    #         hight_size = int(hight_size / 2) if hight_size > 0 else 0
        
    #     return cv2.copyMakeBorder(image, hight_size, hight_size, width_size, width_size, cv2.BORDER_CONSTANT, (0, 0, 0))

    def setup(self):
        """
        OCRのための各種設定
        """

        self.is_run = False
        self.X, self.Y = 0, 1

        current_directry = os.path.dirname(__file__)
        # os.environ['TESSDATA_PREFIX'] = os.path.join(current_directry, "tesseract_folder", "tessdata")

        pyocr.tesseract.TESSERACT_CMD = os.path.join(current_directry, "tesseract_folder", "tesseract.exe")
        self.tool = pyocr.get_available_tools()[0]
        self.builder = pyocr.builders.WordBoxBuilder(tesseract_layout=6)

    def set_run_flag(self, is_run:bool=False):
        """
        OCRの実行フラグを設定

        Args:
            is_run (bool, optional):
                OCR処理を実行する場合はTreu : OCR処理を停止する場合はFalse
        """

        self.is_run = is_run

    # def get_run_flag(self):
    #     """
    #     OCRの実行フラグを取得

    #     Returns:
    #         bool: Treuの場合OCR処理を実行 : Falseの場合OCR処理を停止
    #     """

    #     return self.is_run

    def ocr(self, language:str = "eng+jpn", paragraph_threshold_value:float = 1.0, space_and_newline:bool = True, detection_sound:bool = True):
        """
        クリップボード上の最新の値がテキストを含んでいる写真の場合にOCR処理を実行し、その結果をクリップボードにコピーします

        Args:
            language (str, optional):
                OCRで優先する言語

            paragraph_threshold_value (float, optional):
                改行の閾値（値を小さくすることで改行しやすくなる）

            space_and_newline (bool, optional):
                OCR結果にスペースと改行を含めるか

            detection_sound (bool, optional):
                OCR終了時に通知音を出力
        """

        if self.is_run:
            # print(f'引数の説明は以下を参考にしてください。\n\t"{os.path.join(current_directry, "Clipboard OCR")}" -h')

            while True:
                try:#極稀に画像参照時に謎のエラーが出ることがある　繰り返すとエラーは出ない
                    new_image = ImageGrab.grabclipboard()
                    # 画像じゃないときcontinue
                    if not new_image:
                        return
                    break
                except:
                    continue

            # 画像を最小の大きさでパディングする
            # new_image = self.image_paddinger(np.array(new_image.convert("RGB")), width_size=400, hight_size=400)
            # cv2.imshow("padding_image", new_image)

            # new_image = Image.fromarray(np.array(new_image))
            # new_image = Image.fromarray(new_image)
            # new_image.show()

            #OCR処理の実行
            result = self.tool.image_to_string (
                new_image,
                lang = language,
                builder = self.builder
                )

            #テキストが検出されなかったときにクリップボード最新の値を空文字で上書き（同じ画像を参照してループしないように）

            if result == []:
                pyperclip.copy("")
                return

            #利用する辞書、リスト、変数の初期化
            result_dict = {
                "up_left": [],
                "down_left": [],
                "down_right":[], 
                "text":[]
                }

            create_text_composition = []
            jpn_language_list = []
            output_text = []
            front_space = ""
            end_space = ""
            is_jpn = True

            # インデントの基準値を取得
            det_position = tuple(result[0].position)
            result_dict["up_left"].append(det_position[0])
            result_dict["down_right"].append(det_position[1])

            #OCR結果を展開
            for detection_list in result:
                det_text = detection_list.content
                det_position = tuple(detection_list.position)
                result_dict["down_left"].append((det_position[0][0], det_position[1][1]))
                result_dict["text"].append(det_text)

            # 改行、インデントの基準値を計算
            paragraph_threshold = (result_dict["down_left"][0][self.Y] - result_dict["up_left"][0][self.Y]) * paragraph_threshold_value
            space = (result_dict["down_right"][0][self.X] - result_dict["down_left"][0][self.X]) / len(result_dict["text"][0])
            standard_space_value = result_dict["down_left"][0][self.X]

            # 改行、インデントを適切に挿入する
            for index in range(len(result_dict["text"])-1):
                diff = result_dict["down_left"][index+1][self.Y] - result_dict["down_left"][index][self.Y]
                is_new_line, end_space = (True, "\n") if diff >= paragraph_threshold else (False, " ")
                create_text_composition.append(front_space + result_dict["text"][index] + end_space)
                front_space = " " * int(("{:.0f}").format((result_dict["down_left"][index+1][self.X] - standard_space_value) / space)) if is_new_line else ""

            create_text_composition.append(front_space + result_dict["text"][-1])

            # リストを一次元にする
            join_text = "".join(create_text_composition)
            
            # 日本語が入っている場合、分かち書きの不要な空白を削除
            for i in range(len(join_text) - 1):
                if join_text[i].isascii() == False or join_text[i+1].isascii() == False:
                    jpn_language_list.append(join_text[i])
                    is_jpn = False
                    continue
                else:
                    if is_jpn:
                        output_text.append(join_text[i])
                    else:
                        output_text.append(("".join(jpn_language_list) + join_text[i]).replace(" ", ""))
                        jpn_language_list = []
                        is_jpn = True

            if not jpn_language_list == []:
                output_text.append("".join(jpn_language_list).replace(" ", ""))

            output_text.append(join_text[-1])
            output_text = "".join(output_text)

            if not space_and_newline:
                output_text = output_text.replace("\n", "").replace(" ", "")

            # クリップボードにOCR結果をコピーする
            pyperclip.copy(output_text)

            # detection_soundがTrueの場合に処理終了を通知する
            if detection_sound:
                import winsound
                winsound.PlaySound("./", winsound.SND_FILENAME)