from website import create_app

from datetime import date
# from utils.schedule_utils import generate_class_sessions - uncomment when function() is written
from website.models import db, Class

# Initialize the app with the desired configuration
app = create_app(config_class='config.DevelopmentConfig')
'''
some_class = Class.query.get(1)
sessions = generate_class_sessions(some_class.id, date(2025, 9, 1), date(2025, 12, 20), ["Mon 09:00", "Wed 11:00"])
db.session.add_all(sessions)
db.session.commit()
'''
#write query to get calendar after schedule_utils is written

if __name__ == '__main__':
    app.run(debug=True)
