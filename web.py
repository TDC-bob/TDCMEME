#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      owner
#
# Created:     28/05/2013
# Copyright:   (c) owner 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from _logging._logging import mkLogger
logger = mkLogger(__name__)

import cherrypy
class HelloWorld():
    def index(self):
        return "Hello Caribou!"
    index.exposed = True

def http_error_401_hander(status, message, traceback, version):
    """ Custom handler for 401 error """
    if status != "401 Unauthorized":
        logger.log(u"CherryPy caught an error: %s %s" % (status, message), logger.ERROR)
        logger.log(traceback, logger.DEBUG)
    return r'''
<html>
<head>
<title>%s</title>
</head>
<body>
<br/>
<font color="#0000FF">Error %s: You need to provide a valid username and password.</font>
</body>
</html>
''' % ('Access denied', status)

def http_error_404_hander(status, message, traceback, version):
    """ Custom handler for 404 error, redirect back to main page """
    return r'''
<html>
<head>
<title>404</title>
<script type="text/javascript" charset="utf-8">
<!--
location.href = "%s"
//-->
</script>
</head>
<body>
<br/>
</body>
</html>
''' % '/'

def main():
    options_dict = {
                    'server.socket_port': 8081,
                    'server.socket_host': '0.0.0.0',
                    'log.screen': False,
                    'error_page.401': http_error_401_hander,
                    'error_page.404': http_error_404_hander,
    }
    cherrypy.config.update(options_dict)
    app = cherrypy.tree.mount(HelloWorld(), "/")#, conf)
    cherrypy.server.start()
    cherrypy.server.wait()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
