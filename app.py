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
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .filter-section {
        margin-bottom: 1rem;
        padding: 0.5rem;
        border-radius: 0.3rem;
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
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
st.sidebar.title("🏠 Realtor Filters")
st.sidebar.markdown("---")

# Get current filtered options
current_options = get_filtered_options(df, st.session_state.filters)

# Development filter
st.sidebar.markdown('<div class="filter-section">', unsafe_allow_html=True)
st.sidebar.subheader("Development")
development_options = ['All'] + current_options['development']
selected_development = st.sidebar.selectbox(
    "Select Development",
    options=development_options,
    key="development_select",
    index=0 if st.session_state.filters['development'] is None else development_options.index(st.session_state.filters['development'])
)

if selected_development != 'All':
    if selected_development != st.session_state.filters['development']:
        st.session_state.filters = update_filters_based_on_selection(df, 'development', selected_development)
else:
    if st.session_state.filters['development'] is not None:
        st.session_state.filters = update_filters_based_on_selection(df, 'development', None)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Community filter
st.sidebar.markdown('<div class="filter-section">', unsafe_allow_html=True)
st.sidebar.subheader("Community")
community_options = ['All'] + current_options['community']
selected_community = st.sidebar.selectbox(
    "Select Community",
    options=community_options,
    key="community_select",
    index=0 if st.session_state.filters['community'] is None else community_options.index(st.session_state.filters['community'])
)

if selected_community != 'All':
    if selected_community != st.session_state.filters['community']:
        st.session_state.filters = update_filters_based_on_selection(df, 'community', selected_community)
else:
    if st.session_state.filters['community'] is not None:
        st.session_state.filters = update_filters_based_on_selection(df, 'community', None)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Sub Community filter
st.sidebar.markdown('<div class="filter-section">', unsafe_allow_html=True)
st.sidebar.subheader("Sub Community")
sub_community_options = ['All'] + current_options['sub_community']
selected_sub_community = st.sidebar.selectbox(
    "Select Sub Community",
    options=sub_community_options,
    key="sub_community_select",
    index=0 if st.session_state.filters['sub_community'] is None else sub_community_options.index(st.session_state.filters['sub_community'])
)

if selected_sub_community != 'All':
    if selected_sub_community != st.session_state.filters['sub_community']:
        st.session_state.filters = update_filters_based_on_selection(df, 'sub_community', selected_sub_community)
else:
    if st.session_state.filters['sub_community'] is not None:
        st.session_state.filters = update_filters_based_on_selection(df, 'sub_community', None)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Bedrooms filter
st.sidebar.markdown('<div class="filter-section">', unsafe_allow_html=True)
st.sidebar.subheader("Bedrooms")
bedrooms_options = ['All'] + [str(x) for x in current_options['bedrooms']]
selected_bedrooms = st.sidebar.selectbox(
    "Select Bedrooms",
    options=bedrooms_options,
    key="bedrooms_select",
    index=0 if st.session_state.filters['bedrooms'] is None else bedrooms_options.index(str(st.session_state.filters['bedrooms']))
)

if selected_bedrooms != 'All':
    if int(selected_bedrooms) != st.session_state.filters['bedrooms']:
        st.session_state.filters = update_filters_based_on_selection(df, 'bedrooms', int(selected_bedrooms))
else:
    if st.session_state.filters['bedrooms'] is not None:
        st.session_state.filters = update_filters_based_on_selection(df, 'bedrooms', None)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Layout Type filter
st.sidebar.markdown('<div class="filter-section">', unsafe_allow_html=True)
st.sidebar.subheader("Layout Type")
layout_options = ['All'] + current_options['layout_type']
selected_layout = st.sidebar.selectbox(
    "Select Layout Type",
    options=layout_options,
    key="layout_select",
    index=0 if st.session_state.filters['layout_type'] is None else layout_options.index(st.session_state.filters['layout_type'])
)

if selected_layout != 'All':
    if selected_layout != st.session_state.filters['layout_type']:
        st.session_state.filters = update_filters_based_on_selection(df, 'layout_type', selected_layout)
else:
    if st.session_state.filters['layout_type'] is not None:
        st.session_state.filters = update_filters_based_on_selection(df, 'layout_type', None)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Status filter
st.sidebar.markdown('<div class="filter-section">', unsafe_allow_html=True)
st.sidebar.subheader("Status")
status_options = ['All'] + current_options['status']
selected_status = st.sidebar.selectbox(
    "Select Status",
    options=status_options,
    key="status_select",
    index=0 if st.session_state.filters['status'] is None else status_options.index(st.session_state.filters['status'])
)

if selected_status != 'All':
    if selected_status != st.session_state.filters['status']:
        st.session_state.filters = update_filters_based_on_selection(df, 'status', selected_status)
else:
    if st.session_state.filters['status'] is not None:
        st.session_state.filters = update_filters_based_on_selection(df, 'status', None)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Clear filters button
if st.sidebar.button("Clear All Filters"):
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