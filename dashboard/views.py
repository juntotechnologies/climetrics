from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from .models import Procedure, Surgeon
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json

def home(request):
    return render(request, 'dashboard/home.html')

@login_required
def dashboard(request):
    surgeons = Surgeon.objects.all()
    
    # Get all available services from the model
    services = dict(Procedure.SERVICE_CHOICES)
    
    # Get selected service from query params, default to first service
    selected_service = request.GET.get('service', 'Melanoma')
    
    # Filter procedures by selected service
    procedures = Procedure.objects.filter(service=selected_service)
    
    # Calculate metrics
    metrics = {
        'total_procedures': procedures.count(),
        'avg_length_of_stay': procedures.aggregate(Avg('length_of_stay'))['length_of_stay__avg'] or 0,
        'complication_rate': (procedures.filter(complications=True).count() / max(procedures.count(), 1) * 100)
    }
    
    context = {
        'surgeons': surgeons,
        'services': services,
        'selected_service': selected_service,
        'metrics': metrics,
    }
    
    return render(request, 'dashboard/dashboard.html', context)

def get_procedures_df():
    """Get all procedures as a pandas DataFrame."""
    procedures = Procedure.objects.all()
    data = []
    for proc in procedures:
        data.append({
            'service': proc.service,
            'surgeon': proc.surgeon.name,
            'date': proc.date,
            'length_of_stay': proc.length_of_stay,
            'complications': proc.complications,
            't_stage': proc.t_stage,
            'p_stage': proc.p_stage,
            'procedure_time': proc.procedure_time
        })
    return pd.DataFrame(data)

@login_required
def los_comparison(request):
    df = get_procedures_df()
    selected_service = request.GET.get('service', 'Melanoma')
    
    service_data = df[df['service'] == selected_service]
    
    # Calculate LOS statistics by surgeon
    los_stats = service_data.groupby('surgeon')['length_of_stay'].agg([
        ('avg_los', 'mean'),
        ('min_los', 'min'),
        ('max_los', 'max'),
        ('total_cases', 'count')
    ]).reset_index()

    # Calculate overall average LOS for the selected service
    overall_avg_los = service_data['length_of_stay'].mean()

    # Create the figure
    fig = go.Figure()
    
    # Add box plot
    fig.add_trace(go.Box(
        x=service_data['surgeon'],
        y=service_data['length_of_stay'],
        name='LOS Distribution',
        boxpoints='all',
        jitter=0.3,
        pointpos=-1.8
    ))

    # Add average markers
    fig.add_trace(go.Scatter(
        x=los_stats['surgeon'],
        y=los_stats['avg_los'],
        mode='markers',
        name='Average LOS',
        marker=dict(
            color='red',
            size=12,
            symbol='diamond'
        )
    ))

    # Add overall average line
    fig.add_hline(
        y=overall_avg_los,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Overall Average: {overall_avg_los:.1f} days",
        annotation_position="right"
    )

    fig.update_layout(
        title=f'Length of Stay Comparison - {selected_service}',
        xaxis_title='Surgeon',
        yaxis_title='Length of Stay (days)',
        boxmode='group',
        height=600,
        showlegend=True
    )

    plot_div = fig.to_html(full_html=False)
    
    context = {
        'plot_div': plot_div,
        'selected_service': selected_service,
        'services': dict(Procedure.SERVICE_CHOICES)
    }
    
    return render(request, 'dashboard/los_comparison.html', context)

@login_required
def complication_rates(request):
    df = get_procedures_df()
    selected_service = request.GET.get('service', 'Melanoma')
    
    service_data = df[df['service'] == selected_service]
    
    # Calculate complication rates by surgeon
    comp_rates = service_data.groupby('surgeon').agg(
        total_cases=('complications', 'count'),
        complications=('complications', 'sum')
    ).reset_index()
    
    comp_rates['rate'] = (comp_rates['complications'] / comp_rates['total_cases'] * 100)

    # Calculate overall complication rate for the selected service
    overall_comp_rate = (service_data['complications'].sum() / len(service_data) * 100)

    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=comp_rates['surgeon'],
        y=comp_rates['rate'],
        text=comp_rates['rate'].round(1).astype(str) + '%',
        textposition='auto',
    ))

    # Add overall average line
    fig.add_hline(
        y=overall_comp_rate,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Overall Average: {overall_comp_rate:.1f}%",
        annotation_position="right"
    )

    fig.update_layout(
        title=f'Complication Rates by Surgeon - {selected_service}',
        xaxis_title='Surgeon',
        yaxis_title='Complication Rate (%)',
        height=500,
        yaxis_range=[0, 100]
    )

    plot_div = fig.to_html(full_html=False)
    
    context = {
        'plot_div': plot_div,
        'selected_service': selected_service,
        'services': dict(Procedure.SERVICE_CHOICES)
    }
    
    return render(request, 'dashboard/complication_rates.html', context)

@login_required
def stage_distribution(request):
    df = get_procedures_df()
    selected_service = request.GET.get('service', 'Melanoma')
    stage_type = request.GET.get('stage_type', 't_stage')
    
    service_data = df[df['service'] == selected_service]
    
    # Calculate stage distribution
    stage_dist = pd.crosstab(
        service_data['surgeon'],
        service_data[stage_type],
        normalize='index'
    ) * 100

    fig = go.Figure()
    
    for stage in stage_dist.columns:
        fig.add_trace(go.Bar(
            name=stage,
            x=stage_dist.index,
            y=stage_dist[stage],
            text=stage_dist[stage].round(1).astype(str) + '%',
            textposition='auto',
        ))

    fig.update_layout(
        title=f'{stage_type.upper()} Distribution by Surgeon - {selected_service}',
        xaxis_title='Surgeon',
        yaxis_title='Percentage of Cases (%)',
        barmode='group',
        height=600,
        yaxis_range=[0, 100]
    )

    plot_div = fig.to_html(full_html=False)
    
    context = {
        'plot_div': plot_div,
        'selected_service': selected_service,
        'services': dict(Procedure.SERVICE_CHOICES),
        'stage_type': stage_type
    }
    
    return render(request, 'dashboard/stage_distribution.html', context) 