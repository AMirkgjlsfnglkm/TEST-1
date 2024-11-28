
    # مقداردهی اولیه ویژگی‌های کتاب
    def __init__(self, title, author, publication_year):
        self.title = title  # عنوان کتاب
        self.author = author  # نویسنده کتاب
        self.publication_year = publication_year  # سال انتشار کتاب
        self.is_available = True  # وضعیت دسترسی کتاب (در دسترس یا قرض داده شده)

    # تبدیل شیء کتاب به دیکشنری برای ذخیره در فایل JSON
    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "publication_year": self.publication_year,
            "is_available": self.is_available
        }

    # ایجاد شیء کتاب از داده‌های دیکشنری (بارگذاری از فایل JSON)
    @staticmethod
    def from_dict(data):
        book = Book(data["title"], data["author"], data["publication_year"])
        book.is_available = data["is_available"]
        return book

    # تعریف نحوه نمایش کتاب برای چاپ
    def __str__(self):
        status = "Available" if self.is_available else "Borrowed"
        return f"{self.title} by {self.author} ({self.publication_year}) - {status}"


# تعریف کلاس پایه اعضای کتابخانه
class Member:
    # مقداردهی اولیه ویژگی‌های عضو
    def __init__(self, member_id, name, borrow_limit):
        self.member_id = member_id  # شناسه منحصر به فرد عضو
        self.name = name  # نام عضو
        self.borrowed_books = []  # لیست کتاب‌های قرض گرفته شده توسط عضو
        self.borrow_limit = borrow_limit  # محدودیت تعداد کتاب‌های قابل قرض

    # تبدیل شیء عضو به دیکشنری برای ذخیره در فایل JSON
    def to_dict(self):
        return {
            "member_id": self.member_id,
            "name": self.name,
            "borrowed_books": self.borrowed_books,
            "borrow_limit": self.borrow_limit
        }

    # ایجاد شیء عضو از داده‌های دیکشنری (بارگذاری از فایل JSON)
    @staticmethod
    def from_dict(data):
        if data["borrow_limit"] == 5:  # اگر محدودیت ۵ باشد، عضو دانشجو است
            member = Student(data["member_id"], data["name"])
        else:  # در غیر این صورت، عضو استاد است
            member = Professor(data["member_id"], data["name"])
        member.borrowed_books = data["borrowed_books"]
        return member

    # تعریف نحوه نمایش عضو برای چاپ
    def __str__(self):
        return f"{self.name} (ID: {self.member_id}) - Borrowed books: {len(self.borrowed_books)}"


# تعریف کلاس دانشجو (ارث‌بری از Member)
class Student(Member):
    def __init__(self, member_id, name):
        super().__init__(member_id, name, borrow_limit=5)  # محدودیت قرض ۵ کتاب


# تعریف کلاس استاد (ارث‌بری از Member)
class Professor(Member):
    def __init__(self, member_id, name):
        super().__init__(member_id, name, borrow_limit=10)  # محدودیت قرض ۱۰ کتاب


# دیکشنری برای نگهداری کتاب‌ها و اعضا
books = {}  # کلید: عنوان کتاب
members = {}  # کلید: شناسه عضو


