class Constants():

    @staticmethod
    def get_excluded_paths():
        return [
            "/health",
            "/inscription/token/{user_uid}",
            "/docs",
            "/docs/oauth2-redirect",
            "/openapi.json",
            "/redoc",
            "/inscription/token",
            "/swagger-ui.css",
            "/swagger-ui-bundle.js",
            "/.well-known/acme-challenge/",
            "/swagger-ui-standalone-preset.js",
            "/scan/"
        ]