import streamlit as st
import numpy as np
from calculator import calculate_steps, calculate_angle_factor  # Ensure these exist

def main():
    # Page configuration
    st.set_page_config(page_title="WGT Golf Calculator",
                       page_icon="🏌️🇵🇷",
                       layout="wide")

    # Header
    st.title("⛳WGT Golf Calculator")
    st.markdown(
        "Calculate adjusted distances for golf shots based on wind conditions and angle"
    )

    # Explanation
    with st.expander("How it works"):
        st.markdown("""
        This calculator adjusts your golf shot distance based on:
        
        1. **Distance** - The original distance to the target in yards
        2. **Wind Factor** - The strength of the wind (typically 1-20)
        3. **Shot Angle** - The angle of the shot in degrees around a circle
           - Visualized as a point on a circle where:
           - 0° (right side) has a factor of 1.0
           - 90° (top) has a factor of 0.1
           - 180° (left side) has a factor of 1.0
           - 270° (bottom) has a factor of 0.1
        4. **Wind Direction** - Either headwind (against you) or tailwind (behind you)
        
        ### Calculation Example:
        - **Step 1**: Distance (103) × Wind (15) = 1545
        - **Step 2**: Divisor (180) ÷ Angle Factor (1.0) = 180
        - **Step 3**: 1545 ÷ 180 = 8.58333
        - **Final Step**: 
            - For headwind: 103 + 8.58333 = 111.58333 yards
            - For tailwind: 103 - 8.58333 = 94.41667 yards
        """)

    # Create a form for user inputs
    with st.form("distance_calculator_form"):
        col1, col2 = st.columns(2)

        with col1:
            distance = st.number_input(
                "Distance to Target (yards)",
                min_value=0.0,
                value=103.0,
                step=1.0,
                help="Enter the distance to your target in yards")

            wind = st.number_input(
                "Wind",
                min_value=0.0,
                max_value=30.0,
                value=15.0,
                step=0.5,
                help="Enter the wind (strength of the wind)")

        with col2:
            angle = st.number_input(
                "Shot Angle (degrees)",
                min_value=0.0,
                max_value=359.0,
                value=0.0,
                step=1.0,
                help=
                "Enter the angle of your shot (0° = right side, 90° = top, 180° = left side, 270° = bottom)"
            )

            wind_direction = st.radio(
                "Wind Direction",
                options=["headwind", "tailwind"],
                index=0,
                help=
                "Select whether the wind is against you (headwind) or behind you (tailwind)"
            )

        submit_button = st.form_submit_button("Calculate")

    # Display a visual representation of the angle on a circle
    col1, col2 = st.columns([3, 1])
    with col1:
        # Create a circle visualization of the shot angle
        svg_width = 200
        svg_height = 200
        center_x = svg_width / 2
        center_y = svg_height / 2
        radius = 75

        angle_rad = np.radians(angle)

        # Calculate the endpoint of the line based on the angle
        x2 = center_x + radius * np.cos(angle_rad)
        y2 = center_y - radius * np.sin(
            angle_rad)  # Negative because SVG Y-axis is inverted

        # Call the proper angle factor calculation
        angle_factor = calculate_angle_factor(angle)

        # Draw the angle visualization using SVG
        svg_content = f"""
        <svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">
            <rect width="{svg_width}" height="{svg_height}" fill="#f5f5f5" />
            
            <!-- Circle -->
            <circle cx="{center_x}" cy="{center_y}" r="{radius}" fill="none" stroke="gray" stroke-width="1" />
            
            <!-- Horizontal and vertical axes -->
            <line x1="{center_x - radius}" y1="{center_y}" x2="{center_x + radius}" y2="{center_y}" stroke="gray" stroke-width="1" />
            <line x1="{center_x}" y1="{center_y - radius}" x2="{center_x}" y2="{center_y + radius}" stroke="gray" stroke-width="1" />
            
            <!-- Angle line -->
            <line x1="{center_x}" y1="{center_y}" x2="{x2}" y2="{y2}" stroke="blue" stroke-width="3" />
            
            <!-- Labels -->
            <text x="{center_x + radius + 10}" y="{center_y + 5}" fill="black">0° (1.0)</text>
            <text x="{center_x - 5}" y="{center_y - radius - 10}" fill="black">90° (0.1)</text>
            <text x="{center_x - radius - 35}" y="{center_y + 5}" fill="black">180° (1.0)</text>
            <text x="{center_x - 5}" y="{center_y + radius + 20}" fill="black">270° (0.1)</text>
            <text x="{x2 + (10 if x2 > center_x else -40)}" y="{y2 - 10}" fill="blue">{angle}° ({angle_factor:.2f})</text>
            
            <!-- Green markers at 0°, 90°, 180°, 270° -->
            <line x1="{center_x + radius + 2}" y1="{center_y}" x2="{center_x + radius + 8}" y2="{center_y}" stroke="green" stroke-width="3" />
            <line x1="{center_x}" y1="{center_y - radius - 2}" x2="{center_x}" y2="{center_y - radius - 8}" stroke="green" stroke-width="3" />
            <line x1="{center_x - radius - 2}" y1="{center_y}" x2="{center_x - radius - 8}" y2="{center_y}" stroke="green" stroke-width="3" />
            <line x1="{center_x}" y1="{center_y + radius + 2}" x2="{center_x}" y2="{center_y + radius + 8}" stroke="green" stroke-width="3" />
            
            <!-- Center point -->
            <circle cx="{center_x}" cy="{center_y}" r="5" fill="black" />
            
            <!-- Angle point -->
            <circle cx="{x2}" cy="{y2}" r="5" fill="blue" />
            
            <!-- Arc for angle visualization -->
            <path d="M {center_x + 50}, {center_y} A 50 50 0 {1 if angle > 180 else 0} {1 if angle > 180 else 0} {center_x + 50 * np.cos(angle_rad)}, {center_y - 50 * np.sin(angle_rad)}" 
                  fill="none" stroke="red" stroke-width="2" />
        </svg>
        """
        # Use HTML component to display SVG
        html_content = f'<div style="text-align: center;">{svg_content}</div>'
        st.components.v1.html(html_content, height=svg_height + 20)

    with col2:
        if wind_direction == "headwind":
            st.markdown("### Wind Direction")
            st.markdown("🏌️ → 💨")
            st.markdown("**Headwind**")
        else:
            st.markdown("### Wind Direction")
            st.markdown("💨 → 🏌️")
            st.markdown("**Tailwind**")

    # Calculate and display results if the form is submitted
    if submit_button:
        results = calculate_steps(distance, wind, angle, wind_direction)

        # Check for errors
        if "error" in results:
            st.error(results["error"])
        else:
            # Final result with emphasis
            st.markdown("---")
            adjusted_result = float(results['adjusted_distance'])
            st.success(
                f"### Adjusted Distance: {adjusted_result:.2f} yards")

            # Comparison with original
            adjusted_distance = float(results['adjusted_distance'])
            distance_float = float(distance)
            difference = abs(adjusted_distance - distance_float)
            percent_change = (difference / distance_float) * 100

            # Format the values as strings to avoid type issues
            adjusted_dist_str = f"{adjusted_distance:.2f}"
            distance_str = f"{distance_float:.2f}"

            st.info(f"""
            **Original Distance:** {distance_str} yards  
            **Adjustment:** {difference:.2f} yards ({percent_change:.1f}%)  
            **Adjusted Distance:** {adjusted_dist_str} yards
            """)

            # Subheader with author
            st.subheader("-𝘔𝘢𝘥𝘦 𝘣𝘺 𝘎𝘢𝘣𝘦⛳")
                    
if __name__ == "__main__":
    main()
