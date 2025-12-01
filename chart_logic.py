import pandas as pd

CHART_REQUIREMENTS = {
    'bar': {
        'x_types': ['categorical'],
        'y_types': ['numeric'],
        'requires_y': True,
        'show_x': True,
        'show_y': True,
        'description': '1 categorical + 1 numerical',
        'example': 'Categories vs Sales Amount'
    },
    'histogram': {
        'x_types': ['numeric'],
        'y_types': [],
        'requires_y': False,
        'show_x': True,
        'show_y': False,
        'description': '1 numerical',
        'example': 'Age Distribution'
    },
    'pie': {
        'x_types': ['categorical'],
        'y_types': ['numeric'],
        'requires_y': True,
        'show_x': False,
        'show_y': False,
        'description': '1 categorical + 1 numerical',
        'example': 'Market Share by Company'
    },
    'doughnut': {
        'x_types': ['categorical'],
        'y_types': ['numeric'],
        'requires_y': True,
        'show_x': False,
        'show_y': False,
        'description': '1 categorical + 1 numerical',
        'example': 'Sales by Region'
    },
    'line': {
        'x_types': ['datetime', 'numeric'],
        'y_types': ['numeric'],
        'requires_y': True,
        'show_x': True,
        'show_y': True,
        'description': '1 time + 1 numerical (or more)',
        'example': 'Sales Trend Over Time'
    },
    'scatter': {
        'x_types': ['numeric'],
        'y_types': ['numeric'],
        'requires_y': True,
        'show_x': True,
        'show_y': True,
        'description': '2 numerical (+ optional categorical)',
        'example': 'Height vs Weight'
    },
    'box': {
        'x_types': ['numeric', 'categorical'],
        'y_types': ['numeric'],
        'requires_y': True,
        'show_x': True,
        'show_y': True,
        'description': '1 numerical (+ optional categorical)',
        'example': 'Sales Distribution by Category'
    },
    'stacked_bar': {
        'x_types': ['categorical'],
        'y_types': ['numeric'],
        'requires_y': True,
        'show_x': True,
        'show_y': True,
        'description': '2 categorical + 1 numerical',
        'example': 'Sales by Region and Product Type'
    },
    'heatmap': {
        'x_types': ['categorical', 'numeric'],
        'y_types': ['categorical', 'numeric'],
        'requires_y': True,
        'show_x': True,
        'show_y': True,
        'description': '2 categorical + 1 numerical OR correlation matrix',
        'example': 'Sales by Month and Region'
    },
    'area': {
        'x_types': ['datetime', 'numeric'],
        'y_types': ['numeric'],
        'requires_y': True,
        'show_x': True,
        'show_y': True,
        'description': '1 time + 1+ numerical',
        'example': 'Revenue Growth Over Time'
    },
    'bubble': {
        'x_types': ['numeric'],
        'y_types': ['numeric'],
        'requires_y': True,
        'show_x': True,
        'show_y': True,
        'description': '3 numerical (+ optional categorical)',
        'example': 'Price vs Quality vs Popularity'
    }
}

def get_column_type(df, column):
    if pd.api.types.is_datetime64_any_dtype(df[column]):
        return 'datetime'
    elif pd.api.types.is_numeric_dtype(df[column]):
        return 'numeric'
    else:
        return 'categorical'

def get_compatible_columns(df, chart_type):
    if chart_type not in CHART_REQUIREMENTS:
        return {'x_columns': [], 'y_columns': [], 'requires_y': False, 'show_x': True, 'show_y': True}
    
    requirements = CHART_REQUIREMENTS[chart_type]
    
    x_compatible = []
    y_compatible = []
    
    for column in df.columns:
        col_type = get_column_type(df, column)
        
        if col_type in requirements['x_types']:
            x_compatible.append(column)
        
        if col_type in requirements['y_types']:
            y_compatible.append(column)
    
    return {
        'x_columns': x_compatible,
        'y_columns': y_compatible,
        'requires_y': requirements['requires_y'],
        'show_x': requirements['show_x'],
        'show_y': requirements['show_y'],
        'description': requirements['description'],
        'example': requirements['example']
    }

def get_chart_requirements(chart_type):
    return CHART_REQUIREMENTS.get(chart_type, {})

