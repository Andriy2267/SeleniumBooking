from booking.booking import Booking

with Booking(teardown=False) as bot:
    bot.land_first_page()
    # bot.change_currency(currency_code="PLN")
    bot.select_place_to_go('Kyiv')
    bot.select_dates(checkin='2025-04-29',
                     checkout='2025-05-02')
    bot.select_adults(2)
    bot.click_search()

