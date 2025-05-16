from flask import Flask
from website import create_app

app = create_app(config_class='website.config.DevelopmentConfig')
if __name__ == '__main__':
    app.run(debug=True)
    
