from datetime import date

class Category:
    """Категория расходов."""

    def __init__(self, name):
        self.name = name


class ExpenseRecord:
    """Запись о расходе."""

    def __init__(self, amount, category, expense_date=None):
        self.amount = amount
        self.category = category
        if not expense_date:
            expense_date = date.today()
        self.expense_date = expense_date

    def to_text(self):
        """Формирование строки для вывода в текстовый файл."""
        return f"{self.expense_date:%Y-%m-%d}: {self.category.name} - {self.amount:.2f}"


class CategoryFactory:
    """Фабрика для создания категорий."""
    _categories = {}

    @classmethod
    def get_category(cls, name):
        if name in cls._categories:
            return cls._categories[name]

        new_category = Category(name)
        cls._categories[name] = new_category
        return new_category


class FinanceTracker:
    """Система учёта финансов."""

    def __init__(self):
        self.records = []

    def add_expense(self, amount, category_name, expense_date=None):
        category = CategoryFactory.get_category(category_name)
        record = ExpenseRecord(amount, category, expense_date)
        self.records.append(record)

    def get_records_by_month(self, year, month):
        records_in_month = [
            r for r in self.records
            if r.expense_date.year == year and r.expense_date.month == month
        ]
        return records_in_month

    def generate_report(self, year, month):
        records = self.get_records_by_month(year, month)
        total_amount = sum(r.amount for r in records)
        categories = {record.category.name: [] for record in records}

        for record in records:
            categories[record.category.name].append(record.to_text())

        report_data = {
            'total': total_amount,
            'categories': categories
        }

        return report_data


class BaseReportGenerator:
    """Базовый класс для генерации отчётов."""

    def format_header(self, total):
        return f"Тotal: {total:.2f}\n\n"

    def format_category(self, category_name, records):
        formatted = f"{category_name}:\n"
        for record in records:
            formatted += f"\t{record}\n"
        return formatted

    def save_to_file(self, data, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(self.format_header(data['total']))

            for category, records in data['categories'].items():
                file.write(self.format_category(category, records))
                file.write("\n")


class DetailedReportGenerator(BaseReportGenerator):
    """Подробный отчёт с дополнительными сведениями."""

    def format_header(self, total):
        return f"Подробный отчёт\n================\nОбщая сумма: {total:.2f}\n\n"

    def format_category(self, category_name, records):
        formatted = f"Категория: {category_name}\n"
        formatted += f"Количество записей: {len(records)}\n"
        for record in records:
            formatted += f"\t{record}\n"
        return formatted


class SimpleReportGenerator(BaseReportGenerator):
    """Простой отчёт без подробностей."""

    def format_header(self, total):
        return f"Простой отчёт\nОбщая сумма: {total:.2f}\n\n"


if __name__ == "__main__":
    # Создание экземпляра трекера
    tracker = FinanceTracker()

    # Добавление расходов
    tracker.add_expense(1000, 'Еда')
    tracker.add_expense(500, 'Транспорт', date(2023, 10, 17))
    tracker.add_expense(2000, 'Развлечения', date(2023, 10, 15))

    # Генерация отчёта за октябрь 2023 года
    report_data = tracker.generate_report(2023, 10)

    # Сохранение подробного отчёта в файл
    detailed_generator = DetailedReportGenerator()
    detailed_generator.save_to_file(report_data, 'detailed_october_2023_report.txt')

    # Сохранение простого отчёта в файл
    simple_generator = SimpleReportGenerator()
    simple_generator.save_to_file(report_data, 'simple_october_2023_report.txt')
