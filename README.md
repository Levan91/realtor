# 🏠 Realtor Dashboard

A Streamlit-based real estate dashboard with context-aware filtering capabilities.

## Features

- **Context-Aware Filters**: 6 interconnected filters that update based on selections
  - Development
  - Community  
  - Sub Community
  - Bedrooms
  - Layout Type
  - Status
- **No Callbacks**: Smooth user experience without page refreshes
- **Auto-Selection**: Previous filters automatically adjust when selecting out of order
- **Real-time Updates**: Filter options update dynamically based on current selections

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Running the App

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser and navigate to the URL shown in the terminal (usually `http://localhost:8501`)

## How the Filters Work

The filters are designed to be context-aware:

1. **Normal Order**: Select filters from top to bottom (Development → Community → Sub Community → etc.)
2. **Out of Order**: If you select a filter out of order (e.g., Sub Community first), the previous filters will automatically adjust to show only valid options
3. **Auto-Selection**: If there's only one valid option for a previous filter, it will be auto-selected
4. **Reset**: Filters after the selected one are reset to "All"

## Sample Data

The app currently uses generated sample data with:
- 5 Developments (Palm Jumeirah, Downtown Dubai, Dubai Marina, JBR, Emirates Hills)
- Multiple communities and sub-communities for each development
- Various bedroom counts, layout types, and statuses
- 500 sample properties

## Customization

To use your own data:
1. Replace the `generate_sample_data()` function with your data loading logic
2. Ensure your DataFrame has the required columns: Development, Community, Sub Community, Bedrooms, Layout Type, Status
3. Add any additional columns you want to display

## Deployment

This app is ready for deployment on Streamlit Cloud:
1. Push your code to a GitHub repository
2. Connect your repository to Streamlit Cloud
3. Deploy with the command: `streamlit run app.py` 