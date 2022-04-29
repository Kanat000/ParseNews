from dbConnection import Sqlite
from config import dbName


def initialize():
    db = Sqlite(dbName)
    db.create_resource_table()
    db.create_items_table()
    if not db.exists_resource('https://www.nur.kz/society/'):
        db.insert_resource('Nur', 'https://www.nur.kz/society/', 'a|class|article-preview-mixed--secondary',
                           'p|class|formatted-body__paragraph', 'h1|class|main-headline',
                           'time|class|datetime--publication')

    if not db.exists_resource('https://scientificrussia.ru/news'):
        db.insert_resource('ScientificRussia', 'https://scientificrussia.ru/news',
                           'div|class|wrapper&div|class|image&a|class|',
                           'p|style|text-align: justify;', 'h1|itemprop|name headline',
                           'div|class|col-12 col-lg-8&div|class|props&div|class|prop&time|class|')
