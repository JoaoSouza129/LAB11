import sys
sys.path.insert(0,'/users/a12345/public_html/wsgi')

# if you want to use a virtual environment uncomment the following lines
#activate_this ='/users/a12345/public_html/wsgi/LAB11/.virtualenv/bin/activate_this.py'
#with open(activate_this) as file_:
#    exec(file_.read(), dict(__file__=activate_this))

from LAB11 import app as application
