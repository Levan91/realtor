import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Realtor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Modern Sidebar Styling */
    .css-1d391kg {
        background-color: #fafafa;
    }
    
    .css-1lcbmhc {
        background-color: #fafafa;
    }
    
    /* Filter Section Styling */
    .filter-section {
        margin-bottom: 1.5rem;
        padding: 1rem;
        border-radius: 12px;
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: all 0.3s ease;
    }
    
    .filter-section:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transform: translateY(-1px);
    }
    
    /* Filter Headers */
    .filter-header {
        font-size: 0.9rem;
        font-weight: 600;
        color: #495057;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Selectbox Styling */
    .stSelectbox > div > div {
        border-radius: 8px;
        border: 1px solid #dee2e6;
        background-color: #ffffff;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #1f77b4;
    }
    
    /* Button Styling */
    .stButton > button {
        border-radius: 8px;
        border: 1px solid #dee2e6;
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        color: #495057;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1f77b4 0%, #1565c0 100%);
        color: white;
        border-color: #1f77b4;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(31, 119, 180, 0.3);
    }
    
    /* Sidebar Title */
    .sidebar-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #212529;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Divider */
    .sidebar-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, #dee2e6 50%, transparent 100%);
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for filters
if 'filters' not in st.session_state:
    st.session_state.filters = {
        'development': None,
        'community': None,
        'sub_community': None,
        'bedrooms': None,
        'layout_type': None,
        'status': None
    }

# Sample data generation (replace with your actual data source)
@st.cache_data
def generate_sample_data():
    """Generate sample real estate data"""
    np.random.seed(42)
    
    developments = ['Palm Jumeirah', 'Downtown Dubai', 'Dubai Marina', 'JBR', 'Emirates Hills']
    communities = {
        'Palm Jumeirah': ['Palm Tower', 'Palm Gateway', 'Palm Beach'],
        'Downtown Dubai': ['Burj Vista', 'The Address', 'Marina Promenade'],
        'Dubai Marina': ['Marina Gate', 'Marina Heights', 'Marina Bay'],
        'JBR': ['JBR Walk', 'JBR Beach', 'JBR Central'],
        'Emirates Hills': ['Emirates Hills 1', 'Emirates Hills 2', 'Emirates Hills 3']
    }
    
    sub_communities = {
        'Palm Tower': ['Tower A', 'Tower B', 'Tower C'],
        'Palm Gateway': ['Gateway 1', 'Gateway 2'],
        'Palm Beach': ['Beach Front', 'Beach View'],
        'Burj Vista': ['Vista 1', 'Vista 2'],
        'The Address': ['Address 1', 'Address 2'],
        'Marina Promenade': ['Promenade 1', 'Promenade 2'],
        'Marina Gate': ['Gate 1', 'Gate 2'],
        'Marina Heights': ['Height 1', 'Height 2'],
        'Marina Bay': ['Bay 1', 'Bay 2'],
        'JBR Walk': ['Walk 1', 'Walk 2'],
        'JBR Beach': ['Beach 1', 'Beach 2'],
        'JBR Central': ['Central 1', 'Central 2'],
        'Emirates Hills 1': ['Hills 1A', 'Hills 1B'],
        'Emirates Hills 2': ['Hills 2A', 'Hills 2B'],
        'Emirates Hills 3': ['Hills 3A', 'Hills 3B']
    }
    
    bedrooms = [1, 2, 3, 4, 5, 6]
    layout_types = ['Studio', '1BR', '2BR', '3BR', '4BR', '5BR', 'Penthouse', 'Villa']
    statuses = ['Available', 'Sold', 'Under Construction', 'Reserved']
    
    data = []
    for _ in range(500):
        development = np.random.choice(developments)
        community = np.random.choice(communities[development])
        sub_community = np.random.choice(sub_communities[community])
        bedroom = np.random.choice(bedrooms)
        layout_type = np.random.choice(layout_types)
        status = np.random.choice(statuses)
        
        data.append({
            'Development': development,
            'Community': community,
            'Sub Community': sub_community,
            'Bedrooms': bedroom,
            'Layout Type': layout_type,
            'Status': status,
            'Price': np.random.randint(500000, 5000000),
            'Area': np.random.randint(500, 3000)
        })
    
    return pd.DataFrame(data)

# Load data
df = generate_sample_data()

def get_filtered_options(df, current_filters):
    """Get available options for each filter based on current selections"""
    filtered_df = df.copy()
    
    # Apply existing filters
    for filter_name, filter_value in current_filters.items():
        if filter_value is not None:
            column_name = filter_name.replace('_', ' ').title()
            filtered_df = filtered_df[filtered_df[column_name] == filter_value]
    
    # Get unique values for each filter
    options = {}
    filter_columns = ['Development', 'Community', 'Sub Community', 'Bedrooms', 'Layout Type', 'Status']
    
    for col in filter_columns:
        filter_key = col.lower().replace(' ', '_')
        options[filter_key] = sorted(filtered_df[col].unique().tolist())
    
    return options

def update_filters_based_on_selection(df, changed_filter, new_value):
    """Update other filters when one filter changes"""
    # Create a copy of current filters
    new_filters = st.session_state.filters.copy()
    new_filters[changed_filter] = new_value
    
    # If a filter is selected out of order, we need to auto-select or restrict previous filters
    filter_order = ['development', 'community', 'sub_community', 'bedrooms', 'layout_type', 'status']
    changed_index = filter_order.index(changed_filter)
    
    # For filters after the changed one, reset them
    for i in range(changed_index + 1, len(filter_order)):
        new_filters[filter_order[i]] = None
    
    # For filters before the changed one, check if they need to be restricted
    if new_value is not None:
        # Get the filtered dataset based on the new selection
        temp_df = df.copy()
        column_name = changed_filter.replace('_', ' ').title()
        temp_df = temp_df[temp_df[column_name] == new_value]
        
        # Check if previous filters need to be updated
        for i in range(changed_index):
            prev_filter = filter_order[i]
            prev_column = prev_filter.replace('_', ' ').title()
            
            # If the previous filter has a value that's not valid with the new selection
            if new_filters[prev_filter] is not None:
                if new_filters[prev_filter] not in temp_df[prev_column].unique():
                    # Auto-select the only valid option if there's only one
                    valid_options = temp_df[prev_column].unique()
                    if len(valid_options) == 1:
                        new_filters[prev_filter] = valid_options[0]
                    else:
                        # Reset to None if multiple options exist
                        new_filters[prev_filter] = None
    
    return new_filters

# Sidebar
st.sidebar.markdown('<h2 class="sidebar-title">🏠 Realtor</h2>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

current_options = get_filtered_options(df, st.session_state.filters)

# Helper to render a filter card
def filter_card(header, label, options, key, selected, to_str=False):
    with st.sidebar.container():
        st.markdown(f'<div class="filter-section">', unsafe_allow_html=True)
        st.markdown(f'<div class="filter-header">{header}</div>', unsafe_allow_html=True)
        if to_str:
            options = [str(x) for x in options]
            selected = str(selected) if selected is not None else None
        value = st.selectbox(
            label,
            options=options,
            key=key,
            index=0 if selected is None else options.index(selected)
        )
        st.markdown('</div>', unsafe_allow_html=True)
    return value

development_options = ['All'] + current_options['development']
selected_development = filter_card(
    'Development',
    'Select Development',
    development_options,
    'development_select',
    st.session_state.filters['development']
)
if selected_development != 'All':
    if selected_development != st.session_state.filters['development']:
        st.session_state.filters = update_filters_based_on_selection(df, 'development', selected_development)
else:
    if st.session_state.filters['development'] is not None:
        st.session_state.filters = update_filters_based_on_selection(df, 'development', None)

community_options = ['All'] + current_options['community']
selected_community = filter_card(
    'Community',
    'Select Community',
    community_options,
    'community_select',
    st.session_state.filters['community']
)
if selected_community != 'All':
    if selected_community != st.session_state.filters['community']:
        st.session_state.filters = update_filters_based_on_selection(df, 'community', selected_community)
else:
    if st.session_state.filters['community'] is not None:
        st.session_state.filters = update_filters_based_on_selection(df, 'community', None)

sub_community_options = ['All'] + current_options['sub_community']
selected_sub_community = filter_card(
    'Sub Community',
    'Select Sub Community',
    sub_community_options,
    'sub_community_select',
    st.session_state.filters['sub_community']
)
if selected_sub_community != 'All':
    if selected_sub_community != st.session_state.filters['sub_community']:
        st.session_state.filters = update_filters_based_on_selection(df, 'sub_community', selected_sub_community)
else:
    if st.session_state.filters['sub_community'] is not None:
        st.session_state.filters = update_filters_based_on_selection(df, 'sub_community', None)

bedrooms_options = ['All'] + [str(x) for x in current_options['bedrooms']]
selected_bedrooms = filter_card(
    'Bedrooms',
    'Select Bedrooms',
    bedrooms_options,
    'bedrooms_select',
    st.session_state.filters['bedrooms'],
    to_str=True
)
if selected_bedrooms != 'All':
    if int(selected_bedrooms) != st.session_state.filters['bedrooms']:
        st.session_state.filters = update_filters_based_on_selection(df, 'bedrooms', int(selected_bedrooms))
else:
    if st.session_state.filters['bedrooms'] is not None:
        st.session_state.filters = update_filters_based_on_selection(df, 'bedrooms', None)

layout_options = ['All'] + current_options['layout_type']
selected_layout = filter_card(
    'Layout Type',
    'Select Layout Type',
    layout_options,
    'layout_select',
    st.session_state.filters['layout_type']
)
if selected_layout != 'All':
    if selected_layout != st.session_state.filters['layout_type']:
        st.session_state.filters = update_filters_based_on_selection(df, 'layout_type', selected_layout)
else:
    if st.session_state.filters['layout_type'] is not None:
        st.session_state.filters = update_filters_based_on_selection(df, 'layout_type', None)

status_options = ['All'] + current_options['status']
selected_status = filter_card(
    'Status',
    'Select Status',
    status_options,
    'status_select',
    st.session_state.filters['status']
)
if selected_status != 'All':
    if selected_status != st.session_state.filters['status']:
        st.session_state.filters = update_filters_based_on_selection(df, 'status', selected_status)
else:
    if st.session_state.filters['status'] is not None:
        st.session_state.filters = update_filters_based_on_selection(df, 'status', None)

st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
if st.sidebar.button("🗑️ Clear All Filters", use_container_width=True):
    st.session_state.filters = {
        'development': None,
        'community': None,
        'sub_community': None,
        'bedrooms': None,
        'layout_type': None,
        'status': None
    }

# Main content
st.markdown('<h1 class="main-header">🏠 Realtor Dashboard</h1>', unsafe_allow_html=True)

# Apply filters to data
filtered_df = df.copy()
for filter_name, filter_value in st.session_state.filters.items():
    if filter_value is not None:
        column_name = filter_name.replace('_', ' ').title()
        filtered_df = filtered_df[filtered_df[column_name] == filter_value]

# Display results
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Properties", len(filtered_df))
with col2:
    st.metric("Average Price", f"AED {filtered_df['Price'].mean():,.0f}")
with col3:
    st.metric("Average Area", f"{filtered_df['Area'].mean():.0f} sq ft")

# Show filtered data
st.subheader("📋 Property Listings")
st.dataframe(filtered_df, use_container_width=True)

# Debug info (can be removed in production)
with st.expander("Debug: Current Filter State"):
    st.json(st.session_state.filters) 