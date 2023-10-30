from dateparser import parse
from dateparser.search import search_dates

print(parse('Tomorrow'))
print(parse('01/01/20'))
print(search_dates("I will go to the show tomorrow"))
print(search_dates("I'd like to book a table next week Wednesday from 8pm til 9pm"))

