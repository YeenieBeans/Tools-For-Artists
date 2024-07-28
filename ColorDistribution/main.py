import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from sklearn.cluster import KMeans
from collections import Counter
import cv2

st.title('Color Distribution Tool')

uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    img = io.imread(uploaded_file)
    st.image(img, caption='Uploaded Image', use_column_width=True)
    num_colors = st.slider("Number of Colors", 1, 20, 5)
    sensitivity = st.selectbox("Color Sensitivity", ['Very Low', 'Low', 'Medium', 'High', 'Very High'])
    sensitivity_dict = {'Very Low': 0, 'Low': 1, 'Medium': 2, 'High': 3, 'Very High': 4}

    def get_colors(image, num_colors, sensitivity):
        print(f"Original image shape: {image.shape}")
        if len(image.shape) == 2:
            # Grayscale image
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        elif image.shape[2] == 4:
            # Image with alpha channel
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)

        resized_image = cv2.resize(image, (600, 400))
        print(f"Resized image shape: {resized_image.shape}")

        # Flatten the image
        resized_image = resized_image.reshape((resized_image.shape[0] * resized_image.shape[1], 3))
        print(f"Reshaped image shape: {resized_image.shape}")

        kmeans = KMeans(n_clusters=num_colors, n_init=10)
        kmeans.fit(resized_image)
        cluster_centers = kmeans.cluster_centers_
        labels = kmeans.labels_
        counts = Counter(labels)
        colors = [cluster_centers[i] for i in counts.keys()]

        hex_colors = ['#%02x%02x%02x' % (int(color[0]), int(color[1]), int(color[2])) for color in colors]

        merged_colors, merged_counts = merge_similar_colors(hex_colors, counts, sensitivity)

        return merged_colors, merged_counts

    def merge_similar_colors(hex_colors, counts, sensitivity):
        def is_similar_color(c1, c2, threshold):
            return all(abs(int(c1[i:i+2], 16) - int(c2[i:i+2], 16)) <= threshold for i in (1, 3, 5))

        thresholds = [10, 20, 30, 40, 50]
        threshold = thresholds[sensitivity]

        merged_colors = []
        merged_counts = []

        for i, color in enumerate(hex_colors):
            if not merged_colors:
                merged_colors.append(color)
                merged_counts.append(counts[i])
            else:
                merged = False
                for j, merged_color in enumerate(merged_colors):
                    if is_similar_color(color, merged_color, threshold):
                        merged_counts[j] += counts[i]
                        merged = True
                        break
                if not merged:
                    merged_colors.append(color)
                    merged_counts.append(counts[i])

        return merged_colors, merged_counts

    def get_text_color(hex_color):
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        luminance = 0.299 * r + 0.587 * g + 0.114 * b
        return '#000000' if luminance > 186 else '#FFFFFF'

    def plot_colors(hex_colors, counts):
        total = sum(counts)
        percentages = [count / total for count in counts]

        sorted_indices = sorted(range(len(percentages)), key=lambda k: percentages[k], reverse=True)
        hex_colors = [hex_colors[i] for i in sorted_indices]
        percentages = [percentages[i] for i in sorted_indices]

        fig, ax = plt.subplots(figsize=(15, 5))

        start = 0
        for hex_color, percentage in zip(hex_colors, percentages):
            ax.barh(['Colors'], percentage, color=hex_color, edgecolor='white', left=start, height=0.5)
            text_x = start + percentage / 2
            text_color = get_text_color(hex_color)
            ax.text(text_x, 0, f'{hex_color}\n{int(percentage*100)}%', ha='center', va='center', rotation=45, fontsize=10, color=text_color)
            start += percentage

        ax.set_xlim(0, 1)
        ax.axis('off')
        st.pyplot(fig)

    merged_colors, merged_counts = get_colors(img, num_colors, sensitivity_dict[sensitivity])
    plot_colors(merged_colors, merged_counts)
