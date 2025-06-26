# addImagesDB.py
# This lets us add images to the db

from website import create_app
from website.models import db, User

# Creating the app instance (same as in main.py)
app = create_app(config_class='config.DevelopmentConfig')

def addProfileImage(user_id, image_path):
    with app.app_context():
        user = db.session.get(User, user_id)
        if not user:
            print(f"User with id {user_id} not found")
            return
                 
        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()
             
            user.profile = image_data
            db.session.commit()
            print(f"Profile image added for user {user.name}")
         
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")

# Adding images here
if __name__ == "__main__":
    addProfileImage(3, 'website/static/images/teachers/janeSmith.png')
    # addProfileImage(1, 'website/static/images/teachers/johnDoe.jpg') 
    addProfileImage(4, 'website/static/images/students/BrianSmith.png')
    #addProfileImage(2, 'website/static/images/students/ellaThompson.png')
