from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from .models import Procedure, Surgeon
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import os

def home(request):
    return render(request, 'dashboard/home.html')

def load_surgeon_rates():
    """Load the surgeon rates data from CSV file"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rates_file = os.path.join(base_dir, 'output', 'surgeon_rates.csv', 'SurgeonRates.csv')
    
    if not os.path.exists(rates_file):
        raise FileNotFoundError('Surgeon rates file not found. Please ensure rates have been generated.')
        
    return pd.read_csv(rates_file)

@login_required
def dashboard(request):
    try:
        # Get basic procedure metrics
        procedures = Procedure.objects.all()
        total_procedures = procedures.count()
        avg_los = procedures.aggregate(Avg('length_of_stay'))['length_of_stay__avg'] or 0
        complication_rate = (procedures.filter(complications=True).count() / max(total_procedures, 1)) * 100

        # Get surgeon rates data
        df = load_surgeon_rates()
        
        # Get selected rate type from query params, default to SLND
        rate_type = request.GET.get('rate_type', 'SLND')
        
        # Filter rates by type
        filtered_df = df[df['modelId'].str.startswith(rate_type)]
        
        # Calculate surgeon rate metrics
        rate_metrics = {
            'total_surgeons': len(filtered_df['userId'].unique()),
            'avg_rate': filtered_df['rate'].mean() * 100,
            'min_rate': filtered_df['rate'].min() * 100,
            'max_rate': filtered_df['rate'].max() * 100
        }
        
        # Get available rate types
        rate_types = sorted(list(set([
            model_id.split('.')[0] 
            for model_id in df['modelId'].unique()
        ])))
        
        # Create a plot for the dashboard
        fig = go.Figure()
        
        # Add scatter plot for each surgeon
        for surgeon in filtered_df['userId'].unique():
            surgeon_data = filtered_df[filtered_df['userId'] == surgeon]
            
            fig.add_trace(go.Scatter(
                name=surgeon,
                x=surgeon_data['modelId'],
                y=surgeon_data['rate'] * 100,  # Convert to percentage
                mode='lines+markers',
                error_y=dict(
                    type='data',
                    array=(surgeon_data['upperCI'] - surgeon_data['rate']) * 100,
                    arrayminus=(surgeon_data['rate'] - surgeon_data['lowerCI']) * 100,
                    visible=True
                )
            ))
        
        # Update layout
        fig.update_layout(
            title=f'{rate_type} Rates by Surgeon Over Time',
            xaxis_title='Time Period',
            yaxis_title='Rate (%)',
            height=400,  # Smaller height for dashboard
            showlegend=True,
            yaxis_range=[0, 100]
        )
        
        # Rotate x-axis labels for better readability
        fig.update_xaxes(tickangle=45)
        
        plot_div = fig.to_html(full_html=False)
        
        context = {
            'basic_metrics': {
                'total_procedures': total_procedures,
                'avg_los': round(avg_los, 1),
                'complication_rate': round(complication_rate, 1)
            },
            'rate_metrics': rate_metrics,
            'rate_types': rate_types,
            'selected_rate_type': rate_type,
            'plot_div': plot_div
        }
        
        return render(request, 'dashboard/dashboard.html', context)
        
    except Exception as e:
        return render(request, 'dashboard/dashboard.html', {
            'error_message': str(e)
        })

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
    try:
        # Get procedures data for basic complication rates
        procedures = Procedure.objects.all()
        if not procedures.exists():
            return render(request, 'dashboard/complication_rates.html', {
                'error_message': 'No procedure data available. Please add some procedures first.'
            })

        # Calculate basic complication rates by surgeon
        surgeon_complications = {}
        for surgeon in Surgeon.objects.all():
            surgeon_procs = procedures.filter(surgeon=surgeon)
            if surgeon_procs.exists():
                comp_rate = (surgeon_procs.filter(complications=True).count() / surgeon_procs.count()) * 100
                surgeon_complications[surgeon.name] = comp_rate

        # Create basic complication rate plot
        fig = go.Figure()
        
        surgeons = list(surgeon_complications.keys())
        rates = list(surgeon_complications.values())
        
        # Add bar chart
        fig.add_trace(go.Bar(
            x=surgeons,
            y=rates,
            text=[f"{rate:.1f}%" for rate in rates],
            textposition='auto',
        ))
        
        # Calculate and add overall average line
        overall_rate = sum(rates) / len(rates) if rates else 0
        fig.add_hline(
            y=overall_rate,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Overall Average: {overall_rate:.1f}%",
            annotation_position="right"
        )
        
        fig.update_layout(
            title='Overall Complication Rates by Surgeon',
            xaxis_title='Surgeon',
            yaxis_title='Complication Rate (%)',
            height=500,
            yaxis_range=[0, 100],
            showlegend=False
        )
        
        plot_div = fig.to_html(full_html=False)
        
        context = {
            'plot_div': plot_div,
            'basic_metrics': {
                'total_procedures': procedures.count(),
                'total_complications': procedures.filter(complications=True).count(),
                'overall_rate': overall_rate
            }
        }
        
        # Try to get detailed complication rates if available
        try:
            df = load_surgeon_rates()
            comp_data = df[df['modelId'].str.startswith('COMP')]
            
            if not comp_data.empty:
                # Add detailed complication data to context
                context['has_detailed_data'] = True
                context['comp_types'] = sorted(list(set([
                    '.'.join(model_id.split('.')[:3])
                    for model_id in comp_data['modelId']
                ])))
                context['rate_type'] = request.GET.get('rate_type', 'COMP.ANY.COMPGRADE2')
        except:
            # If detailed data is not available, we'll just show the basic view
            pass
            
        return render(request, 'dashboard/complication_rates.html', context)
        
    except Exception as e:
        return render(request, 'dashboard/complication_rates.html', {
            'error_message': f'Error loading complication rates: {str(e)}'
        })

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

@login_required
def surgeon_rates(request):
    try:
        df = load_surgeon_rates()
        rate_type = request.GET.get('rate_type', 'SLND')  # Default to SLND rates
        
        # Filter rates by type (e.g., SLND, POSSLND, CLND, complications)
        filtered_df = df[df['modelId'].str.startswith(rate_type)]
        
        if filtered_df.empty:
            return render(request, 'dashboard/surgeon_rates.html', {
                'error_message': f'No data found for rate type: {rate_type}',
                'rate_types': sorted(list(set([
                    model_id.split('.')[0] 
                    for model_id in df['modelId'].unique()
                ])))
            })
        
        # Create figure
        fig = go.Figure()
        
        # Add scatter plot for each surgeon
        for surgeon in filtered_df['userId'].unique():
            surgeon_data = filtered_df[filtered_df['userId'] == surgeon]
            
            fig.add_trace(go.Scatter(
                name=surgeon,
                x=surgeon_data['modelId'],
                y=surgeon_data['rate'] * 100,  # Convert to percentage
                mode='lines+markers',
                error_y=dict(
                    type='data',
                    array=(surgeon_data['upperCI'] - surgeon_data['rate']) * 100,
                    arrayminus=(surgeon_data['rate'] - surgeon_data['lowerCI']) * 100,
                    visible=True
                )
            ))
        
        # Update layout
        fig.update_layout(
            title=f'{rate_type} Rates by Surgeon Over Time',
            xaxis_title='Time Period',
            yaxis_title='Rate (%)',
            height=600,
            showlegend=True,
            yaxis_range=[0, 100]
        )
        
        # Rotate x-axis labels for better readability
        fig.update_xaxes(tickangle=45)
        
        plot_div = fig.to_html(full_html=False)
        
        # Get available rate types from the data
        rate_types = sorted(list(set([
            model_id.split('.')[0] 
            for model_id in df['modelId'].unique()
        ])))
        
        context = {
            'plot_div': plot_div,
            'rate_type': rate_type,
            'rate_types': rate_types
        }
        
        return render(request, 'dashboard/surgeon_rates.html', context)
        
    except Exception as e:
        return render(request, 'dashboard/surgeon_rates.html', {
            'error_message': f'Error loading surgeon rates: {str(e)}'
        })

@login_required
def users_list(request):
    """View to display all users and their basic information."""
    try:
        users = User.objects.all().order_by('username')
        
        context = {
            'users': [{
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
                'date_joined': user.date_joined,
                'last_login': user.last_login
            } for user in users]
        }
        
        return render(request, 'dashboard/users_list.html', context)
        
    except Exception as e:
        return render(request, 'dashboard/users_list.html', {
            'error_message': f'Error loading users: {str(e)}'
        }) 