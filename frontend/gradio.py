import gradio as gr

# Define the car models and CNN models
car_models = ["Honda Civic", "Honda Accord", "Honda City", "Honda CR-V", "Honda Jazz"]
cnn_models = ["VGG16", "ResNet50", "InceptionV3"]

# Functions to handle screen transitions
def go_to_homepage():
    return gr.update(visible=False), gr.update(visible=True)

def go_to_screen1():
    return gr.update(visible=False), gr.update(visible=True)

def go_to_screen2(car_model, model_chassis_number):
    # Check if both inputs are provided
    if not car_model or not model_chassis_number:
        return (
            gr.update(value="Please fill out all fields!", visible=True),
            gr.update(visible=False),
            gr.update(visible=False)
        )
    # Proceed to Screen 2
    return (
        gr.update(value="", visible=False),
        gr.update(visible=False),
        gr.update(visible=True)
    )

def process_images(uploaded_files, selected_model):
    # Check if files are uploaded
    if not uploaded_files:
        return (
            gr.update(value="Please upload at least one image!", visible=True),
            gr.update(visible=False),
            gr.update(value="Image Here", visible=True),
            gr.update(visible=False)
        )

    # For now, we'll just log the selected model and proceed
    print(f"Selected CNN Model: {selected_model}")

    # Proceed to Screen2b with a placeholder for images
    return (
        gr.update(value="", visible=False),
        gr.update(visible=False),
        gr.update(value="Image Here", visible=True),  # Placeholder instead of gallery
        gr.update(visible=True)
    )

def go_to_screen3_from2b():
    # Proceed to Screen 3 from Screen2b
    return (
        gr.update(visible=False),
        gr.update(visible=True)
    )

def complete_registration(driver_name, accident_description):
    # Check if both inputs are provided
    if not driver_name or not accident_description:
        return (
            gr.update(value="Please fill out all fields!", visible=True),
            gr.update(visible=False),
            gr.update(visible=False)
        )
    # Proceed to the final screen with success message
    return (
        gr.update(value="", visible=False),
        gr.update(visible=False),
        gr.update(visible=True)
    )

# CSS for centering the entire app on the screen and styling the placeholder
custom_css = """
.centered {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}
#placeholder-box {
    display: flex;
    justify-content: center;
    align-items: center;
    border: 2px dashed #cccccc;
    font-size: 24px;
    color: #cccccc;
    height: 300px;
    width: 100%;
    text-align: center;
    margin-top: 20px;
}
.error-message {
    color: red;
    margin-top: 10px;
}
"""

# UI layout with enhanced design, centered on the screen using CSS
with gr.Blocks(css=custom_css) as demo:
    # Homepage
    with gr.Row(visible=True, elem_id="homepage") as homepage_layout:
        with gr.Column(scale=1, min_width=400):
            gr.Markdown("# Car Crash Analyzer")
            gr.Markdown("Welcome to the Car Crash Analyzer app. Click the button below to proceed.")
            home_next_btn = gr.Button("Next", variant="primary")

    # Error message placeholders for different screens
    error_message_screen1 = gr.Textbox("", visible=False, interactive=False, label="Error")
    error_message_screen2 = gr.Textbox("", visible=False, interactive=False, label="Error")
    error_message_screen3 = gr.Textbox("", visible=False, interactive=False, label="Error")

    # Screen 1: Car Model Selection
    with gr.Row(visible=False, elem_id="screen1") as screen1_layout:
        with gr.Column(scale=1, min_width=400):
            gr.Markdown("### FIR Registration - Step 1")
            gr.Markdown("Please select the car model and enter the model or chassis number.")
            car_model = gr.Dropdown(choices=car_models, label="Select Car Model", interactive=True)
            model_chassis_number = gr.Textbox(
                label="Enter Model/Chassis Number",
                placeholder="e.g., 1234ABCD",
                interactive=True
            )
            next_btn1 = gr.Button("Next", variant="primary")
            error_message_screen1  # Display error below the button

    # Screen 2: Image Upload and CNN Model Selection
    with gr.Row(visible=False, elem_id="screen2") as screen2_layout:
        with gr.Column(scale=1, min_width=400):
            gr.Markdown("### FIR Registration - Step 2")
            gr.Markdown("Upload images related to the incident (you can upload multiple images).")
            file_upload = gr.File(
                label="Upload Images",
                file_types=["image"],
                file_count="multiple",
                interactive=True
            )
            # Dropdown for selecting a CNN model
            cnn_model = gr.Dropdown(choices=cnn_models, label="Select CNN Model for Processing", interactive=True)
            next_btn2 = gr.Button("Next", variant="primary")
            error_message_screen2  # Display error below the button

    # Screen 2b: Uploaded Images and Damage Details
    with gr.Row(visible=False, elem_id="screen2b") as screen2b_layout:
        with gr.Column(scale=1, min_width=400):
            gr.Markdown("### FIR Registration - Step 2a")
            placeholder_box = gr.HTML('<div id="placeholder-box">Image Here</div>')  # Placeholder box for images
            parts_damaged_text = gr.Markdown("**Part(s) damaged:** Front Bumper, Left Door")
            estimated_cost_text = gr.Markdown("**Estimated cost:** $1500")
            next_btn2b = gr.Button("Next", variant="primary")

    # Screen 3: Accident Details
    with gr.Row(visible=False, elem_id="screen3") as screen3_layout:
        with gr.Column(scale=1, min_width=400):
            gr.Markdown("### FIR Registration - Step 3")
            gr.Markdown("Provide details of the driver and describe the accident.")
            driver_name = gr.Textbox(
                label="Who was driving?",
                placeholder="Enter driver's name",
                interactive=True
            )
            accident_description = gr.Textbox(
                label="Description of the accident",
                placeholder="Describe what happened...",
                lines=3,
                interactive=True
            )
            next_btn3 = gr.Button("Next", variant="primary")
            error_message_screen3  # Display error below the button

    # Final Screen: FIR Registered
    with gr.Row(visible=False, elem_id="final_screen") as final_screen_layout:
        with gr.Column(scale=1, min_width=400):
            gr.Markdown("### FIR Registered")
            final_message = gr.Markdown("**Your FIR has been successfully registered. Thank you!**", visible=True)

    # Button actions for transitioning screens
    home_next_btn.click(
        go_to_screen1,
        inputs=[],
        outputs=[homepage_layout, screen1_layout]
    )

    next_btn1.click(
        go_to_screen2,
        inputs=[car_model, model_chassis_number], outputs=[error_message_screen1, screen1_layout, screen2_layout]
    )

    next_btn2.click(
        process_images,
        inputs=[file_upload, cnn_model],
        outputs=[error_message_screen2, screen2_layout, placeholder_box, screen2b_layout]
    )

    next_btn2b.click(
        go_to_screen3_from2b,
        inputs=[],
        outputs=[screen2b_layout, screen3_layout]
    )

    next_btn3.click(
        complete_registration,
        inputs=[driver_name, accident_description],
        outputs=[error_message_screen3, screen3_layout, final_screen_layout]
    )

# Launch the app with a shareable link
demo.launch(share=True)
