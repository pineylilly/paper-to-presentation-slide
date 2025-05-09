import os

def compile_slide(markdown_file_path: str, output_file_path: str) -> bool:
    """
    Compile the markdown file into a slide presentation.
    
    Args:
        markdown_file_path (str): Path to the input markdown file.
        output_file_path (str): Path to save the compiled slide presentation.
    """
    print("Compiling slide...")
    status = os.system(f"slidev export {markdown_file_path} --output {output_file_path}")
    if status != 0:
        print("Failed to compile the slide presentation.")
        return False
    print("Slide presentation compiled successfully.")
    return True