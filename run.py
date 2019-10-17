from sys import exit
from facebook import Facebook

try:
    facebook = Facebook("xoceanfirex@gmail.com", "Etq~CE(?(c7:T.<uaKY0z^YV}s=g,Deh", headless_mode=False)
    facebook.login()
    facebook.go_to_group("https://www.facebook.com/groups/BudowaMazowieckie/")
except KeyboardInterrupt:
    exit()
except Exception as e:
    print("Exceprion on run: " + str(e))
finally:
    pass
