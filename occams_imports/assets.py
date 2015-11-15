import os

from webassets import Bundle

from . import log


def includeme(config):
    """
    Loads web assets
    """
    here = os.path.dirname(os.path.realpath(__file__))

    env = config.get_webassets_env()
    env.append_path(os.path.join(here, 'static'), '/imports/static')

    # "resolves" the path relative to this package
    def rel(path):
        return os.path.join(here, 'static', path)

    scriptsdir = os.path.join(here, 'static/scripts')

    config.add_webasset('imports-js', Bundle(
        # Dependency javascript libraries must be loaded in a specific order
        rel('bower_components/jquery/jquery.min.js'),
        rel('bower_components/jquery-ui/jquery-ui.min.js'),
        Bundle(rel('bower_components/jquery-cookie/jquery.cookie.js'), filters='jsmin'),
        rel('bower_components/jquery-validate/dist/jquery.validate.min.js'),
        rel('bower_components/bootstrap/dist/js/bootstrap.min.js'),
        rel('bower_components/knockout/dist/knockout.js'),
        rel('bower_components/knockout-sortable/build/knockout-sortable.min.js'),
        rel('bower_components/select2/select2.min.js'),
        rel('bower_components/moment/min/moment.min.js'),
        rel('bower_components/eonasdan-bootstrap-datetimepicker/build/js/bootstrap-datetimepicker.min.js'),
        rel('bower_components/lodash/lodash.js'),
        rel('bower_components/backbone/backbone.js'),
        rel('bower_components/jointjs/dist/joint.js'),
        # App-specific scripts can be loaded in any order
        Bundle(
            *[os.path.join(root, filename)
                for root, dirnames, filenames in os.walk(scriptsdir)
                for filename in filenames if filename.endswith('.js')],
            filters='jsmin'),
        output=rel('gen/imports.%(version)s.js')))

    config.add_webasset('imports-css', Bundle(
        Bundle(
            rel('styles/main.less'),
            filters='less,cssmin',
            depends=rel('styles/*.less'),
            output=rel('gen/limis-main.%(version)s.css')),
        Bundle(rel('bower_components/select2/select2.css'), filters='cssrewrite'),
        rel('bower_components/select2-bootstrap-css/select2-bootstrap.css'),
        rel('bower_components/jointjs/joint.css'),
       # rel('styles/demo.css')
        output=rel('gen/imports.%(version)s.css')))

    log.debug('Assets configurated')
