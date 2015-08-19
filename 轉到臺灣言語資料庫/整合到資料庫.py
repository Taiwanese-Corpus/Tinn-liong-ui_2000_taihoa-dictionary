# -*- coding: utf-8 -*-
from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 版權表
from csv import DictReader
from os.path import dirname, abspath, join
from posix import listdir
from 臺灣言語工具.音標系統.閩南語.教會羅馬字音標 import 教會羅馬字音標
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.解析整理.文章粗胚 import 文章粗胚
from 臺灣言語工具.解析整理.物件譀鏡 import 物件譀鏡
from 臺灣言語工具.解析整理.轉物件音家私 import 轉物件音家私


class 整合到資料庫:
    台文華文線頂辭典 = 來源表.objects.get_or_create(名='鄭良偉')[0]
    薛丞宏 = 來源表.objects.get_or_create(名='薛丞宏')[0]
    版權 = 版權表.objects.get_or_create(版權='無版權')[0]
    專案目錄 = join(dirname(abspath(__file__)), '..')
    公家內容 = {
        '來源': 台文華文線頂辭典,
        '版權': 版權,
        '種類': '字詞',
        '語言腔口': '閩南語',
        '著作所在地': '臺灣',
        '著作年': '2015',
    }
    _分析器 = 拆文分析器()
    _粗胚 = 文章粗胚()
    _譀鏡 = 物件譀鏡()
    _轉音家私 = 轉物件音家私()

    def 處理詞條(self, 詞條, 收錄者):
        公家內容 = {
            '收錄者': 收錄者,
        }
        公家內容.update(self.公家內容)

        if 詞條['台語漢字'] == '赤&#399' and 詞條['華語對譯'] == ';赤&#39918;;':
            詞條['台語漢字'] = '赤鯮'
            詞條['華語對譯'] = ';赤鯮;'

        for 華語 in 詞條['華語對譯'].strip(';').split(';'):
            華語內容 = {
                '外語語言': '華語',
                '外語資料': 華語.strip(),
            }
            華語內容.update(公家內容)
#             外語 = 外語表.加資料(華語內容)
            外語 = None
            self.加臺語詞條(公家內容, 詞條['ID'], 外語, 詞條['台語漢字'], 詞條['台語羅馬字'])
            if 詞條['台語羅馬字2'].strip() != '':
                self.加臺語詞條(公家內容, 詞條['ID'], 外語, 詞條['台語漢字'], 詞條['台語羅馬字2'])

    def 加臺語詞條(self, 公家內容, 編號, 外語, 漢字, 羅馬字):
        try:
            處理減號音標 = self._粗胚.建立物件語句前處理減號(教會羅馬字音標, 羅馬字)
            處理了音標 = self._粗胚.符號邊仔加空白(處理減號音標)
            原音章物件 = self._分析器.產生對齊章(漢字, 處理了音標)
            上尾章物件 = self._轉音家私.轉音(教會羅馬字音標, 原音章物件)
            型 = self._譀鏡.看型(上尾章物件)
            音 = self._譀鏡.看音(上尾章物件)
        except Exception as 錯誤:
            print(編號, 錯誤)
            型 = 漢字
            音 = 羅馬字

        臺語內容 = {
            '文本資料': 型,
            '屬性': {'音標': 音}
        }
        臺語內容.update(公家內容)
#         外語.翻母語(臺語內容)

    def 檢查資料有改過無(self):
        原始檔名 = join(self.專案目錄, '原始資料', 'Taihoa.csv')
        全部原始資料 = {}
        with open(原始檔名) as 原始檔案:
            for 一筆 in DictReader(原始檔案):
                全部原始資料[一筆['ID']] = 一筆
        for 一筆 in self.掠編輯過資料出來():
            原始資料 = 全部原始資料[一筆['ID']]
            for 欄位, 內容 in 一筆.items():
                if 欄位 in ['']:
                    if 內容.strip() not in ['', r'\\']:
                        raise RuntimeError('空欄位有資料：{}'.format(內容.strip()))
                    continue
                if 內容 != 原始資料[欄位]:
                    raise RuntimeError(
                        '資料有校對過，請看一下：{}、{}、{}、{}'.format(
                            欄位, 一筆['ID'], 原始資料[欄位], 內容
                        )
                    )

    def 掠編輯過資料出來(self):
        編輯過目錄 = join(self.專案目錄, '編輯過資料')
        for 檔名 in sorted(listdir(編輯過目錄)):
            with open(join(編輯過目錄, 檔名)) as 編輯過檔案:
                for 一筆 in DictReader(編輯過檔案):
                    yield 一筆


def 走(收錄者=整合到資料庫.薛丞宏):
    到資料庫 = 整合到資料庫()
    到資料庫.檢查資料有改過無()
    for _第幾个, 詞條 in enumerate(到資料庫.掠編輯過資料出來()):
        try:
            到資料庫.處理詞條(詞條, 收錄者)
        except Exception as e:
            print(詞條, e)
            raise