# بارگذاری داده‌ها از فایل JSON
def load_data():
    global books, members
    try:
        with open("library_data.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            books = {title: Book.from_dict(b) for title, b in data["books"].items()}
            members = {id: Member.from_dict(m) for id, m in data["members"].items()}
    except FileNotFoundError:  # اگر فایل پیدا نشد، دیکشنری‌ها خالی می‌شوند
        books = {}
        members = {}
    except Exception as e:  # مدیریت خطاهای دیگر
        print(f"Error loading data: {e}")


# ذخیره داده‌ها در فایل JSON
def save_data():
    try:
        data = {
            "books": {title: b.to_dict() for title, b in books.items()},
            "members": {id: m.to_dict() for id, m in members.items()}
        }
        with open("library_data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print("Data saved successfully!")  # پیام موفقیت ذخیره
    except Exception as e:  # مدیریت خطا در ذخیره‌سازی
        print(f"Error saving data: {e}")


# پاک کردن کنسول
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')  # پاک کردن کنسول برای ویندوز و لینوکس


# اضافه کردن کتاب به کتابخانه
def add_book():
    clear_console()
    title = input("Enter book title: ")  # دریافت عنوان کتاب
    author = input("Enter book author: ")  # دریافت نویسنده
    year = int(input("Enter publication year: "))  # دریافت سال انتشار
    book = Book(title, author, year)  # ایجاد شیء کتاب
    books[title] = book  # افزودن کتاب به دیکشنری
    print(f"Book '{title}' added successfully!")
    save_data()  # ذخیره تغییرات


# اضافه کردن عضو (دانشجو یا استاد)
def add_member(member_type):
    clear_console()
    member_id = input("Enter member ID: ")  # شناسه عضو
    name = input("Enter member name: ")  # نام عضو
    if member_type == "student":
        member = Student(member_id, name)  # ایجاد دانشجو
    else:
        member = Professor(member_id, name)  # ایجاد استاد
    members[member_id] = member  # افزودن عضو به دیکشنری
    print(f"{'Student' if member_type == 'student' else 'Professor'} '{name}' added successfully!")
    save_data()  # ذخیره تغییرات


# قرض گرفتن کتاب
def borrow_book():
    clear_console()
    member_id = input("Enter member ID: ")  # شناسه عضو
    book_title = input("Enter book title: ")  # عنوان کتاب
    if member_id in members and book_title in books:  # بررسی وجود عضو و کتاب
        member = members[member_id]
        book = books[book_title]
        if not book.is_available:
            print(f"Sorry, the book '{book_title}' is already borrowed.")  # کتاب قبلاً قرض داده شده
        elif len(member.borrowed_books) >= member.borrow_limit:
            print(f"{member.name} has reached the borrow limit.")  # عضو به محدودیت قرض رسیده
        else:
            book.is_available = False  # تغییر وضعیت کتاب به "قرض داده شده"
            member.borrowed_books.append(book.title)  # افزودن کتاب به لیست عضو
            print(f"Book '{book_title}' has been borrowed by {member.name}.")
    else:
        print("Member or book not found.")  # اگر عضو یا کتاب پیدا نشود
    save_data()  # ذخیره تغییرات


# بازگرداندن کتاب
def return_book():
    clear_console()
    member_id = input("Enter member ID: ")  # شناسه عضو
    book_title = input("Enter book title: ")  # عنوان کتاب
    if member_id in members and book_title in books:  # بررسی وجود عضو و کتاب
        member = members[member_id]
        book = books[book_title]
        if book.title in member.borrowed_books:  # بررسی اینکه کتاب قرض گرفته شده است
            book.is_available = True  # تغییر وضعیت کتاب به "در دسترس"
            member.borrowed_books.remove(book.title)  # حذف کتاب از لیست عضو
            print(f"Book '{book_title}' has been returned by {member.name}.")
        else:
            print(f"{member.name} has not borrowed '{book_title}'.")  # اگر کتاب در لیست عضو نباشد
    else:
        print("Member or book not found.")  # اگر عضو یا کتاب پیدا نشود
    save_data()  # ذخیره تغییرات


# نمایش لیست کتاب‌ها
def show_books():
    clear_console()
    if books:  # بررسی وجود کتاب‌ها
        print("List of books:\n")
        for book in books.values():
            print(book)  # چاپ اطلاعات کتاب
    else:
        print("No books available in the library.")  # پیام در صورت نبود کتاب
    input("\nPress Enter to return to the menu...")  # منتظر ماندن برای بازگشت به منو


# منوی اصلی برنامه
def main_menu():
    load_data()  # بارگذاری داده‌ها
    while True:
        clear_console()
        print("Library Management System")
        print("1. Add Book")
        print("2. Add Student")
        print("3. Add Professor")
        print("4. Borrow Book")
        print("5. Return Book")
        print("6. Show Books")
        print("7. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            add_book()
        elif choice == "2":
            add_member("student")
        elif choice == "3":
            add_member("professor")
        elif choice == "4":
            borrow_book()
        elif choice == "5":
            return_book()
        elif choice == "6":
            show_books()
        elif choice == "7":
            save_data()
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")  # مدیریت انتخاب نامعتبر


# اجرای برنامه
if __name__ == "__main__":
    main_menu()
