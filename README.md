# LAB11 skeleton

### Compiles and hot-reloads for development
```
python -m flask --app LAB11 run --debug --host=0.0.0.0
```

### Open project in browser at URL
```
http://josebastos.eu:5000
```

### Compiles and minifies for production

Change '12345' with your student number:

```
nano app.wsgi

import sys
sys.path.insert(0,'/users/a12345/public_html/wsgi')

from LAB11 import app as application
```

### Open project in browser at URL
```
http://josebastos.eu/~a12345/wsgi/LAB11/app.wsgi
```


