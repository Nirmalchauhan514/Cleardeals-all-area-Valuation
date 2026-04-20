import streamlit as st
from fpdf import FPDF
import matplotlib.pyplot as plt
from io import BytesIO
import tempfile
import os
import pandas as pd

# Load Excel
df = pd.read_excel("pune_rates.xlsx")
df.columns = df.columns.str.strip()

# Options
furnish_options = ["Fully Furnished", "Semi Furnished", "Unfurnished"]

amenities_list = [
    "Swimming Pool", "Gym", "Club House", "Covered Parking",
    "Banquet Hall", "Garden", "Children Play Area",
    "Senior Citizen Park", "Indoor Games", "Gazebo", "Cafeteria"
]

age_options = ["New Property", "0-5 years", "5-10 years", "10+ years"]
overlooking_options = ["Garden", "Pool", "Main Road", "Normal"]

st.set_page_config(page_title="Pune Valuation Tool", layout="centered")
st.title("Cleardeals Pune Smart Valuation Tool")

# Inputs
property_name = st.text_input("Property Name")
name = st.text_input("Client Name")
contact = st.text_input("Contact Number")

area = st.selectbox("Select Area", sorted(df["Area"].dropna().unique()))

furnishing = st.selectbox("Furnishing", furnish_options)
amenities = st.multiselect("Amenities", amenities_list)
age = st.selectbox("Property Age", age_options)
view = st.selectbox("Overlooking", overlooking_options)
bhk = st.selectbox("Property Type", ["1 BHK", "2 BHK", "3 BHK", "Villa", "Commercial"])
size = st.number_input("Property Size (sq.ft.)", min_value=100)

# Button
if st.button("Generate Premium Report"):

    if "Rate" not in df.columns:
        st.error("Excel must have 'Rate' column")
        st.stop()

    rate = df[df["Area"] == area]["Rate"].values[0]
    base_rate = rate

    # Furnishing Impact
    if furnishing == "Fully Furnished":
        base_rate += 500
    elif furnishing == "Semi Furnished":
        base_rate += 250

    # Age Impact
    if age == "New Property":
        base_rate += 300
    elif age == "0-5 years":
        base_rate += 200
    elif age == "5-10 years":
        base_rate += 100
    else:
        base_rate -= 200

    # Overlooking Impact
    if view == "Garden":
        base_rate += 200
    elif view == "Pool":
        base_rate += 250
    elif view == "Main Road":
        base_rate += 100

    # Amenities Impact
    for a in amenities:
        base_rate += 100  # flat impact

    # Final Values
    avg = base_rate
    low = avg * 0.9
    high = avg * 1.1

    val_low = low * size
    val_avg = avg * size
    val_high = high * size

    st.success(f"Estimated Value: Rs.{val_avg:,.0f}")
    st.write(f"Range: Rs.{val_low:,.0f} - Rs.{val_high:,.0f}")

    # Insight
    if avg < rate:
        insight = "Good Deal - Below Market"
    elif avg == rate:
        insight = "Fair Price - Market Standard"
    else:
        insight = "Premium Property - Above Market"

    st.info(f"Insight: {insight}")

    # 🔥 PREMIUM GRAPH (Updated)
    fig, ax = plt.subplots(figsize=(6,4))

    labels = ["Lower", "Average", "Higher"]
    values = [val_low, val_avg, val_high]
    colors = ["red", "gray", "blue"]

    bars = ax.bar(labels, values, color=colors)

    # Price labels in Lacs
    def format_lacs(value):
        return f"{round(value/100000, 1)} L"

    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2,
            height,
            format_lacs(height),
            ha='center',
            va='bottom',
            fontsize=9
        )

    ax.set_ylabel("Price (Lacs)")
    ax.set_title("Property Valuation Range")

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.grid(axis='y', linestyle='--', linewidth=0.5)

    plt.tight_layout()

    st.pyplot(fig)

    # PDF Class
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 14)
            self.cell(0, 10, f"{property_name} - Valuation Report", ln=True, align="C")

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)

    pdf.multi_cell(0, 8,
        f"Property Name: {property_name}\nClient: {name}\nContact: {contact}\nArea: {area}\nType: {bhk}\n"
        f"Furnishing: {furnishing}\nAge: {age}\nView: {view}\n"
        f"Amenities: {', '.join(amenities) if amenities else 'None'}\n"
        f"Size: {size} sq.ft.\n\n"
        f"Estimated Value: Rs.{val_avg:,.0f}\n"
        f"Price Range: Rs.{val_low:,.0f} - Rs.{val_high:,.0f}\n\n"
        f"Insight: {insight}"
    )

    # Save Graph
    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=300, bbox_inches='tight')
    buf.seek(0)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        tmp.write(buf.getbuffer())
        path = tmp.name

    pdf.image(path, x=20, w=170)
    os.remove(path)

    pdf_bytes = pdf.output(dest='S').encode('latin1')

    st.download_button(
        label="Download Report",
        data=pdf_bytes,
        file_name=f"{property_name}_valuation_report.pdf",
        mime="application/pdf"
    )