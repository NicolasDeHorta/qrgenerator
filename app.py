import streamlit as st
from io import BytesIO
from generate_qr import generate_qr_code, QRCodeData, add_logo, add_bottom_text


st.write("Generate your QR code!")

col1, col2 = st.columns(2)


with col1:
    st.text_input("Enter the text to encode in the QR code:", key="qr_text", value="https://www.duckfoo.dev")
    if st.checkbox("Show bottom text", key="show_bottom_text"):
        st.text_input("Text to be shown below the QR code", key="bottom_text", value="Your text here")
    st.slider("Border width", key="border_width", min_value=1, max_value=10, value=4)
    st.slider("Box size", key="box_size", min_value=1, max_value=50, value=20)
    st.color_picker("Fill color", key="fill_color", value="#000000")
    st.color_picker("Background color", key="back_color", value="#FFFFFF")
    if st.checkbox("Add logo in the middle", key="add_logo"):
        logo_file = st.file_uploader("Add logo (PNG)", type=["png"])


with col2:
    # if st.button("Generate!", disabled=not st.session_state.get("qr_text")):
    qr_data = QRCodeData(
        border_width=st.session_state.border_width,
        box_size=st.session_state.box_size,
        text=st.session_state.qr_text,
        fill_color=st.session_state.fill_color,
        back_color=st.session_state.back_color
    )

    img = generate_qr_code(qr_data=qr_data)
    if st.session_state.add_logo:
        img = add_logo(img, logo_file, bg_color=qr_data.back_color) if logo_file else img
    
    if st.session_state.show_bottom_text:
        img = add_bottom_text(img, bg_color=qr_data.back_color, fill_color=st.session_state.fill_color, text=st.session_state.bottom_text)

    st.image(img)

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    
    st.download_button(
        label="Download QR code",
        data=buffer,
        file_name="QR_download.png",
        mime="image/png"
    )   