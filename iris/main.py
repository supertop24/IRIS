from website import create_app

from datetime import date
from website.models import db, Class

# Initialize the app with the desired configuration
app = create_app(config_class='config.DevelopmentConfig')

if __name__ == '__main__':
    app.run(debug=True)

