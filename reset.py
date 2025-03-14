import os


def rename_pdfs_to_numbers(directory):
    pdf_files = [f for f in os.listdir(directory) if f.endswith(".pdf")]
    for i, filename in enumerate(pdf_files):
        new_name = f"{i}.pdf"
        os.rename(os.path.join(directory, filename), os.path.join(directory, new_name))


# Example usage
if __name__ == "__main__":
    directory = input("Enter the directory containing PDFs: ")
    rename_pdfs_to_numbers(directory)
