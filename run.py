from booking.booking import Booking

with Booking(teardown=False) as bot:
    bot.land_first_page()
    bot.change_currency(currency_code="GBP")
    bot.change_language()
    bot.select_place_to_go("Kyiv")
    bot.select_dates(checkin="2025-05-05",
                     checkout="2025-05-10")
    bot.select_adults()
    bot.click_search()
    bot.apply_filtration()
    bot.report_results()

