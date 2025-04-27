import nbformat
import sys

def extract_code_from_notebook(notebook_path, output_path=None):
    """
    Extract all code cells from a Jupyter notebook and save them to a file or print to console.
    
    Args:
        notebook_path (str): Path to the input .ipynb file
        output_path (str, optional): Path where to save the extracted code. If None, print to console.
    """
    # Load the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)
    
    # Extract code from all code cells
    code_blocks = []
    for cell in notebook.cells:
        if cell.cell_type == 'code':
            code_blocks.append(cell.source)
    
    # Join all code blocks with newlines between them
    all_code = '\n\n# ' + '-'*40 + '\n\n'.join(code_blocks)
    
    # Output the code
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(all_code)
        print(f"Code extracted to {output_path}")
    else:
        print(all_code)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_notebook_code.py notebook.ipynb [output.py]")
        sys.exit(1)
    
    notebook_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    extract_code_from_notebook(notebook_path, output_path)