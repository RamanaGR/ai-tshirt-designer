import streamlit as st
from PIL import Image, ImageOps

st.set_page_config(page_title="AI T-Shirt Designer", layout="centered")

# ===============================
# 🎨 Branding Header with Logo
# ===============================

col1, col2 = st.columns([1, 5])
with col1:
    try:
        st.image("assets/logo.png", width=80)
    except Exception:
        st.markdown(" ")
with col2:
    st.markdown("<h1 style='margin-bottom: 0;'>AI-Powered T-Shirt Designer</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: gray; font-style: italic;'>MIT 588 · Personalized E-Commerce Platform</p>", unsafe_allow_html=True)

st.markdown("---")




# Sidebar Inputs
st.sidebar.header("🛠️ Customize Your T-Shirt")
tshirt_type = st.sidebar.selectbox("Choose T-Shirt Style", ["Round Neck", "V-Neck", "Polo", "Hoodie"])
color = st.sidebar.color_picker("Pick a Color", "#ffffff")
uploaded_img = st.sidebar.file_uploader("Upload Your Design", type=["jpg", "jpeg", "png"])
size = st.sidebar.radio("Select Size", ["S", "M", "L", "XL"])

st.subheader("👕 T-Shirt Preview")

# Map styles to base shirt images
style_map = {
    "Round Neck": "assets/round_neck.png",
    "V-Neck": "assets/v_neck.png",
    "Polo": "assets/polo.png",
    "Hoodie": "assets/hoodie.png"
}

# Preview uploaded design
if uploaded_img:
    user_design = Image.open(uploaded_img).convert("RGBA")
    st.image(user_design, caption="Uploaded Design", use_container_width=True)
else:
    st.info("Upload a design to generate preview.")

# Generate AI Preview
if st.button("Generate AI Preview"):
    if not uploaded_img:
        st.warning("Please upload a design to continue.")
    else:
        # Load and color the base shirt
        tshirt_base = Image.open(style_map[tshirt_type]).convert("RGBA")
        color_overlay = Image.new("RGBA", tshirt_base.size, color)
        colored_shirt = Image.blend(tshirt_base, color_overlay, alpha=0.4)

        # Get original design
        design = Image.open(uploaded_img).convert("RGBA")
        shirt_width, shirt_height = colored_shirt.size

        # Set dynamic limits based on shirt type
        if tshirt_type == "Hoodie":
            max_width = int(shirt_width * 0.55)
            max_height = int(shirt_height * 0.35)
            top_offset = -60
        else:
            max_width = int(shirt_width * 0.65)
            max_height = int(shirt_height * 0.45)
            top_offset = {
                "Round Neck": 50,
                "V-Neck": 80,
                "Polo": 80
            }.get(tshirt_type, 70)

        # Maintain aspect ratio
        design_ratio = design.width / design.height
        if max_width / design_ratio <= max_height:
            new_width = max_width
            new_height = int(max_width / design_ratio)
        else:
            new_height = max_height
            new_width = int(max_height * design_ratio)

        design_resized = design.resize((new_width, new_height), Image.LANCZOS)

        # Apply transparency
        alpha = design_resized.split()[3].point(lambda p: int(p * 0.75))
        design_resized.putalpha(alpha)

        # Positioning
        x_center = (shirt_width - new_width) // 2
        y_center = ((shirt_height - new_height) // 2) + top_offset

        # Final image composition
        final_preview = colored_shirt.copy()
        final_preview.paste(design_resized, (x_center, y_center), design_resized)

        # Show output
        st.success(f"✅ AI Preview Generated ({tshirt_type})")
        st.image(final_preview, caption="AI-Generated T-Shirt", use_container_width=True)
# ===============================
# 📘 Footer
# ===============================
st.markdown("""
<hr style="margin-top: 40px; margin-bottom: 10px;">

<div style='text-align: center; font-size: 0.9em; color: grey'>
    Designed as part of <b>MIT 588: Software Development and Management</b><br>
    Developed by Team Aistitch · June 2025
</div>
""", unsafe_allow_html=True)