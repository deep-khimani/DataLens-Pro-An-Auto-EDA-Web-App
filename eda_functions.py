import matplotlib
matplotlib.use("Agg")

import pandas as pd
import numpy as np
import openai
import os
from dotenv import load_dotenv
import json

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_data_preview(df, table_option):
    if table_option == "full":
        data = df.head(100) if len(df) > 100 else df
    elif table_option == "tail":
        data = df.tail(10)
    elif table_option == "sample":
        n_samples = min(10, len(df))
        data = df.sample(n=n_samples, random_state=42) if len(df) > 0 else df
    else:
        data = df.head(10)
    
    return data.to_html(classes="table table-striped table-hover", border=0, escape=False)

def get_statistics(df):
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.empty:
        return "<p class='text-muted'>No numeric columns found for statistical analysis.</p>"
    
    stats = numeric_df.describe()
    stats.loc['missing'] = df.isnull().sum()[numeric_df.columns]
    stats.loc['dtype'] = [str(dtype) for dtype in numeric_df.dtypes]
    
    return stats.to_html(classes="table table-striped table-hover", border=0)

def create_chart_with_api(df, chart_type, x_column, y_column=None, size_column=None, stack_column=None):
    try:
        chart_data = {'labels': [], 'datasets': []}
        
        # Professional color palette
        colors = [
            'rgba(102, 126, 234, 0.8)', 'rgba(255, 99, 132, 0.8)', 'rgba(54, 162, 235, 0.8)',
            'rgba(255, 205, 86, 0.8)', 'rgba(75, 192, 192, 0.8)', 'rgba(153, 102, 255, 0.8)',
            'rgba(255, 159, 64, 0.8)', 'rgba(199, 199, 199, 0.8)', 'rgba(83, 102, 255, 0.8)',
            'rgba(255, 99, 255, 0.8)', 'rgba(99, 255, 132, 0.8)', 'rgba(255, 192, 203, 0.8)'
        ]
        
        if chart_type == 'bar':
            # 1 categorical + 1 numerical
            if pd.api.types.is_numeric_dtype(df[x_column]):
                # Convert numeric to categories using binning
                df_copy = df.copy()
                df_copy[f'{x_column}_binned'] = pd.cut(df_copy[x_column], bins=10, duplicates='drop')
                grouped = df_copy.groupby(f'{x_column}_binned')[y_column].mean().dropna()
                chart_data['labels'] = [str(label) for label in grouped.index]
            else:
                # Categorical x-axis
                grouped = df.groupby(x_column)[y_column].mean().sort_values(ascending=False).head(15)
                chart_data['labels'] = grouped.index.tolist()
            
            chart_data['datasets'] = [{
                'label': f'{y_column} by {x_column}',
                'data': grouped.values.tolist(),
                'backgroundColor': colors[0],
                'borderColor': colors[0].replace('0.8', '1'),
                'borderWidth': 2,
                'borderRadius': 4,
                'borderSkipped': False
            }]
            
        elif chart_type == 'histogram':
            # 1 numerical
            data_values = df[x_column].dropna()
            hist, bin_edges = np.histogram(data_values, bins=20)
            chart_data['labels'] = [f'{bin_edges[i]:.2f}' for i in range(len(hist))]
            chart_data['datasets'] = [{
                'label': f'Distribution of {x_column}',
                'data': hist.tolist(),
                'backgroundColor': colors[0],
                'borderColor': colors[0].replace('0.8', '1'),
                'borderWidth': 1
            }]
            chart_type = 'bar'  # Use bar chart for histogram
            
        elif chart_type in ['pie', 'doughnut']:
            # 1 categorical + 1 numerical
            grouped = df.groupby(x_column)[y_column].sum().sort_values(ascending=False).head(8)
            chart_data['labels'] = grouped.index.tolist()
            chart_data['datasets'] = [{
                'label': f'{x_column}',
                'data': grouped.values.tolist(),
                'backgroundColor': colors[:len(grouped)],
                'borderWidth': 2,
                'borderColor': 'rgba(255, 255, 255, 0.8)'
            }]
            
        elif chart_type == 'line':
            # 1 time + 1 numerical (or more)
            df_sorted = df.sort_values(x_column).dropna(subset=[x_column, y_column])
            if len(df_sorted) > 500:
                df_sorted = df_sorted.iloc[::len(df_sorted)//500]  # Sample evenly
            
            chart_data['labels'] = df_sorted[x_column].astype(str).tolist()
            chart_data['datasets'] = [{
                'label': y_column,
                'data': df_sorted[y_column].tolist(),
                'borderColor': colors[0].replace('0.8', '1'),
                'backgroundColor': colors[0].replace('0.8', '0.1'),
                'fill': False,
                'tension': 0.4,
                'pointRadius': 2,
                'pointHoverRadius': 6,
                'borderWidth': 3
            }]
            
        elif chart_type == 'scatter':
            # 2 numerical (+ optional categorical)
            sample_size = min(1000, len(df))
            df_sample = df.sample(n=sample_size, random_state=42) if len(df) > sample_size else df
            
            scatter_data = []
            for _, row in df_sample.iterrows():
                if pd.notna(row[x_column]) and pd.notna(row[y_column]):
                    scatter_data.append({
                        'x': float(row[x_column]),
                        'y': float(row[y_column])
                    })
            
            chart_data['datasets'] = [{
                'label': f'{x_column} vs {y_column}',
                'data': scatter_data,
                'backgroundColor': colors[0],
                'borderColor': colors[0].replace('0.8', '1'),
                'pointRadius': 4,
                'pointHoverRadius': 8
            }]
            
        elif chart_type == 'box':
            # 1 numerical (+ optional categorical) - Simplified as histogram
            if pd.api.types.is_numeric_dtype(df[x_column]):
                # Single box plot - show as histogram
                data_values = df[x_column].dropna()
                q1, median, q3 = np.percentile(data_values, [25, 50, 75])
                
                chart_data['labels'] = ['Q1', 'Median', 'Q3', 'Min', 'Max']
                chart_data['datasets'] = [{
                    'label': f'{x_column} Statistics',
                    'data': [q1, median, q3, data_values.min(), data_values.max()],
                    'backgroundColor': colors[:5],
                    'borderWidth': 1
                }]
                chart_type = 'bar'
            else:
                # Box plot by category - show means
                grouped = df.groupby(x_column)[y_column].agg(['mean', 'std']).fillna(0)
                chart_data['labels'] = grouped.index.tolist()
                chart_data['datasets'] = [{
                    'label': f'Average {y_column}',
                    'data': grouped['mean'].tolist(),
                    'backgroundColor': colors[0],
                    'borderWidth': 1
                }]
                chart_type = 'bar'
                
        elif chart_type == 'stacked_bar':
            # 2 categorical + 1 numerical
            if stack_column:
                pivot_df = df.pivot_table(values=y_column, index=x_column, columns=stack_column, 
                                        aggfunc='sum', fill_value=0)
                chart_data['labels'] = pivot_df.index.tolist()
                
                datasets = []
                for i, col in enumerate(pivot_df.columns[:6]):  # Limit to 6 stacks
                    datasets.append({
                        'label': str(col),
                        'data': pivot_df[col].tolist(),
                        'backgroundColor': colors[i % len(colors)],
                        'borderWidth': 1
                    })
                chart_data['datasets'] = datasets
            else:
                # Fallback to regular bar
                grouped = df.groupby(x_column)[y_column].sum().head(10)
                chart_data['labels'] = grouped.index.tolist()
                chart_data['datasets'] = [{
                    'label': y_column,
                    'data': grouped.values.tolist(),
                    'backgroundColor': colors[0]
                }]
            chart_type = 'bar'
            
        elif chart_type == 'heatmap':
            # 2 categorical + 1 numerical OR correlation matrix
            if pd.api.types.is_numeric_dtype(df[x_column]) and pd.api.types.is_numeric_dtype(df[y_column]):
                # Correlation matrix visualization
                numeric_cols = df.select_dtypes(include=[np.number]).columns[:5]  # Limit to 5
                corr_matrix = df[numeric_cols].corr()
                
                # Convert to format suitable for Chart.js scatter plot
                scatter_data = []
                for i, col1 in enumerate(corr_matrix.columns):
                    for j, col2 in enumerate(corr_matrix.index):
                        scatter_data.append({
                            'x': i,
                            'y': j,
                            'v': corr_matrix.loc[col2, col1]  # correlation value
                        })
                
                chart_data['datasets'] = [{
                    'label': 'Correlation',
                    'data': scatter_data,
                    'backgroundColor': lambda ctx: get_heatmap_color(ctx.parsed.v),
                    'pointRadius': 15
                }]
                chart_type = 'scatter'
            else:
                # Categorical heatmap as grouped bar
                grouped = df.groupby([x_column, y_column]).size().reset_index(name='count')
                pivot_df = grouped.pivot(index=x_column, columns=y_column, values='count').fillna(0)
                
                chart_data['labels'] = pivot_df.index.tolist()
                datasets = []
                for i, col in enumerate(pivot_df.columns[:8]):
                    datasets.append({
                        'label': str(col),
                        'data': pivot_df[col].tolist(),
                        'backgroundColor': colors[i % len(colors)]
                    })
                chart_data['datasets'] = datasets
                chart_type = 'bar'
                
        elif chart_type == 'area':
            # 1 time + 1+ numerical
            df_sorted = df.sort_values(x_column).dropna(subset=[x_column, y_column])
            if len(df_sorted) > 300:
                df_sorted = df_sorted.iloc[::len(df_sorted)//300]
            
            chart_data['labels'] = df_sorted[x_column].astype(str).tolist()
            chart_data['datasets'] = [{
                'label': y_column,
                'data': df_sorted[y_column].tolist(),
                'borderColor': colors[0].replace('0.8', '1'),
                'backgroundColor': colors[0].replace('0.8', '0.3'),
                'fill': True,
                'tension': 0.4,
                'borderWidth': 2
            }]
            chart_type = 'line'
            
        elif chart_type == 'bubble':
            # 3 numerical (+ optional categorical)
            sample_size = min(500, len(df))
            df_sample = df.sample(n=sample_size, random_state=42) if len(df) > sample_size else df
            
            if not size_column:
                size_column = df.select_dtypes(include=[np.number]).columns[0]
            
            bubble_data = []
            for _, row in df_sample.iterrows():
                if pd.notna(row[x_column]) and pd.notna(row[y_column]) and pd.notna(row[size_column]):
                    bubble_data.append({
                        'x': float(row[x_column]),
                        'y': float(row[y_column]),
                        'r': max(3, min(20, abs(float(row[size_column])) / df[size_column].std() * 5))
                    })
            
            chart_data['datasets'] = [{
                'label': f'{x_column} vs {y_column} (Size: {size_column})',
                'data': bubble_data,
                'backgroundColor': colors[0],
                'borderColor': colors[0].replace('0.8', '1'),
                'borderWidth': 1
            }]
        
        return {
            'type': chart_type,
            'data': chart_data,
            'options': get_chart_options(chart_type, x_column, y_column, size_column)
        }
        
    except Exception as e:
        raise Exception(f"Error creating {chart_type} chart: {str(e)}")

def get_heatmap_color(value):
    """Generate color based on correlation value"""
    if value > 0.7:
        return 'rgba(255, 0, 0, 0.8)'    # Red for strong positive
    elif value > 0.3:
        return 'rgba(255, 165, 0, 0.8)'  # Orange for moderate positive
    elif value > -0.3:
        return 'rgba(255, 255, 255, 0.8)'  # White for weak
    elif value > -0.7:
        return 'rgba(0, 0, 255, 0.6)'    # Light blue for moderate negative
    else:
        return 'rgba(0, 0, 139, 0.8)'    # Dark blue for strong negative

def get_chart_options(chart_type, x_column, y_column=None, size_column=None):
    base_options = {
        'responsive': True,
        'maintainAspectRatio': False,
        'plugins': {
            'title': {
                'display': True,
                'text': f'{chart_type.replace("_", " ").title()}: {x_column}' + 
                       (f' vs {y_column}' if y_column else '') + 
                       (f' (Size: {size_column})' if size_column else ''),
                'font': {'size': 16, 'weight': 'bold'},
                'padding': 20,
                'color': '#2d3748'
            },
            'legend': {
                'display': True,
                'position': 'top',
                'labels': {
                    'usePointStyle': True,
                    'padding': 15,
                    'font': {'size': 12}
                }
            }
        },
        'animation': {
            'duration': 800,
            'easing': 'easeOutQuart'
        }
    }
    
    # Add scales for charts that need them
    if chart_type not in ['pie', 'doughnut']:
        base_options['scales'] = {
            'x': {
                'title': {
                    'display': True,
                    'text': x_column,
                    'font': {'size': 14, 'weight': 'bold'}
                },
                'grid': {
                    'display': True,
                    'color': 'rgba(0, 0, 0, 0.1)'
                }
            }
        }
        
        if y_column:
            base_options['scales']['y'] = {
                'title': {
                    'display': True,
                    'text': y_column,
                    'font': {'size': 14, 'weight': 'bold'}
                },
                'grid': {
                    'display': True,
                    'color': 'rgba(0, 0, 0, 0.1)'
                },
                'beginAtZero': chart_type in ['bar', 'area']
            }
    
    # Special options for stacked charts
    if chart_type == 'bar' and 'stacked' in str(chart_type):
        base_options['scales']['x']['stacked'] = True
        base_options['scales']['y']['stacked'] = True
    
    return base_options

def get_ai_recommendations(df, x_column=None, y_column=None, chart_type=None, size_column=None, stack_column=None):
    try:
        data_info = {
            'shape': df.shape,
            'numeric_columns': df.select_dtypes(include=[np.number]).columns.tolist()[:5],
            'categorical_columns': df.select_dtypes(include=['object', 'category']).columns.tolist()[:5]
        }
        
        context = f"Chart: {chart_type}, X: {x_column}, Y: {y_column}"
        if size_column:
            context += f", Size: {size_column}"
        if stack_column:
            context += f", Stack: {stack_column}"
            
        prompt = f"""
        Data context: {json.dumps(data_info)}
        Selected: {context}
        
        Provide 3-4 brief insights about this visualization choice.
        Format as JSON array of strings. Each insight should be 1 sentence.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.7
        )
        
        recommendations_text = response.choices[0].message.content.strip()
        
        try:
            recommendations = json.loads(recommendations_text)
        except:
            recommendations = [
                f"✅ {chart_type.title()} is perfect for your data combination",
                f"📊 Shows clear relationship between {x_column} and {y_column or 'distribution'}",
                f"🎯 Great choice for exploring patterns in your dataset",
                f"💡 Consider filtering data if you have too many categories"
            ]
        
        return recommendations[:4]
        
    except Exception as e:
        return [
            f"📊 {chart_type.title()} visualization selected",
            f"✅ Good choice for {x_column}" + (f" and {y_column}" if y_column else ""),
            f"🎯 This chart type effectively shows your data patterns",
            f"💡 Make sure your data is clean for best results"
        ]

