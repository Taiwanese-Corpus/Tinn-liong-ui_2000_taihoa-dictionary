# 轉到臺灣言語資料庫

## 流程

## 匯入資料庫
在`臺灣言語資料庫`專案目錄下
```bash
git clone https://github.com/Taiwanese-Corpus/ungian_taihoa_dictionary.git
sudo apt-get install -y python3 python-virtualenv
virtualenv --python=python3 venv
. venv/bin/activate
pip install -r moedict-data-twblg/轉到臺灣言語資料庫/requirements.txt
echo "from 轉到臺灣言語資料庫.整合到資料庫 import 走 ; 走()" | PYTHONPATH=moedict-data-twblg python manage.py shell
```

## 開發試驗
在`ungian_taihoa_dictionary`專案目錄下
```
sudo apt-get install -y python3 python-virtualenv
virtualenv --python=python3 venv
. venv/bin/activate
pip install -r 轉到臺灣言語資料庫/requirements.txt
python -m unittest 
```
