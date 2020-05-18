from tinydb import TinyDB, Query
from datetime import date, datetime
import activityscreen

user_query = Query()
user_bookings = TinyDB('bookings', indent=2)
user_account = TinyDB('account', indent=2)
user_profile = TinyDB('profile', indent=2)


class User:

    def __init__(self, username):
        self.username = username
        self.bookings = user_bookings.search(user_query.username == self.username)
        self.account = user_account.search(user_query.username == self.username)

    def extract_activity(self, day):
        bookings = self.bookings[0]['activities'][day]
        return bookings

    def book_activity(self, day, activity):
        bookings = self.bookings[0]['activities']
        bookings[day] = activity
        user_bookings.update({'activities': bookings}, user_query.username == self.username)

    def book_meals(self, time, section, meal):
        bookings = self.bookings[0]['meals']
        bookings[activityscreen.ActivityScreenLayout.body.today][time][section] = meal
        user_bookings.update({'meals': bookings}, user_query.username == self.username)

    def extract_meals(self, time):
        bookings = self.bookings[0]['meals'][activityscreen.ActivityScreenLayout.body.today][time]
        bookings_list = []
        for each in bookings:
            bookings_list.append(bookings[each])
        return bookings_list

    def extract_date(self):
        if self.account[0]['start_date']:
            today = datetime.today()
            start_date = datetime.strptime(self.account[0]['start_date'], '%d-%m-%y')
            day_passed = (today - start_date).days
            return day_passed
        else:
            start_date = date.today().strftime('%d-%m-%y')
            user_account.update({'start_date': start_date, 'day': '1'}, user_query.username == self.username)
            return '1'

    def extract_profile(self):
        for each in user_profile.all():
            name = each['name'].split(' ')
            if (name[1] + name[0][0] + str(each['cabin number'])) == self.username:
                user = each
                return user

    def extract_activities(self):
        bookings = self.bookings[0]['activities']
        return list(bookings.values())

    def update_profile(self, info):
        name = self.extract_profile()['name']
        user_profile.update(info, user_query.name == name)

    def register(self):
        pass
