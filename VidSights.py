import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from googleapiclient.discovery import build
import plotly.graph_objects as go
import plotly.io as pio
import datetime

pio.templates.default = "plotly_dark"


API_KEY = "YOUR_API_KEY"
CHANNEL_ID = "YOUR_CHANNEL_ID"
youtube = build('youtube', 'v3', developerKey=API_KEY)


def get_channel_videos(channel_id):
    video_list = []
    next_page_token = None
    while True:
        request = youtube.search().list(
            part="id,snippet",
            channelId=channel_id,
            maxResults=50,
            order="date",
            type="video",
            pageToken=next_page_token
        )
        response = request.execute()
        for item in response['items']:
            video_list.append({
                'Video_ID': item['id']['videoId'],
                'Title': item['snippet']['title'],
                'Published_Date': pd.to_datetime(item['snippet']['publishedAt'])
            })
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
    return pd.DataFrame(video_list)


def get_video_stats(video_ids):
    stats_list = []
    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part="statistics,contentDetails",
            id=",".join(video_ids[i:i+50])
        )
        response = request.execute()
        for item in response['items']:
            stats_list.append({
                'Video_ID': item['id'],
                'Views': int(item['statistics'].get('viewCount', 0)),
                'Likes': int(item['statistics'].get('likeCount', 0)),
                'Comments': int(item['statistics'].get('commentCount', 0)),
                'Duration': item['contentDetails']['duration']
            })
    return pd.DataFrame(stats_list)

videos_df = get_channel_videos(CHANNEL_ID)
stats_df = get_video_stats(videos_df['Video_ID'].tolist())
data = pd.merge(videos_df, stats_df, on='Video_ID')
data['Like_Ratio'] = data['Likes'] / data['Views']
data['Comment_Ratio'] = data['Comments'] / data['Views']

monthly_data = data.groupby(data['Published_Date'].dt.tz_localize(None).dt.to_period('M'))[['Views', 'Likes', 'Comments']].sum().reset_index()
monthly_data['Published_Date'] = monthly_data['Published_Date'].astype(str)

monthly_trends_fig = go.Figure(
    data=[
        go.Scatter(x=monthly_data['Published_Date'], y=monthly_data['Views'], mode='lines+markers', name='Views'),
        go.Scatter(x=monthly_data['Published_Date'], y=monthly_data['Likes'], mode='lines+markers', name='Likes'),
        go.Scatter(x=monthly_data['Published_Date'], y=monthly_data['Comments'], mode='lines+markers', name='Comments')
    ],
    layout=go.Layout(
        title='Monthly Engagement Trends',
        xaxis_title='Month',
        yaxis_title='Count',
        template='plotly_dark',
        height=400,  
        autosize=False  
    )
)

views_likes_fig = px.scatter(
    data,
    x='Views',
    y='Likes',
    hover_data=['Title'],
    title='Views vs. Likes'
)
views_likes_fig.update_layout(height=400, autosize=False)  

corr_df = data[['Views', 'Likes', 'Comments', 'Like_Ratio', 'Comment_Ratio']].corr()
correlation_heatmap_fig = px.imshow(
    corr_df,
    text_auto=True,
    color_continuous_scale='Viridis',
    title='Engagement Metrics Correlation'
)
correlation_heatmap_fig.update_layout(height=400, autosize=False)  

app = dash.Dash(__name__)

