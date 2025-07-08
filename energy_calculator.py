import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Energy Consumption Calculator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    
    .info-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #bee5eb;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background-color: #1f77b4;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    
    .stSelectbox > div > div > div {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<h1 class="main-header">⚡ Energy Consumption Calculator</h1>', unsafe_allow_html=True)

# Initialize session state
if 'calculated' not in st.session_state:
    st.session_state.calculated = False
    st.session_state.energy_data = {}

# Sidebar for user inputs
with st.sidebar:
    st.header("🏠 Personal Information")
    
    # Personal details
    name = st.text_input("Enter your name:", placeholder="John Doe")
    age = st.number_input("Enter your age:", min_value=18, max_value=100, value=30)
    city = st.text_input("Enter your city:", placeholder="Mumbai")
    area = st.text_input("Enter your area name:", placeholder="Andheri West")
    
    st.header("🏢 Housing Details")
    
    # Housing type
    flat_tenement = st.selectbox(
        "Are you living in Flat or Tenement?",
        ["Flat", "Tenement"]
    )
    
    # BHK configuration
    facility = st.selectbox(
        "Select your housing configuration:",
        ["1BHK", "2BHK", "3BHK"]
    )
    
    st.header("🔌 Appliances")
    
    # Appliances
    ac = st.radio("Are you using AC?", ["Yes", "No"])
    fridge = st.radio("Are you using Fridge?", ["Yes", "No"])
    washing_machine = st.radio("Are you using Washing Machine?", ["Yes", "No"])
    
    # Calculate button
    if st.button("🔍 Calculate Energy Consumption", type="primary"):
        st.session_state.calculated = True
        
        # Energy calculation logic
        cal_energy = 0
        
        # Base energy consumption based on BHK
        if facility == "1BHK":
            cal_energy += 2 * 0.4 + 2 * 0.8  # 2.4 kWh
        elif facility == "2BHK":
            cal_energy += 3 * 0.4 + 3 * 0.8  # 3.6 kWh
        elif facility == "3BHK":
            cal_energy += 4 * 0.4 + 4 * 0.8  # 4.8 kWh
        
        # Additional appliances
        appliances_energy = 0
        appliances_list = []
        
        if ac == "Yes":
            appliances_energy += 3
            appliances_list.append("AC")
        if fridge == "Yes":
            appliances_energy += 3
            appliances_list.append("Fridge")
        if washing_machine == "Yes":
            appliances_energy += 3
            appliances_list.append("Washing Machine")
        
        total_energy = cal_energy + appliances_energy
        
        # Store data in session state
        st.session_state.energy_data = {
            'name': name,
            'age': age,
            'city': city,
            'area': area,
            'flat_tenement': flat_tenement,
            'facility': facility,
            'base_energy': cal_energy,
            'appliances_energy': appliances_energy,
            'total_energy': total_energy,
            'appliances_list': appliances_list
        }

# Main content area
if st.session_state.calculated and st.session_state.energy_data:
    data = st.session_state.energy_data
    
    # User info display
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="info-box">
            <h4>👤 Personal Details</h4>
            <p><strong>Name:</strong> {data['name']}</p>
            <p><strong>Age:</strong> {data['age']}</p>
            <p><strong>Location:</strong> {data['area']}, {data['city']}</p>
            <p><strong>Housing:</strong> {data['facility']} {data['flat_tenement']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="info-box">
            <h4>🏠 Base Consumption</h4>
            <p><strong>Housing Type:</strong> {data['facility']}</p>
            <p><strong>Base Energy:</strong> {data['base_energy']:.1f} kWh/day</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="info-box">
            <h4>🔌 Appliances</h4>
            <p><strong>Additional Energy:</strong> {data['appliances_energy']:.1f} kWh/day</p>
            <p><strong>Appliances:</strong> {', '.join(data['appliances_list']) if data['appliances_list'] else 'None'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Energy consumption metrics
    st.header("📊 Energy Consumption Analysis")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Daily Consumption",
            value=f"{data['total_energy']:.1f} kWh",
            delta=f"{data['appliances_energy']:.1f} kWh from appliances"
        )
    
    with col2:
        st.metric(
            label="Monthly Consumption",
            value=f"{data['total_energy'] * 30:.1f} kWh",
            delta=f"~₹{data['total_energy'] * 30 * 6:.0f} cost"
        )
    
    with col3:
        st.metric(
            label="Annual Consumption",
            value=f"{data['total_energy'] * 365:.1f} kWh",
            delta=f"~₹{data['total_energy'] * 365 * 6:.0f} cost"
        )
    
    with col4:
        st.metric(
            label="Carbon Footprint",
            value=f"{data['total_energy'] * 365 * 0.82:.1f} kg CO₂",
            delta="per year"
        )
    
    # Charts
    st.header("📈 Visual Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Energy breakdown pie chart
        labels = ['Base Consumption', 'Appliances']
        values = [data['base_energy'], data['appliances_energy']]
        colors = ['#1f77b4', '#ff7f0e']
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            marker_colors=colors
        )])
        
        fig_pie.update_layout(
            title="Energy Consumption Breakdown",
            title_x=0.5,
            font=dict(size=14),
            height=400
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Monthly projection bar chart
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        monthly_consumption = [data['total_energy'] * 30] * 12
        
        fig_bar = go.Figure(data=[
            go.Bar(
                x=months,
                y=monthly_consumption,
                marker_color='#1f77b4',
                text=[f"{val:.1f} kWh" for val in monthly_consumption],
                textposition='auto'
            )
        ])
        
        fig_bar.update_layout(
            title="Monthly Energy Consumption Projection",
            title_x=0.5,
            xaxis_title="Month",
            yaxis_title="Energy (kWh)",
            font=dict(size=14),
            height=400
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Comparison chart
    st.header("📊 Comparison with Standard Consumption")
    
    # Create comparison data
    comparison_data = {
        'Category': ['Your Consumption', 'Average 1BHK', 'Average 2BHK', 'Average 3BHK'],
        'Daily kWh': [data['total_energy'], 4, 6, 8],
        'Monthly Cost (₹)': [data['total_energy'] * 30 * 6, 4 * 30 * 6, 6 * 30 * 6, 8 * 30 * 6]
    }
    
    df_comparison = pd.DataFrame(comparison_data)
    
    fig_comparison = px.bar(
        df_comparison,
        x='Category',
        y='Daily kWh',
        color='Category',
        title="Energy Consumption Comparison",
        text='Daily kWh'
    )
    
    fig_comparison.update_layout(
        title_x=0.5,
        font=dict(size=14),
        height=400,
        showlegend=False
    )
    
    fig_comparison.update_traces(texttemplate='%{text:.1f} kWh', textposition='outside')
    
    st.plotly_chart(fig_comparison, use_container_width=True)
    
    # Energy saving tips
    st.header("💡 Energy Saving Tips")
    
    tips = [
        "🌡️ Set AC temperature to 24°C for optimal energy efficiency",
        "🔌 Unplug electronics when not in use to avoid phantom loads",
        "💡 Switch to LED bulbs - they use 75% less energy than incandescent",
        "🌞 Use natural light during the day to reduce lighting costs",
        "🚿 Take shorter showers to reduce water heating energy",
        "🏠 Ensure proper insulation to maintain temperature efficiently",
        "⚡ Use appliances during off-peak hours for lower electricity rates",
        "🔄 Regular maintenance of appliances improves energy efficiency"
    ]
    
    col1, col2 = st.columns(2)
    
    for i, tip in enumerate(tips):
        if i % 2 == 0:
            col1.markdown(f"- {tip}")
        else:
            col2.markdown(f"- {tip}")
    
    # Export data option
    st.header("📥 Export Your Data")
    
    export_data = {
        'Parameter': ['Name', 'Age', 'City', 'Area', 'Housing Type', 'Configuration', 
                     'Base Energy (kWh/day)', 'Appliances Energy (kWh/day)', 
                     'Total Energy (kWh/day)', 'Monthly Cost (₹)', 'Annual Cost (₹)'],
        'Value': [data['name'], data['age'], data['city'], data['area'], 
                 data['flat_tenement'], data['facility'], data['base_energy'],
                 data['appliances_energy'], data['total_energy'],
                 data['total_energy'] * 30 * 6, data['total_energy'] * 365 * 6]
    }
    
    df_export = pd.DataFrame(export_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="📊 Download Report (CSV)",
            data=df_export.to_csv(index=False),
            file_name=f"energy_report_{data['name'].replace(' ', '_')}.csv",
            mime="text/csv"
        )
    
    with col2:
        st.download_button(
            label="📋 Download Summary (TXT)",
            data=f"""Energy Consumption Report
========================
Name: {data['name']}
Location: {data['area']}, {data['city']}
Housing: {data['facility']} {data['flat_tenement']}

Daily Consumption: {data['total_energy']:.1f} kWh
Monthly Consumption: {data['total_energy'] * 30:.1f} kWh
Annual Consumption: {data['total_energy'] * 365:.1f} kWh

Estimated Monthly Cost: ₹{data['total_energy'] * 30 * 6:.0f}
Estimated Annual Cost: ₹{data['total_energy'] * 365 * 6:.0f}

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
""",
            file_name=f"energy_summary_{data['name'].replace(' ', '_')}.txt",
            mime="text/plain"
        )

else:
    # Welcome screen
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h2>Welcome to the Energy Consumption Calculator! 🏠⚡</h2>
        <p style="font-size: 1.2rem; color: #666;">
            Calculate your household energy consumption and get personalized insights 
            to help you save money and reduce your carbon footprint.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>📊 Detailed Analysis</h4>
            <p>Get comprehensive breakdown of your energy consumption with visual charts and graphs.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>💰 Cost Estimation</h4>
            <p>Calculate your monthly and annual electricity costs based on current rates.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4>🌱 Eco-Friendly Tips</h4>
            <p>Receive personalized recommendations to reduce your energy consumption.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem;">
        <p style="font-size: 1.1rem; color: #1f77b4;">
            👈 Please fill in your details in the sidebar to get started!
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
---
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>Energy Consumption Calculator | Built with ❤️ using Streamlit & Plotly</p>
    <p><small>💡 Tip: Regular monitoring of energy consumption helps in better resource management</small></p>
</div>
""", unsafe_allow_html=True)