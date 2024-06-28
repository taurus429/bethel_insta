import util
import setting as s
def initUtil(app):
    app.setting = s.Setting()

    darkmode = app.setting.get_settings("darkmode")
    if darkmode:
        app.dark_mode = True
    else:
        app.dark_mode = False

    app.news_list = []
    app.schedule_list = []
    app.birthday_list = []