app.layout = html.Div(
    style={
        'backgroundColor': '#1E1E1E', 
        'color': 'white', 
        'fontFamily': 'Arial, sans-serif',
        'minHeight': '100vh',  
        'overflow': 'auto'     
    }, 
    children=[
        html.H1(
            children=[
                html.Span('VidSights', style={'color': '#FF0000'}),
                html.Span(' - YouTube Analytics Dashboard', style={'color': 'white'})
            ], 
            style={'textAlign': 'center', 'paddingTop': '20px'}
        ),
        html.Hr(style={'borderTop': '2px solid #FF0000'}),
        
        html.Div(
            className="row", 
            style={
                'display': 'flex', 
                'padding': '20px',
                'minHeight': '450px',  
                'maxHeight': '500px'  
            }, 
            children=[
                html.Div(
                    className="six columns", 
                    style={
                        'width': '50%', 
                        'paddingRight': '10px',
                        'height': '450px' 
                    }, 
                    children=[
                        html.H3('Video-Specific Metrics', style={'textAlign': 'center'}),
                        dcc.Dropdown(
                            id='video-dropdown',
                            options=[{'label': title, 'value': title} for title in data['Title'].unique()],
                            value=data['Title'].unique()[0],
                            style={'color': 'black', 'marginTop': '10px'}
                        ),
                        dcc.Dropdown(
                            id='metric-type-dropdown',
                            options=[
                                {'label': 'Raw Metrics (Views, Likes, Comments)', 'value': 'raw'},
                                {'label': 'Engagement Ratios (Like Ratio, Comment Ratio)', 'value': 'ratios'}
                            ],
                            value='raw',
                            style={'color': 'black', 'marginTop': '10px'}
                        ),
                        dcc.Graph(
                            id='engagement-graph',
                            style={
                                'marginTop': '20px',
                                'height': '350px'  
                            }
                        ),
                    ]
                ),
                
                html.Div(
                    className="six columns", 
                    style={
                        'width': '50%', 
                        'paddingLeft': '10px',
                        'height': '450px' 
                    }, 
                    children=[
                        html.H3('Monthly Engagement Trends', style={'textAlign': 'center'}),
                        dcc.Graph(
                            id='monthly-trends-graph',
                            style={
                                'marginTop': '20px',
                                'height': '400px' 
                            },
                            figure=monthly_trends_fig,
                            config={'responsive': False} 
                        ),
                    ]
                ),
            ]
        ),
        
        html.Div(
            className="row", 
            style={
                'display': 'flex', 
                'padding': '20px',
                'minHeight': '450px', 
                'maxHeight': '500px'   
            }, 
            children=[
                html.Div(
                    className="six columns", 
                    style={
                        'width': '50%', 
                        'paddingRight': '10px',
                        'height': '450px'  
                    }, 
                    children=[
                        html.H3('Views vs. Likes', style={'textAlign': 'center'}),
                        dcc.Graph(
                            id='views-likes-graph',
                            style={
                                'marginTop': '20px',
                                'height': '400px'
                            },
                            figure=views_likes_fig,
                            config={'responsive': False} 
                        ),
                    ]
                ),
                html.Div(
                    className="six columns", 
                    style={
                        'width': '50%', 
                        'paddingLeft': '10px',
                        'height': '450px'  
                    }, 
                    children=[
                        html.H3('Metric Correlation', style={'textAlign': 'center'}),
                        dcc.Graph(
                            id='correlation-heatmap',
                            style={
                                'marginTop': '20px',
                                'height': '400px' 
                            },
                            figure=correlation_heatmap_fig,
                            config={'responsive': False}  
                        ),
                    ]
                ),
            ]
        ),
    ]
)

@app.callback(
    Output('engagement-graph', 'figure'),
    [Input('video-dropdown', 'value'),
     Input('metric-type-dropdown', 'value')]
)
def update_graph(selected_title, selected_type):
    filtered_df = data[data['Title'] == selected_title].iloc[0]
    
    if selected_type == 'raw':
        metrics_df = pd.DataFrame({
            'Metric': ['Views', 'Likes', 'Comments'],
            'Value': [filtered_df['Views'], filtered_df['Likes'], filtered_df['Comments']]
        })
        fig = px.bar(
            metrics_df,
            x='Metric',
            y='Value',
            title=f'Raw Metrics for "{selected_title}"'
        )
    else:
        metrics_df = pd.DataFrame({
            'Metric': ['Like Ratio', 'Comment Ratio'],
            'Value': [filtered_df['Like_Ratio'], filtered_df['Comment_Ratio']]
        })
        fig = px.bar(
            metrics_df,
            x='Metric',
            y='Value',
            title=f'Engagement Ratios for "{selected_title}"'
        )
    

    fig.update_layout(
        height=350, 
        autosize=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        title_font=dict(size=16, color='white'),
        margin=dict(t=50, b=50, l=50, r=50)
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)
