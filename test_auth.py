import cherrypy
from auth import AuthController, require, member_of, name_is

class RestrictedArea:

    # all methods in this controller (and subcontrollers) is
    # open only to members of the admin group

    _cp_config = {
        'auth.require': [member_of('admin')]
    }

    @cherrypy.expose
    def index(self):
        return """This is the admin only area."""


class Root:

    _cp_config = {
        'tools.sessions.on': True,
        'tools.auth.on': True
    }

    auth = AuthController()

    restricted = RestrictedArea()

    @cherrypy.expose
    @require()
    def index(self):
        return """This page only requires a valid login."""

    @cherrypy.expose
    def open(self):
        return """This page is open to everyone"""

    @cherrypy.expose
    @require(name_is("joe"))
    def only_for_joe(self):
        return """Hello Joe - this page is available to you only"""

    # This is only available if the user name is joe _and_ he's in group admin
    @cherrypy.expose
    @require(name_is("joe"))
    @require(member_of("admin"))   # equivalent: @require(name_is("joe"), member_of("admin"))
    def only_for_joe_admin(self):
        return """Hello Joe Admin - this page is available to you only"""


def main():
    options_dict = {
                    'server.socket_port': 8082,
                    'server.socket_host': '0.0.0.0',
                    'log.screen': False,
##                    'error_page.401': http_error_401_hander,
##                    'error_page.404': http_error_404_hander,
    }
    cherrypy.config.update(options_dict)
    app = cherrypy.tree.mount(Root(), "/")#, conf)
    # monkey patch
    def fake_wait_for_occupied_port(host, port): return
    cherrypy.process.servers.wait_for_occupied_port = fake_wait_for_occupied_port
    cherrypy.server.start()
    cherrypy.server.wait()
##    cherrypy.quickstart(Root())

if __name__ == '__main__':
    try:
        main()
        while True:
            pass
        print("finished main()")
    except KeyboardInterrupt:
        cherrypy.server.stop()
        print("finished main()")
        pass