# Install required libraries
!pip install streamlit transformers pillow colorthief

# Import libraries
import streamlit as st
from PIL import Image
from transformers import pipeline
from colorthief import ColorThief
import io

# Function to generate color combinations (Hugging Face model can be integrated)
def suggest_color_combinations(input_color, combination_style):
    # Here you can use any pre-trained model from Hugging Face
    # Example: model = pipeline('color-combination-generator')
    # color_combinations = model(input_color)

    # For now, we'll use example combinations based on style
    if combination_style == "Complementary":
        color_combinations = ['#FF5733', '#33FF57']
    elif combination_style == "Analogous":
        color_combinations = ['#FF5733', '#FFBD33', '#FF5733']
    elif combination_style == "Monochromatic":
        color_combinations = ['#FF5733', '#FF6F33', '#FF8633']
    else:
        color_combinations = ['#FF5733', '#33FF57', '#3357FF']  # Default example
    return color_combinations

# Generate images for the color combinations
def generate_color_images(color_combinations):
    images = []
    for color in color_combinations:
        img = Image.new('RGB', (100, 100), color)
        images.append(img)
    return images

# Streamlit App Interface
st.title("Color Combination Suggestion Bot")

# Color input or image upload
st.header("Input a Color or Upload an Image")

# Option to select input method
input_method = st.radio("Select Input Method", ("Pick a Color", "Upload an Image"))

# Choose combination style
combination_style = st.selectbox("Choose combination style", ["Complementary", "Analogous", "Monochromatic"])

if input_method == "Pick a Color":
    # Color Picker
    input_color = st.color_picker("Choose a color", "#FF0000")
    st.write(f"Selected Color: {input_color}")

    if st.button("Generate Combinations"):
        # Get color combinations
        combinations = suggest_color_combinations(input_color, combination_style)

        # Display suggested combinations
        st.subheader("Best Color Combinations:")
        for color in combinations:
            st.write(f"Color: {color}")

        # Generate and display images for the combinations
        images = generate_color_images(combinations)
        st.subheader("Color Combination Images:")
        for idx, img in enumerate(images):
            st.image(img, caption=f"Combination {idx+1}")

            # Download button for each image
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            byte_im = buf.getvalue()
            st.download_button(label=f"Download Image {idx+1}", data=byte_im, file_name=f'color_combination_{idx+1}.png')

elif input_method == "Upload an Image":
    # File uploader
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])

    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        st.image(img, caption='Uploaded Image', use_column_width=True)

        # Extract dominant color
        color_thief = ColorThief(uploaded_file)
        dominant_color = color_thief.get_color(quality=1)
        dominant_color_hex = '#{:02x}{:02x}{:02x}'.format(dominant_color[0], dominant_color[1], dominant_color[2])
        st.write(f"Dominant Color: {dominant_color_hex}")

        if st.button("Generate Combinations from Dominant Color"):
            # Get color combinations using the dominant color
            combinations = suggest_color_combinations(dominant_color_hex, combination_style)

            # Display suggested combinations
            st.subheader("Best Color Combinations:")
            for color in combinations:
                st.write(f"Color: {color}")

            # Generate and display images for the combinations
            images = generate_color_images(combinations)
            st.subheader("Color Combination Images:")
            for idx, img in enumerate(images):
                st.image(img, caption=f"Combination {idx+1}")

                # Download button for each image
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                byte_im = buf.getvalue()
                st.download_button(label=f"Download Image {idx+1}", data=byte_im, file_name=f'color_combination_{idx+1}.png')

# Color Theory Information
if st.checkbox("Learn about Color Theory"):
    st.write("""
        **Complementary Colors**: Colors opposite each other on the color wheel.
        **Analogous Colors**: Colors next to each other on the color wheel.
        **Monochromatic Colors**: Variations of a single color using different shades, tones, and tints.
    """)

# Feedback system
feedback = st.text_area("Provide feedback or suggestions")
if st.button("Submit Feedback"):
    st.write("Thank you for your feedback!")
