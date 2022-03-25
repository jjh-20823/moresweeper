import json

setting_path = ".\settings.json"

class Options():
    def __init__(self):
        self.opts = {
            "game_style": {
                "mode": 3,
                "height": 16, 
                "width": 30,
                "mines": 99,
                "bfs": False, 
                "ez_flag": False, 
                "nf": False
            }
        }

    def reload(self):
        with open(setting_path, "r") as load_f:
            self.opts = json.load(load_f)

    def save(self):
        with open(setting_path, "w") as write_f:
            json.dump(self.opts, write_f, indent=4, sort_keys=True, ensure_ascii=False)
