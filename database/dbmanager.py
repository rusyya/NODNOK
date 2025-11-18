import psycopg2
import os
from datetime import datetime


class DatabaseManager:
    def __init__(self):
        self.connection_params = {
            'dbname': 'gcd_lcm_db',
            'user': 'calculator',
            'password': 'calculator123',
            'host': 'localhost',
            'port': '5432'
        }
        self.init_database()

    def get_connection(self):
        """Создание подключения к базе данных"""
        return psycopg2.connect(**self.connection_params)

    def init_database(self):
        """Инициализация базы данных (таблица уже создана в init.sql)"""
        try:
            conn = self.get_connection()
            conn.close()
            print("Подключение к базе данных установлено")
        except Exception as e:
            print(f"Ошибка подключения к БД: {e}")

    def save_calculation(self, operation_type, value_a, value_b, result):
        """Сохранение расчета в базу данных"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO calculations (operation_type, value_a, value_b, result)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            ''', (operation_type, value_a, value_b, result))
            record_id = cursor.fetchone()[0]
            conn.commit()
            return record_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def get_all_calculations(self):
        """Получение всех расчетов из базы данных"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT id, operation_type, value_a, value_b, result, timestamp
                FROM calculations 
                ORDER BY timestamp DESC
            ''')
            calculations = cursor.fetchall()
            return calculations
        finally:
            cursor.close()
            conn.close()

    def get_calculations_by_type(self, operation_type):
        """Получение расчетов по типу операции"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT id, operation_type, value_a, value_b, result, timestamp
                FROM calculations 
                WHERE operation_type = %s
                ORDER BY timestamp DESC
            ''', (operation_type,))
            calculations = cursor.fetchall()
            return calculations
        finally:
            cursor.close()
            conn.close()

    def clear_all_calculations(self):
        """Очистка всей базы данных"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM calculations')
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def get_statistics(self):
        """Получение статистики по базе данных"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Общее количество записей
            cursor.execute('SELECT COUNT(*) FROM calculations')
            total_count = cursor.fetchone()[0]
            # Количество по типам операций
            cursor.execute('''
                SELECT operation_type, COUNT(*) 
                FROM calculations 
                GROUP BY operation_type
            ''')
            type_stats = cursor.fetchall()
            # Последние 5 записей
            cursor.execute('''
                SELECT operation_type, value_a, value_b, result, timestamp
                FROM calculations 
                ORDER BY timestamp DESC 
                LIMIT 5
            ''')
            recent_calculations = cursor.fetchall()
            return {
                'total_count': total_count,
                'type_stats': type_stats,
                'recent_calculations': recent_calculations
            }
        finally:
            cursor.close()
            conn.close()

    def format_timestamp(self, timestamp):
        """Форматирование timestamp для отображения"""
        if isinstance(timestamp, datetime):
            return timestamp.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(timestamp, str):
            return timestamp.split('.')[0]  # Убираем миллисекунды если есть
        else:
            return str(timestamp)