import plotly.express as px
import plotly.graph_objects as go

def create_gauge(value, title, color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=value, title={'text': title},
        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': color}}
    ))
    fig.update_layout(height=230, margin=dict(l=20,r=20,t=40,b=20), paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
    return fig

def create_donut_chart(df, colors):
    tier_counts = df['Student_Tier'].value_counts().reset_index()
    fig = px.pie(tier_counts, values='count', names='Student_Tier', hole=0.5,
                 title="Student Performance Mix", color='Student_Tier', color_discrete_map=colors)
    fig.update_layout(legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center"))
    return fig