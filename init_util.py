import util
import setting as s
def initUtil(app):
    app.setting = s.Setting()
    app.settings = app.setting.get_settings()

    if 'darkmode' in app.settings.keys():
        app.dark_mode = app.settings["darkmode"]
    else:
        app.dark_mode = False

    app.news_list = []
    app.schedule_list = []
