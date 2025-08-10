import streamlit as st
from fpdf import FPDF
import matplotlib.pyplot as plt
from io import BytesIO
import tempfile
import os

# Area lists
areas = {
    "Ahmedabad": [
        "Bopal", "South Bopal", "Ambli", "Shilaj", "Gota", "Chandkheda", "Motera", "Sabarmati",
        "Paldi", "Maninagar", "Isanpur", "Naroda", "Nikol", "Vastral", "Ghodasar", "Vejalpur",
        "Prahladnagar", "Satellite", "Bodakdev", "Thaltej", "Jodhpur", "Memnagar", "Navrangpura",
        "Ellis Bridge", "CG Road", "Naranpura", "Ranip", "Shahibaug", "Asarwa", "Meghaninagar",
        "Behrampura", "Kalupur", "Jamalpur", "Saraspur", "Khokhra", "Amraiwadi", "Rakhial",
        "Vasna", "Jivraj Park", "Gulbai Tekra"
    ],
    "Gandhinagar": [
        "Sector 1", "Sector 2", "Sector 3", "Sector 4", "Sector 5", "Sector 6", "Sector 7",
        "Sector 8", "Sector 9", "Sector 10", "Sector 11", "Sector 12", "Sector 13", "Sector 14",
        "Sector 15", "Sector 16", "Sector 17", "Sector 18", "Sector 19", "Sector 20", "Sector 21",
        "Sector 22", "Sector 23", "Sector 24", "Sector 25", "Sector 26", "Sector 27", "Sector 28",
        "Sector 29", "Sector 30"
    ],
    "Pune": [
        "Baner", "Pashan", "Kothrud", "Bavdhan", "Hinjewadi", "Wakad", "Balewadi", "Aundh", "Sus",
        "Rahatani", "Tathawade", "Punawale", "Kharadi", "Vadgaon Sheri", "Hadapsar", "Mundhwa",
        "Koregaon Park", "Kalyani Nagar", "Wagholi", "Chandan Nagar", "Manjari", "Vishrantwadi",
        "Dhanori", "Lohegaon"
    ]
}

# Price ranges per area
price_ranges = {
    "Ahmedabad": {
        "Bopal": 6500, "South Bopal": 6800, "Ambli": 9500, "Shilaj": 7200, "Gota": 6200,
        "Chandkheda": 5800, "Motera": 6000, "Sabarmati": 5500, "Paldi": 8000, "Maninagar": 6000,
        "Isanpur": 5200, "Naroda": 4800, "Nikol": 4900, "Vastral": 4700, "Ghodasar": 5300,
        "Vejalpur": 6200, "Prahladnagar": 9000, "Satellite": 9200, "Bodakdev": 9500, "Thaltej": 9300,
        "Jodhpur": 8800, "Memnagar": 8000, "Navrangpura": 9000, "Ellis Bridge": 9500, "CG Road": 10000,
        "Naranpura": 7800, "Ranip": 5900, "Shahibaug": 8500, "Asarwa": 4800, "Meghaninagar": 4900,
        "Behrampura": 4600, "Kalupur": 5000, "Jamalpur": 4700, "Saraspur": 4800, "Khokhra": 5300,
        "Amraiwadi": 4900, "Rakhial": 4700, "Vasna": 7000, "Jivraj Park": 6800, "Gulbai Tekra": 8500
    },
    "Gandhinagar": {
        "Sector 1": 4500, "Sector 2": 4500, "Sector 3": 4500, "Sector 4": 4600, "Sector 5": 4700,
        "Sector 6": 4800, "Sector 7": 4900, "Sector 8": 5000, "Sector 9": 5100, "Sector 10": 5200,
        "Sector 11": 5300, "Sector 12": 5400, "Sector 13": 5500, "Sector 14": 5600, "Sector 15": 5700,
        "Sector 16": 5800, "Sector 17": 5900, "Sector 18": 6000, "Sector 19": 6100, "Sector 20": 6200,
        "Sector 21": 6300, "Sector 22": 6400, "Sector 23": 6500, "Sector 24": 6600, "Sector 25": 6700,
        "Sector 26": 6800, "Sector 27": 6900, "Sector 28": 7000, "Sector 29": 7100, "Sector 30": 7200
    },
    "Pune": {
        "Baner": 9500, "Pashan": 9000, "Kothrud": 10000, "Bavdhan": 8800, "Hinjewadi": 7800,
        "Wakad": 8200, "Balewadi": 9000, "Aundh": 9500, "Sus": 8000, "Rahatani": 7500, "Tathawade": 7200,
        "Punawale": 7000, "Kharadi": 9200, "Vadgaon Sheri": 8200, "Hadapsar": 8500, "Mundhwa": 8400,
        "Koregaon Park": 12000, "Kalyani Nagar": 11500, "Wagholi": 6800, "Chandan Nagar": 8000,
        "Manjari": 6500, "Vishrantwadi": 7200, "Dhanori": 7000, "Lohegaon": 6900
    }
}

