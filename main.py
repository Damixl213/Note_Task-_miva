# Main entry point for Flask Note-Taking Application
from Note_website import create_app

# Create Flask app instance
app = create_app()

# Run app in development mode
if __name__== '__main__':
  app.run(debug=True)