import telebot
import datetime
import schedule
import time
import csv


TOKEN = ''
bot = telebot.TeleBot(TOKEN)


def get_day():
    today = str(datetime.date.today()).split('-', 3)
    day = today[2]
    month = today[1]
    year = today[0]
    date = f'{day}-{month}-{year}'
    return date


csvfile = 'mikitracking.csv'
HEADERS = ['Day', 'Water', 'Shower', 'Walk', 'test']
first_day = get_day()
temporary_list = [first_day, 0, 0, 0, 0]


def handle_shower():
    temporary_list[2] = 0


def handle_walk():
    temporary_list[3] = 0


def list_to_dict(List: list) -> dict:
    dictionary = {}
    for item in List:
        dictionary[HEADERS[List.index(item)]] = item
    return dictionary


def append_row(row: list, newline="") -> None:
    with open(csvfile, 'a', newline=newline) as year_csv:
        year_writer = csv.DictWriter(year_csv, HEADERS)
        year_writer.writerow(list_to_dict(row))


def new_day():
    global temporary_list
    print(f'{temporary_list} before')
    append_row(temporary_list)
    temporary_list[0] = get_day()
    temporary_list[1] = 0
    temporary_list[2] += 1
    temporary_list[3] += 1
    print(f'{temporary_list} after')


def read_last_row():
    with open(csvfile, "r") as scraped:
        return scraped.readlines()[-1]


def translate_liters(message):
    quantity = message.text.split(' ', 2)[1]
    numbers = int(''.join(filter(str.isdigit, quantity)))
    letters = ''
    for i in quantity:
        try:
            int(i)
        except ValueError:
            letters += i
    if letters == 'l':
        numbers *= 1000
    elif letters == 'ml':
        pass
    return numbers


@bot.message_handler(commands=['drink'])
def handle_liters(message):
    # translate message into mililiters
    quantity = message.text.split(' ', 2)[1]
    numbers = int(''.join(filter(str.isdigit, quantity)))
    letters = ''
    for i in quantity:
        try:
            int(i)
        except ValueError:
            letters += i
    if letters == 'l':
        numbers *= 1000
    elif letters == 'ml':
        pass
    # add to csv
    temporary_list[1] += numbers
    # send confirmation in chat
    bot.send_message(message.chat.id, f'{numbers} ml added to your daily consumption, {temporary_list[1]} ml already!')


@bot.message_handler(commands=['shower'])
def handle_shower(message):
    temporary_list[2] = 0
    bot.send_message(message.chat.id, f'{temporary_list} test')


@bot.message_handler(commands=['walk'])
def handle_walk(message):
    temporary_list[3] = 0
    bot.send_message(message.chat.id, f'{temporary_list} test')


@bot.message_handler(commands=['new'])
def new(message):
    send()
    new_day()

def send():
    bot.send_message(138077070, 'hi')


def main():
    bot.polling()


if __name__ == '__main__':
    main()
