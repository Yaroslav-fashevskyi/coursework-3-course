class VideoLesson:
    def __init__(self, title, description, author, duration, category):
        self.title = title
        self.description = description
        self.author = author
        self.duration = duration  # тривалість у хвилинах
        self.category = category

    def __str__(self):
        return f"{self.title} ({self.category}) by {self.author}, Duration: {self.duration} хв."


class Catalog:
    def __init__(self):
        self.lessons = []

    def add_lesson(self, lesson):
        self.lessons.append(lesson)

    def edit_lesson(self, index, title=None, description=None, author=None, duration=None, category=None):
        if 0 <= index < len(self.lessons):
            lesson = self.lessons[index]
            if title is not None:
                lesson.title = title
            if description is not None:
                lesson.description = description
            if author is not None:
                lesson.author = author
            if duration is not None:
                lesson.duration = duration
            if category is not None:
                lesson.category = category
        else:
            print("Невірний індекс уроку для редагування.")

    def delete_lesson(self, index):
        if 0 <= index < len(self.lessons):
            del self.lessons[index]
        else:
            print("Невірний індекс уроку для видалення.")

    def filter_lessons(self, category=None, author=None):
        filtered = self.lessons
        if category:
            filtered = [lesson for lesson in filtered if lesson.category.lower() == category.lower()]
        if author:
            filtered = [lesson for lesson in filtered if lesson.author.lower() == author.lower()]
        return filtered

    def sort_lessons(self, sort_by):
        if sort_by == 'duration':
            self.lessons.sort(key=lambda l: l.duration)
        elif sort_by == 'title':
            self.lessons.sort(key=lambda l: l.title.lower())
        elif sort_by == 'author':
            self.lessons.sort(key=lambda l: l.author.lower())
        else:
            print("Невідоме критеріє сортування. Оберіть 'duration', 'title' або 'author'.")

    def display_lessons(self):
        if not self.lessons:
            print("Каталог порожній.")
        for i, lesson in enumerate(self.lessons):
            print(f"{i}: {lesson}")


class Playlist:
    def __init__(self, name):
        self.name = name
        self.lessons = []

    def add_to_playlist(self, lesson):
        self.lessons.append(lesson)

    def remove_from_playlist(self, index):
        if 0 <= index < len(self.lessons):
            del self.lessons[index]
        else:
            print("Невірний індекс уроку в плейлисті.")

    def display_playlist(self):
        print(f"Плейлист: {self.name}")
        if not self.lessons:
            print("Плейлист порожній.")
        for i, lesson in enumerate(self.lessons):
            print(f"{i}: {lesson}")


def main():
    catalog = Catalog()
    # Додавання тестових уроків
    catalog.add_lesson(VideoLesson("Python Basics", "Вступ до Python", "Alice", 45, "Програмування"))
    catalog.add_lesson(VideoLesson("OOP in Python", "Класи та об'єкти", "Bob", 60, "Програмування"))
    catalog.add_lesson(VideoLesson("Advanced Python", "Глибоке занурення", "Charlie", 90, "Програмування"))

    while True:
        print("--- Головне меню ---")
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
            try:
                index = int(input("Введіть індекс уроку для редагування: "))
            except ValueError:
                print("Невірний індекс.")
                continue
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
            catalog.edit_lesson(index,
                                title=title if title.strip() != "" else None,
                                description=description if description.strip() != "" else None,
                                author=author if author.strip() != "" else None,
                                duration=duration,
                                category=category if category.strip() != "" else None)

        elif choice == '4':
            try:
                index = int(input("Введіть індекс уроку для видалення: "))
            except ValueError:
                print("Невірний індекс.")
                continue
            catalog.delete_lesson(index)

        elif choice == '5':
            category = input("Введіть категорію для фільтрації (залиште порожнім для пропуску): ")
            author = input("Введіть автора для фільтрації (залиште порожнім для пропуску): ")
            filtered = catalog.filter_lessons(category=category if category.strip() != "" else None,
                                              author=author if author.strip() != "" else None)
            if not filtered:
                print("За заданими критеріями уроки не знайдені.")
            else:
                for i, lesson in enumerate(filtered):
                    print(f"{i}: {lesson}")

        elif choice == '6':
            print("Сортувати за: 1. Тривалістю  2. Назвою  3. Автором")
            sort_choice = input("Введіть номер критерію сортування (1/2/3): ")
            if sort_choice == '1':
                catalog.sort_lessons('duration')
            elif sort_choice == '2':
                catalog.sort_lessons('title')
            elif sort_choice == '3':
                catalog.sort_lessons('author')
            else:
                print("Невірний вибір для сортування.")

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
                    try:
                        index = int(input("Введіть індекс уроку для додавання до плейлиста: "))
                    except ValueError:
                        print("Невірний індекс.")
                        continue
                    if 0 <= index < len(catalog.lessons):
                        playlist.add_to_playlist(catalog.lessons[index])
                    else:
                        print("Невірний індекс уроку.")
                elif p_choice == '2':
                    playlist.display_playlist()
                    try:
                        index = int(input("Введіть індекс уроку для видалення з плейлиста: "))
                    except ValueError:
                        print("Невірний індекс.")
                        continue
                    playlist.remove_from_playlist(index)
                elif p_choice == '3':
                    playlist.display_playlist()
                elif p_choice == '4':
                    break
                else:
                    print("Невірний вибір.")

        elif choice == '8':
            print("Вихід з програми.")
            break

        else:
            print("Невірний вибір. Спробуйте ще раз.")


if __name__ == "__main__":
    main()
