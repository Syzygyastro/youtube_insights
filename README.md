
# YouTube Insights    
  <img src=https://github.com/user-attachments/assets/a8c4d640-d90e-41bc-8621-0a2e8bf22f41 width=70>    
  <img src=https://github.com/user-attachments/assets/e8f6ad5a-c56a-4b3a-aa00-938280a1ddff width=70>

YouTube Insights is a web application that provides users with an analysis of their YouTube subscriptions, categorizing them into various content types such as Music, Gaming, News, and others. Built with Flask, the app integrates with the YouTube Data API to fetch user subscription data and offers a dashboard for visualizing the analysis.

## Features

- **User Authentication:** Secure OAuth2-based authentication to access user subscription data.
- **Subscription Analysis:** Categorizes user subscriptions into predefined categories based on channel titles.
- **Dashboard:** Displays the analysis results in a user-friendly interface.

## Technologies Used

- **Backend:** Python, Flask
- **Frontend:** HTML
- **APIs:** YouTube Data API

## Setup Instructions

# 1. Clone the Repository
git clone https://github.com/Syzygyastro/youtube_insights.git

# 2. Navigate to the Backend Directory
cd youtube_insights/backend

# 3. Install Dependencies
pip install -r requirements.txt

# 4. Set Up Environment Variables
# Create a .env file in the backend directory with the following variables:
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
YOUTUBE_API_KEY=your_youtube_api_key

# 5. Run the Application
flask run

# 6. Access the Application
# Open your browser and navigate to http://localhost:5000 to use the app.
