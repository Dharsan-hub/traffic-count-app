import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load or create a CSV file to store data
def load_data():
    try:
        df = pd.read_csv('traffic_counts.csv')
        df['Time'] = pd.to_datetime(df['Time'])  # Ensure 'Time' column is datetime type
        return df
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Date', 'Time', 'Cars', 'Bicycles', 'Pedestrians'])
        df.to_csv('traffic_counts.csv', index=False)
        return df

# Add a new entry to the CSV file
def add_entry(cars, bicycles, pedestrians):
    df = load_data()
    new_entry = pd.DataFrame({
        'Date': [datetime.now().strftime('%Y-%m-%d')],
        'Time': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],  # Full datetime format
        'Cars': [cars],
        'Bicycles': [bicycles],
        'Pedestrians': [pedestrians]
    })
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv('traffic_counts.csv', index=False)
    st.success('Data recorded successfully!')

# Main app function
def main():
    st.title("Traffic Count Study App")

    # Input fields for user to enter counts
    st.header("Enter Traffic Counts")
    cars = st.number_input('Number of Cars', min_value=0, value=0, step=1)
    bicycles = st.number_input('Number of Bicycles', min_value=0, value=0, step=1)
    pedestrians = st.number_input('Number of Pedestrians', min_value=0, value=0, step=1)

    if st.button("Record Data"):
        add_entry(cars, bicycles, pedestrians)

    st.header("Traffic Data Overview")
    df = load_data()
    if not df.empty:
        st.write(df)

        # Display summary charts
        st.subheader("Traffic Counts Over Time")

        # Plotting
        df['Time'] = pd.to_datetime(df['Time'])  # Ensure 'Time' is in datetime format
        df_sorted = df.sort_values(by='Time')  # Sort by time to ensure the plot is chronological

        fig, ax = plt.subplots(figsize=(10, 5))
        df_sorted.set_index('Time')[['Cars', 'Bicycles', 'Pedestrians']].plot(ax=ax)
        plt.xticks(rotation=45)
        plt.title('Traffic Counts Throughout the Day')
        plt.xlabel('Time')
        plt.ylabel('Count')
        st.pyplot(fig)

if __name__ == "__main__":
    main()