furnish_options = ["Fully Furnished", "Semi Furnished", "Unfurnished"]
amenities = ["Swimming Pool", "Garden", "Gym", "Secured", "Covered Parking", "Club House"]

st.set_page_config(page_title="Multi-City Valuation Tool", layout="centered")
st.title("ClearDeals Property Valuation Tool")

# Inputs
name = st.text_input("Your Name")
contact = st.text_input("Contact Number")
city = st.selectbox("City", list(areas.keys()))
area = st.selectbox("Area", areas[city])
furnishing = st.selectbox("Furnishing Level", furnish_options)
amenity_sel = st.multiselect("Amenities", amenities)
bhk = st.selectbox("Property Type / BHK", ["1 BHK", "2 BHK", "3 BHK", "Villa", "Commercial"])
size = st.number_input("Property Size (sq.ft.)", min_value=100, step=50)

# Valuation
if st.button("Generate Valuation Report"):
    rate = price_ranges[city][area]
    low = rate * 0.9
    avg = rate
    high = rate * 1.1

    val_low = low * size
    val_avg = avg * size
    val_high = high * size

    st.success(f"Estimated Value: Rs.{val_avg:,.0f}")
    st.write(f"Range: Rs.{val_low:,.0f} – Rs.{val_high:,.0f}")

    # Chart
    fig, ax = plt.subplots()
    ax.bar(["Lower", "Average", "Higher"], [val_low, val_avg, val_high], color=["#ff9999","#66b3ff","#99ff99"])
    ax.set_ylabel("Price (Rs.)")
    ax.set_title("Valuation Price Range")
    st.pyplot(fig)

    # PDF class with Arial font
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 14)
            self.cell(0, 10, "ClearDeals Property Valuation Report", ln=True, align="C")
            self.ln(5)
        def footer(self):
            self.set_y(-25)
            self.set_font("Arial", "", 8)
            self.multi_cell(0, 10, (
                "Disclaimer: This report is indicative based on market data as of Aug 2025. "
                "Please consult licensed valuers. Powered by ClearDeals"), align="C")

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8,
        f"Name: {name}\nContact: {contact}\nCity: {city}\nArea: {area}\n"
        f"BHK/Type: {bhk}\nFurnishing: {furnishing}\nAmenities: {', '.join(amenity_sel) if amenity_sel else 'None'}\n"
        f"Size (sq.ft.): {size}\n\nEstimated Value: Rs.{val_avg:,.0f}\nPrice Range: Rs.{val_low:,.0f} - Rs.{val_high:,.0f}"
    )

    # Save chart as image
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        tmp.write(buf.getbuffer())
        tmp_path = tmp.name

    pdf.image(tmp_path, x=20, w=170)
    os.remove(tmp_path)

    # Output PDF to bytes
    pdf_bytes = BytesIO()
    pdf_output = pdf.output(dest='S').encode('latin1')
    pdf_bytes.write(pdf_output)
    pdf_bytes.seek(0)

    # Download button
    st.download_button(
        label="📄 Download Report",
        data=pdf_bytes,
        file_name="valuation_report.pdf",
        mime="application/pdf"
    )
