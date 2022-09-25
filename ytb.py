if __name__ == '__main__':
    from api_ import YTBInfoBot
    bot = YTBInfoBot([])
    print(bot.latest_video_title('https://www.youtube.com/c/mitocw/videos'))
    bot.print_database()
   