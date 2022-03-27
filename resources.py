from PyQt5.QtGui import QPixmap

resource_path = "./resources/{}/{}.svg"
items = ["celldown"] + ["cell" + str(i) for i in range(1, 9)] + ["cellup", "celldown", "cellflag", "cellunflagged", "falsemine", "blast", "cellmine"]

def get_skin(skin, size):
    return [QPixmap(resource_path.format(skin, item)).scaled(size, size) for item in items]