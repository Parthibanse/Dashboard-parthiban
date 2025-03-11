import streamlit as st
import pandas as pd

# Load dataset
FILE_PATH = "/mnt/data/Workshop details.xlsx"
df = pd.read_excel(FILE_PATH)

# Ensure required columns exist
df = df[['Pincode', 'Latitude', 'Longitude', 'Channel', 'Body Shop', 'State']]

def get_nearest_pincodes(pincode, df, num_results=5):
    if pincode not in df['Pincode'].values:
        return df.head(num_results)
    
    target_row = df[df['Pincode'] == pincode].iloc[0]
    df['Distance'] = df.apply(lambda row: geodesic((target_row['Latitude'], target_row['Longitude']), 
                                                   (row['Latitude'], row['Longitude'])).km, axis=1)
    return df.sort_values('Distance').head(num_results)

def main():
    st.title("Workshop Locator Dashboard")
    
    pincode = st.text_input("Enter Pincode:")
    channel = st.selectbox("Select Channel:", ["All", "Arena", "Nexa"])
    bodyshop = st.selectbox("Body Shop:", ["All", "Yes", "No"])
    state = st.selectbox("Select State:", ["All"] + df['State'].dropna().unique().tolist())
    
    filtered_df = df.copy()
    if pincode:
        filtered_df = get_nearest_pincodes(int(pincode), df)
    if channel != "All":
        filtered_df = filtered_df[filtered_df['Channel'] == channel]
    if bodyshop != "All":
        filtered_df = filtered_df[filtered_df['Body Shop'] == bodyshop]
    if state != "All":
        filtered_df = filtered_df[filtered_df['State'] == state]
    
    if not filtered_df.empty:
        st.write("### Filtered Workshops")
        st.dataframe(filtered_df)
    else:
        st.warning("No results found for the selected filters.")
    
if __name__ == "__main__":
    main()
