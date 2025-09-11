# VidSights - YouTube Analytics Dashboard
A comprehensive YouTube analytics dashboard that transforms raw video metrics into actionable insights through interactive visualizations and trend analysis.

<img width="1881" height="800" alt="image" src="https://github.com/user-attachments/assets/136f46de-75d8-49e8-9694-916e4cb9b592" />
<img width="1884" height="572" alt="image" src="https://github.com/user-attachments/assets/3cac67f3-4e49-43f8-8db4-83a923292039" />

## 🚀 Features
📊 Interactive Video Metrics: Analyze individual video performance with raw metrics (views, likes, comments) and engagement ratios

📈 Monthly Trends: Track channel performance over time with interactive line charts

💙 Correlation Analysis: Visualize relationships between different engagement metrics through scatter plots and heatmaps

🎯 Real-time Data: Fetch live data directly from YouTube Data API v3

🌙 Modern Dark UI: Professional, card-based design with smooth interactions

## 🛠️ Tech Stack
Backend: Python, Pandas

Frontend: Dash, Plotly

API: YouTube Data API v3

Data Processing: Pandas, NumPy

## 📦 Installation
Clone the repository
bashgit clone https://github.com/yourusername/vidsights.git
cd vidsights

### Install dependencies
bashpip install -r requirements.txt

### Set up YouTube API
Go to Google Cloud Console
Create a new project or select existing one
Enable YouTube Data API v3
Create credentials (API Key)
Replace API_KEY in the script with your key


## Configure Channel
Replace CHANNEL_ID with your target YouTube channel ID

## 🚀 Usage
bashpython app.py
Open your browser and navigate to the host url

## 📊 Dashboard Components

### Video-Specific Metrics
Interactive dropdown to select individual videos
Toggle between raw metrics and engagement ratios
Dynamic bar charts for selected video performance

### Monthly Engagement Trends
Line chart showing views, likes, and comments over time
Automatic aggregation by month
Interactive hover details

### Views vs. Likes Correlation
Scatter plot showing relationship between views and likes
Hover data displays video titles
Identifies high-performing content patterns

### Metric Correlation Heatmap
Correlation matrix between all engagement metrics
Color-coded visualization for easy pattern recognition
Includes engagement ratios analysis

## 🔧 Configuration
API Setup
pythonAPI_KEY = "your_youtube_api_key_here"
CHANNEL_ID = "target_channel_id_here"

## Customization
Modify color schemes in the Plotly templates
Adjust chart dimensions in the layout configuration
Add new metrics by extending the data processing functions

## 📋 Requirements
dash==2.14.1
plotly==5.17.0
pandas==2.0.3
google-api-python-client==2.100.0

## 📈 Future Enhancements
 Multi-channel comparison
 Export functionality for reports
 Subscriber growth tracking
 Revenue analytics integration
 Automated report scheduling
 Mobile responsive design

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
