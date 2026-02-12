from parsing import HHParser
from cleaning import Cleaner
from config import CONFIG, CLEAN_PATH, DIRTY_PATH, HEADERS
import subprocess
import sys
import os


def need_to_parse():
    return not os.path.exists(DIRTY_PATH)

def need_to_clean():
    return not os.path.exists(CLEAN_PATH)


if __name__ == '__main__':

    if need_to_parse():
        print("Сырые данные не найдены. Запускаем парсер...")
        parser = HHParser(HEADERS)
        parser.run(DIRTY_PATH) 
    else:
        print("Сырые данные уже есть. Пропускаем парсинг.")

    if need_to_clean():
        print("Чистые данные не найдены. Запускаем очистку...")
        cleaner = Cleaner(CONFIG)
        cleaner.run(DIRTY_PATH, CLEAN_PATH)
    else:
        print("Чистые данные уже есть. Пропускаем очистку.")

    app_path = os.path.join(os.path.dirname(__file__), '..', 'dashboard', 'app.py')
    print(f"Запускаем дашборд: {app_path}")
    subprocess.run([sys.executable, '-m', 'streamlit', 'run', app_path])

