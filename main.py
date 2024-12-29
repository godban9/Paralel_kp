import os
import threading

total_occurrences = 0
lock = threading.Lock()

def count_occurrences_in_file(file_path, search_string):
    count = 0
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                count += line.count(search_string)
    except Exception as e:
        print(f"Помилка обробки файлу {file_path}: {e}")
    return count

def process_file(file_path, search_string):
    global total_occurrences
    count = count_occurrences_in_file(file_path, search_string)
    with lock:
        total_occurrences += count

def traverse_directory(directory, search_string): # Функція для обходу директорії та створення потоків
    threads = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            thread = threading.Thread(target=process_file, args=(file_path, search_string))
            threads.append(thread)
            thread.start()

            if len(threads) >= 50:  #КІЛЬКІСТЬ ПОТОКІВ
                for t in threads:
                    t.join()
                threads = []

    for t in threads:
        t.join()

if __name__ == '__main__':
    search_string = input("Введіть строку для пошуку (3-5 символів): ")
    if len(search_string) < 3 or len(search_string) > 5:
        print("Довжина строки повинна бути від 3 до 5 символів.")
        exit(1)

    directory = os.getcwd()
    traverse_directory(directory, search_string)
    print(f"Загальна кількість входжень: {total_occurrences}")
