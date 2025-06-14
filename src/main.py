
from database.db_config import *
from controller.Controller import Controller
import json
conn = connect()
controller = Controller(conn)
pattern = "technical"
text = "aaaaaaaaa"

# print(controller.searchhh(pattern, text))
a = controller.searchQuery("accounting")

print(a)