import os
from PIL import Image
import json

# Extract images from a PDF file
def extract_images_from_pdf(data_folder, weights_folder):
    # Create the output folder if it does not exist
    output_folder = os.path.join(data_folder, "images")
    tempout_folder = os.path.join(data_folder, "tempout")
    os.makedirs(output_folder, exist_ok=True)
    
    # Clear the tempout folder and output folder
    if not os.path.exists(tempout_folder):
        os.makedirs(tempout_folder)
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    os.system(f"rm -rf {output_folder}/*")
    
    # Execute command to run docker container
    status = os.system(f"docker run --rm --env-file deepfigures-local.env --volume {tempout_folder}:/work/host-output --volume {data_folder}:/work/host-input --volume {weights_folder}:/work/weights deepfigures-cpu:0.0.1 python3 /work/scripts/rundetection.py /work/host-output /work/host-input/paper.pdf")
    if status != 0:
        raise Exception("Error running docker container")
    
    # # Get directory path of result in tempout, which is the first directory in tempout
    result_dir = os.listdir(tempout_folder)[0]
    result_dir = os.path.join(tempout_folder, result_dir)
    
    print(f"Result directory: {result_dir}")
    
    # Strip name of paper images in result_dir/paper.pdf-images/ghostscript/dpi200 from paper.pdf-dpi200-pageXXXX.png to pageXXXX.png
    for file in os.listdir(f"{result_dir}/paper.pdf-images/ghostscript/dpi200"):
        if file == "_SUCCESS":
            os.remove(f"{result_dir}/paper.pdf-images/ghostscript/dpi200/_SUCCESS")
        if file.endswith(".png"):
            os.rename(f"{result_dir}/paper.pdf-images/ghostscript/dpi200/{file}", f"{result_dir}/paper.pdf-images/ghostscript/dpi200/{file.split('-')[-1]}")

    # Load JSON data from {result_dir}/paperdeepfigures-results.json
    with open(f"{result_dir}/paperdeepfigures-results.json") as f:
        data = json.load(f)
        
    # Extract figures and tables
    for figure in data.get("figures", []):
        page = figure["page"] + 1
        figure_type = figure["figure_type"]
        name = figure["name"]
        figure_boundary = figure["figure_boundary"]
        caption_boundary = figure["caption_boundary"]
        # boundary = figure["figure_boundary"]
        # Merge figure and caption boundaries
        boundary = {
            "x1": min(figure_boundary["x1"]*2, caption_boundary["x1"]*2 - 4),
            "y1": min(figure_boundary["y1"]*2, caption_boundary["y1"]*2 - 4),
            "x2": max(figure_boundary["x2"]*2, caption_boundary["x2"]*2 + 4),
            "y2": max(figure_boundary["y2"]*2, caption_boundary["y2"]*2 + 4),
        }

        # Construct the image file path
        img_path = f"{result_dir}/paper.pdf-images/ghostscript/dpi200/page{('0000' + str(page))[-4:]}.png"
        if not os.path.exists(img_path):
            print(f"Image for page {page} not found: {img_path}")
            continue

        # Open the image and crop based on the boundary
        with Image.open(img_path) as img:
            x1, y1, x2, y2 = map(int, [boundary["x1"], boundary["y1"], boundary["x2"], boundary["y2"]])
            cropped_img = img.crop((x1, y1, x2, y2))

            # Save the cropped image
            output_path = os.path.join(output_folder, f"{figure_type}_{name}.png")
            cropped_img.save(output_path)
            print(f"Saved: {output_path}")
            
            output_path = os.path.join(output_folder, "..", f"{figure_type}_{name}.png")
            cropped_img.save(output_path)
            print(f"Saved: {output_path}")
    
    # Create a txt file with description of figures and tables
    with open(os.path.join(output_folder, "../figures_and_tables.txt"), "w") as f:
        for figure in data.get("figures", []):
            figure_type = figure["figure_type"]
            name = figure["name"]
            caption_text = figure["caption_text"]
            f.write(f"{figure_type} {name} ({figure_type}_{name}.png): {caption_text}\n")
        print(f"Saved: {output_folder}/../figures_and_tables.txt")
    
    # Remove the tempout folder
    os.system(f"rm -rf {tempout_folder}/*")