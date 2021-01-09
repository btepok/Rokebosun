import OsuApi
import telebot
import configparser
import configwrite

bot = telebot.TeleBot('<token>')


@bot.message_handler(commands=['start'])
def start_reg(message):
    if configwrite.is_exist(message.chat.id):
        bot.send_message(message.chat.id, "Ты дэб или перерешать акк хочешь?")

    else:
        config = configparser.ConfigParser()
        bot.send_message(message.chat.id, "Даров")

        config.add_section("User")
        config.set("User", "telegram_id", str(message.chat.id))

        bot.send_message(message.chat.id, "Напиши ник осу акка")
        bot.register_next_step_handler(message, user_name, config)


def user_name(message, config):
    username = message.text
    try:
        data = OsuApi.account_data(username)
        osu_user_id = data["id"]

        name = data["username"]
        pp = int(data["statistics"]["pp"])
        play_count = data["statistics"]["play_count"]
        rank = data["statistics"]["pp_rank"]

        bot.send_message(message.chat.id, f"{name}, нафармил {pp}pp за {play_count} игр. Ранк #{rank}")

        config.set("User", "Username", username)
        config.set("User", "osu_id", str(osu_user_id))

        with open(f"users/{message.chat.id}.ini", "w") as user_file:
            config.write(user_file)

        bot.send_message(message.chat.id, "Записал")

    except Exception as e:
        bot.send_message(message.chat.id, f"Неправильно {e}")
        print(e)


@bot.message_handler(commands=['user'])
def start_reg(message):
    try:
        user = str(message.text.split()[1])
        bot.send_message(message.chat.id, OsuApi.short_info(user, "old_user"))
    except Exception as e:
        bot.send_message(message.chat.id, f"Не понял {e}")


@bot.message_handler(commands=['me'])
def start_reg(message):
    config = configparser.ConfigParser()
    config.read(f"users/{message.chat.id}.ini")
    username = config.get("User", "osu_id")
    bot.send_message(message.chat.id, OsuApi.short_info(username, "old_user"))


@bot.message_handler(commands=['best'])
def start_reg(message):
    user = str(message.text.split()[1])
    req = OsuApi.account_data(user)
    user_id = req["id"]
    data = OsuApi.best_scores(user_id)

    for i in range(len(data)):
        bot.send_message(message.chat.id, data[i]["beatmap"]["url"])


@bot.message_handler(commands=['rc'])
def start_reg(message):
    try:
        account = configparser.ConfigParser()
        account.read(f"users/{message.from_user.id}.ini")
        user_id = str(account.get("User", "osu_id"))

        data = OsuApi.recent_scores(user_id)
        print(data)

        for i in range(len(data)):
            url = data[i]["beatmap"]["url"]
            title = data[i]["beatmapset"]["title"]
            artist = data[i]["beatmapset"]["artist"]
            maper = data[i]["beatmapset"]["creator"]

            print(data[i]["perfect"])

            if (data[i]["accuracy"]) == 1:
                fc = "SSнул"

            elif data[i]["perfect"]:
                fc = "Фкшнул"

            else:
                fc = "Пасснул"

            print(artist)
            print(title)
            bot.send_message(message.chat.id, f"{fc} мапу <a href='{url}'>{artist}: {title}</a> от {maper}",
                             parse_mode='HTML', disable_web_page_preview=True)

    except Exception as e:
        bot.send_message(message.chat.id, "Зарегайся сначала")
        print(e)


bot.polling(none_stop=True)
