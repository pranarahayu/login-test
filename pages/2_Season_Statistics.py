import streamlit as st
from menu import menu
from streamlit_image_coordinates import streamlit_image_coordinates

menu()
st.title("This page is available to all users")
st.markdown(f"You are currently logged in")

'''
coor = []
value = streamlit_image_coordinates('./data/lapangkosong2.jpg', width=617.65, height=400, key="local",)
coor.append(value)
st.write(value)
st.write(coor)
'''
with Image.open('./data/lapangkosong2.jpg') as img:
    draw = ImageDraw.Draw(img)

    # Draw an ellipse at each coordinate in points
    for point in st.session_state["points"]:
        coords = get_ellipse_coords(point)
        draw.ellipse(coords, fill="red")

    value = streamlit_image_coordinates(img, key="pil")

    if value is not None:
        point = value["x"], value["y"]

        if point not in st.session_state["points"]:
            st.session_state["points"].append(point)
            st.experimental_rerun()
