import json
import os
import uuid
import time
from natsort import natsorted

class VideoLesson:
    def __init__(self, title, description, author, duration, category, lesson_id=None):
        # Якщо ID не передано, генеруємо унікальний UUID
        self.id = lesson_id if lesson_id is not None else str(uuid.uuid4())
        self.title = title
        self.description = description
        self.author = author
        self.duration = duration  # тривалість у хвилинах
        self.category = category

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'author': self.author,
            'duration': self.duration,
            'category': self.category
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['title'],
            data['description'],
            data['author'],
            data['duration'],
            data['category'],
            lesson_id=data.get('id')
        )

    def __str__(self):
        return f"🆔 ID: {self.id} | 📚 Назва: {self.title} (📂 Категорія: {self.category}) ✍️ Автор: {self.author}, ⏱ Тривалість: {self.duration} хв. \n 📝 Опис: {self.description}"


class Catalog:
    def __init__(self, filename="catalog.json"):
        self.filename = filename
        self.lessons = []
        self.load_from_file()

    def find_lesson_index(self, lesson_id):
        for index, lesson in enumerate(self.lessons):
            if lesson.id == lesson_id:
                return index
        return -1

    def add_lesson(self, lesson):
        self.lessons.append(lesson)
        self.save_to_file()

    def edit_lesson(self, lesson_id, title=None, description=None, author=None, duration=None, category=None):
        index = self.find_lesson_index(lesson_id)
        if index != -1:
            lesson = self.lessons[index]
            if title is not None and title.strip() != "":
                lesson.title = title
            if description is not None and description.strip() != "":
                lesson.description = description
            if author is not None and author.strip() != "":
                lesson.author = author
            if duration is not None:
                lesson.duration = duration
            if category is not None and category.strip() != "":
                lesson.category = category
            self.save_to_file()
        else:
            print("Неправильний ID уроку для редагування.")

    def delete_lesson(self, lesson_id):
        index = self.find_lesson_index(lesson_id)
        if index != -1:
            del self.lessons[index]
            self.save_to_file()
        else:
            print("Неправильний ID уроку для видалення.")

    def filter_lessons(self, category=None, author=None):
        filtered = self.lessons
        if category:
            filtered = [lesson for lesson in filtered if lesson.category.lower() == category.lower()]
        if author:
            filtered = [lesson for lesson in filtered if lesson.author.lower() == author.lower()]
        return filtered

    def sort_lessons(self):
        print("Виберіть критерій сортування:")
        print("1. Тривалість")
        print("2. Назва")
        print("3. Автор")
        choice = input("Введіть номер критерію: ")

        if choice == '1':
            print("Оберіть порядок сортування за тривалістю:")
            print("1. Від меншого до більшого")
            print("2. Від більшого до меншого")
            order_choice = input("Введіть номер порядку: ")
            reverse = order_choice == '2'
            self.lessons.sort(key=lambda lesson: lesson.duration, reverse=reverse)
            print("Уроки відсортовано за тривалістю.")
        elif choice == '2':
            print("Оберіть порядок сортування за назвою:")
            print("1. За алфавітом (від A до Z)")
            print("2. За зворотному алфавіті (від Z до A)")
            order_choice = input("Введіть номер порядку: ")
            reverse = order_choice == '2'
            # Використовуємо natsort для природного сортування назв
            self.lessons = natsorted(self.lessons, key=lambda lesson: lesson.title, reverse=reverse)
            print("Уроки відсортовано за назвою.")
        elif choice == '3':
            print("Оберіть порядок сортування за автором:")
            print("1. За алфавітом")
            print("2. За зворотному алфавіті")
            order_choice = input("Введіть номер порядку: ")
            reverse = order_choice == '2'
            self.lessons = natsorted(self.lessons, key=lambda lesson: lesson.author, reverse=reverse)
            print("Уроки відсортовано за автором.")
        else:
            print("Неправильний вибір критерію сортування.")
            return

        self.save_to_file()

    def display_lessons(self):
        if not self.lessons:
            print("Каталог порожній.")
        for lesson in self.lessons:
            print(lesson)

    def load_from_file(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.lessons = [VideoLesson.from_dict(item) for item in data]
            except Exception as e:
                print(f"Помилка завантаження файлу: {e}")
                self.lessons = []
        else:
            self.lessons = []

    def save_to_file(self):
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump([lesson.to_dict() for lesson in self.lessons],
                          f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Помилка збереження файлу: {e}")


class Playlist:
    def __init__(self, name):
        self.name = name
        self.lessons = []

    def find_lesson_index(self, lesson_id):
        for index, lesson in enumerate(self.lessons):
            if lesson.id == lesson_id:
                return index
        return -1

    def add_to_playlist(self, lesson):
        self.lessons.append(lesson)

    def remove_from_playlist(self, lesson_id):
        index = self.find_lesson_index(lesson_id)
        if index != -1:
            del self.lessons[index]
        else:
            print("Неправильний ID уроку в плейлисті.")

    def display_playlist(self):
        print(f"Плейлист: {self.name}")
        if not self.lessons:
            print("В плейлисті нічого немає.")
        for lesson in self.lessons:
            print(lesson)


def main():
    catalog = Catalog()  # Дані завантажуються з файлу "catalog.json"
    # Тестове додавання уроків, якщо файл порожній
    if not catalog.lessons:
        catalog.add_lesson(VideoLesson("Python Basics", "Вступ до Python", "Alice", 45, "Програмування"))
        catalog.add_lesson(VideoLesson("OOP in Python", "Класи та об'єкти", "Bob", 60, "Програмування"))
        catalog.add_lesson(VideoLesson("Advanced Python", "Глибоке занурення", "Charlie", 90, "Програмування"))

    while True:
        print("\n--- Головне меню ---")
        print("1. Показати каталог уроків")
        print("2. Додати новий урок")
        print("3. Редагувати урок")
        print("4. Видалити урок")
        print("5. Фільтрувати уроки")
        print("6. Сортувати уроки")
        print("7. Створити персональний плейлист")
        print("8. Вийти")
        choice = input("Введіть номер вибраної дії: ")

        if choice == '1':
            catalog.display_lessons()

        elif choice == '2':
            title = input("Назва уроку: ")
            description = input("Опис уроку: ")
            author = input("Автор уроку: ")
            try:
                duration = int(input("Тривалість (в хвилинах): "))
            except ValueError:
                duration = 0
            category = input("Категорія уроку: ")
            catalog.add_lesson(VideoLesson(title, description, author, duration, category))

        elif choice == '3':
            lesson_id = input("Введіть ID уроку для редагування: ")
            title = input("Нова назва (залиште порожнім, якщо не змінюється): ")
            description = input("Новий опис (залиште порожнім, якщо не змінюється): ")
            author = input("Новий автор (залиште порожнім, якщо не змінюється): ")
            duration_input = input("Нова тривалість (залиште порожнім, якщо не змінюється): ")
            category = input("Нова категорія (залиште порожнім, якщо не змінюється): ")
            duration = None
            if duration_input.strip() != "":
                try:
                    duration = int(duration_input)
                except ValueError:
                    duration = None
            catalog.edit_lesson(lesson_id,
                                title=title if title.strip() != "" else None,
                                description=description if description.strip() != "" else None,
                                author=author if author.strip() != "" else None,
                                duration=duration,
                                category=category if category.strip() != "" else None)

        elif choice == '4':
            lesson_id = input("Введіть ID уроку для видалення: ")
            catalog.delete_lesson(lesson_id)

        elif choice == '5':
            category = input("Введіть категорію для фільтрації (залиште порожнім для пропуску): ")
            author = input("Введіть автора для фільтрації (залиште порожнім для пропуску): ")
            filtered = catalog.filter_lessons(category=category if category.strip() != "" else None,
                                              author=author if author.strip() != "" else None)
            if not filtered:
                print("За заданими критеріями уроки не знайдені.")
            else:
                for lesson in filtered:
                    print(lesson)

        elif choice == '6':
            catalog.sort_lessons()
            print("\nВідсортований каталог уроків:")
            catalog.display_lessons()

        elif choice == '7':
            playlist_name = input("Введіть назву плейлиста: ")
            playlist = Playlist(playlist_name)
            while True:
                print("\n--- Меню плейлиста ---")
                print("1. Додати урок до плейлиста")
                print("2. Видалити урок з плейлиста")
                print("3. Показати плейлист")
                print("4. Повернутись до головного меню")
                p_choice = input("Введіть номер дії: ")

                if p_choice == '1':
                    catalog.display_lessons()
                    lesson_id = input("Введіть ID уроку для додавання до плейлиста: ")
                    index = catalog.find_lesson_index(lesson_id)
                    if index != -1:
                        playlist.add_to_playlist(catalog.lessons[index])
                    else:
                        print("Неправильний ID уроку.")
                elif p_choice == '2':
                    playlist.display_playlist()
                    lesson_id = input("Введіть ID уроку для видалення з плейлиста: ")
                    playlist.remove_from_playlist(lesson_id)
                elif p_choice == '3':
                    playlist.display_playlist()
                elif p_choice == '4':
                    break
                else:
                    print("Неправильний вибір.")

        elif choice == '8':
            print("Вихід з програми.")
            break

        else:
            print("Неправильний вибір. Спробуйте ще раз.")


if __name__ == "__main__":
    main()
