from NewsParser import Parser
from dbInitialize import initialize
if __name__ == '__main__':
    initialize()
    parser = Parser()
    parser.parse("https://www.nur.kz/society/")
    parser.parse("https://scientificrussia.ru/news")
    parser.parse("https://google.com")
    parser.close()
