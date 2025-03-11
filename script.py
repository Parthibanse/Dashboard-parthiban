import streamlit as st
import pandas as pd

# Load the dataset
FILE_PATH = "Workshop details.xlsx"
try:
    df = pd.read_excel(FILE_PATH)
except FileNotFoundError:
    st.error("Error: The specified file was not found. Please upload the correct file.")
    st.stop()
except Exception as e:
    st.error(f"Error loading the file: {e}")
    st.stop()

# Function to find nearest pincodes
def get_nearest_pincodes(pincode, df, num_results=5):
    if pincode not in df["Pincode"].values:
        return df.head(num_results)
    return df[df["Pincode"] == pincode].head(num_results)

# Streamlit UI
def main():
    st.title("Workshop Dashboard")
    
    if df.empty:
        st.warning("No data available. Please check the uploaded file.")
        return
    
    # Search by Pincode
    pincode = st.text_input("Enter Pincode:")
    
    # Filters
    channels = df["Channel"].dropna().unique().tolist()
    channel = st.selectbox("Select Channel:", ["All"] + channels)
    
    bodyshops = df["Body Shop"].dropna().unique().tolist()
    bodyshop = st.selectbox("Body Shop:", ["All"] + bodyshops)
    
    states = df["State"].dropna().unique().tolist()
    state = st.selectbox("Select State:", ["All"] + states)
    
    # Filter data based on inputs
    filtered_df = df.copy()
    if pincode:
        filtered_df = get_nearest_pincodes(pincode, df)
    if channel != "All":
        filtered_df = filtered_df[filtered_df["Channel"] == channel]
    if bodyshop != "All":
        filtered_df = filtered_df[filtered_df["Body Shop"] == bodyshop]
    if state != "All":
        filtered_df = filtered_df[filtered_df["State"] == state]
    
    # Display filtered data
    if not filtered_df.empty:
        st.write("### Filtered Workshops")
        st.dataframe(filtered_df)
    else:
        st.warning("No results found for the selected filters.")

if __name__ == "__main__":
    main()
