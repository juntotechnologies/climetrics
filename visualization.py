import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def create_los_comparison(df, service, current_surgeon):
    """Create length of stay comparison plot."""
    service_data = df[df['service'] == service]

    # Calculate detailed statistics for each surgeon
    los_by_surgeon = []
    for surgeon in service_data['surgeon'].unique():
        surgeon_data = service_data[service_data['surgeon'] == surgeon]
        los_by_surgeon.append({
            'surgeon': surgeon,
            'avg_los': surgeon_data['length_of_stay'].mean(),
            'min_los': surgeon_data['length_of_stay'].min(),
            'max_los': surgeon_data['length_of_stay'].max(),
            'total_cases': len(surgeon_data)
        })

    los_df = pd.DataFrame(los_by_surgeon)

    # Calculate overall service mean
    overall_mean = service_data['length_of_stay'].mean()

    fig = go.Figure()

    # Add bar chart with custom hover template
    fig.add_trace(go.Bar(
        x=los_df['surgeon'],
        y=los_df['avg_los'],
        marker_color=[
            '#0066cc' if surgeon == current_surgeon else '#B3B3B3'
            for surgeon in los_df['surgeon']
        ],
        hovertemplate=(
            "<b>%{x}</b><br>" +
            "Average LOS: %{y:.1f} days<br>" +
            "Range: %{customdata[0]:.1f} - %{customdata[1]:.1f} days<br>" +
            "Total Cases: %{customdata[2]}<br>" +
            "<extra></extra>"
        ),
        customdata=los_df[['min_los', 'max_los', 'total_cases']].values
    ))

    # Add mean line
    fig.add_hline(
        y=overall_mean,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Service Mean: {overall_mean:.1f} days",
        annotation_position="top right"
    )

    fig.update_layout(
        title='Length of Stay Distribution by Surgeon',
        yaxis_title='Average Days',
        showlegend=False,
        height=600,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#2c3e50'},
        margin=dict(t=50, l=50, r=30, b=50),
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="sans-serif"
        )
    )

    return fig

def create_complication_rate_chart(df, service, current_surgeon):
    """Create complication rate comparison chart."""
    service_data = df[df['service'] == service]

    comp_rates = []
    for surgeon in service_data['surgeon'].unique():
        surgeon_data = service_data[service_data['surgeon'] == surgeon]
        complications = surgeon_data['complications'].sum()
        total_cases = len(surgeon_data)
        comp_rates.append({
            'surgeon': surgeon,
            'rate': (complications / total_cases * 100) if total_cases > 0 else 0,
            'complications': complications,
            'total_cases': total_cases
        })

    comp_df = pd.DataFrame(comp_rates)

    # Calculate overall mean complication rate for the service
    overall_mean = service_data['complications'].mean() * 100

    fig = go.Figure()

    # Add bar chart with custom hover template
    fig.add_trace(go.Bar(
        x=comp_df['surgeon'],
        y=comp_df['rate'],
        marker_color=[
            '#0066cc' if surgeon == current_surgeon else '#B3B3B3'
            for surgeon in comp_df['surgeon']
        ],
        hovertemplate=(
            "<b>%{x}</b><br>" +
            "Complication Rate: %{y:.1f}%<br>" +
            "Cases with Complications: %{customdata[0]}<br>" +
            "Total Cases: %{customdata[1]}<br>" +
            "<extra></extra>"
        ),
        customdata=comp_df[['complications', 'total_cases']].values
    ))

    # Add mean line
    fig.add_hline(
        y=overall_mean,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Service Mean: {overall_mean:.1f}%",
        annotation_position="top right"
    )

    fig.update_layout(
        title='Complication Rates by Surgeon',
        xaxis_title='',
        yaxis_title='Complication Rate (%)',
        showlegend=False,
        height=600,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#2c3e50'},
        margin=dict(t=50, l=50, r=30, b=50),
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="sans-serif"
        )
    )

    return fig

def create_stage_distribution_chart(df, service, current_surgeon, stage_type='t_stage'):
    """Create stage distribution chart."""
    service_data = df[df['service'] == service]

    stage_dist = []
    for surgeon in service_data['surgeon'].unique():
        surgeon_data = service_data[service_data['surgeon'] == surgeon]
        total_cases = len(surgeon_data)
        for stage in sorted(service_data[stage_type].unique()):
            stage_count = len(surgeon_data[surgeon_data[stage_type] == stage])
            stage_dist.append({
                'surgeon': surgeon,
                'stage': stage,
                'count': stage_count,
                'percentage': (stage_count / total_cases * 100) if total_cases > 0 else 0,
                'total_cases': total_cases
            })

    stage_df = pd.DataFrame(stage_dist)

    # Calculate overall percentage for each stage across all surgeons
    overall_stage_dist = (service_data[stage_type].value_counts() / len(service_data) * 100).round(1)

    fig = go.Figure()

    # Add grouped bars for each stage with custom hover template
    for stage in sorted(stage_df['stage'].unique()):
        stage_data = stage_df[stage_df['stage'] == stage]
        fig.add_trace(go.Bar(
            name=stage,
            x=stage_data['surgeon'],
            y=stage_data['percentage'],
            marker_color=[
                '#0066cc' if surgeon == current_surgeon else '#B3B3B3'
                for surgeon in stage_data['surgeon']
            ],
            hovertemplate=(
                "<b>%{x}</b><br>" +
                f"Stage {stage}<br>" +
                "Percentage: %{y:.1f}%<br>" +
                "Count: %{customdata[0]}<br>" +
                "Total Cases: %{customdata[1]}<br>" +
                "<extra></extra>"
            ),
            customdata=stage_data[['count', 'total_cases']].values
        ))

    # Add mean line for overall service distribution
    colors = px.colors.qualitative.Set3
    for i, (stage, percentage) in enumerate(overall_stage_dist.items()):
        fig.add_hline(
            y=percentage,
            line_dash="dash",
            line_color=colors[i % len(colors)],
            annotation_text=f"{stage} Service Mean: {percentage:.1f}%",
            annotation_position="top right",
            annotation_yshift=15 * i  # Stack annotations
        )

    fig.update_layout(
        title=f'{stage_type.upper()} Distribution by Surgeon',
        xaxis_title='',
        yaxis_title='Percentage of Cases (%)',
        barmode='group',
        showlegend=True,
        legend_title='Stage',
        height=600,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#2c3e50'},
        margin=dict(t=50, l=50, r=30, b=50),
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="sans-serif"
        )
    )

    return fig