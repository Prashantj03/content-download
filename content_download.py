import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import os

# Function to download the file from the provided URL
def download_file():
    url = url_entry.get()  # Get URL from user input
    if not url:
        messagebox.showerror("Error", "Please enter a valid URL!")
        return

    try:
        # Send a GET request to the URL
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check for HTTP errors
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Download Error", f"Failed to download: {e}")
        return

    # Ask user where to save the file
    save_path = filedialog.asksaveasfilename(
        defaultextension=os.path.splitext(url)[1], 
        filetypes=[("All Files", "*.*")], 
        initialfile=os.path.basename(url)
    )
    
    if not save_path:  # If the user cancels the file save dialog
        return

    # Write the content of the response to the specified file path
    try:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        messagebox.showinfo("Success", f"File downloaded successfully!\nSaved to: {save_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save file: {e}")

# Create the main GUI window
root = tk.Tk()
root.title("File Downloader")

# Create a label and entry field for the URL
tk.Label(root, text="Enter File URL:").pack(pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Create a download button
download_button = tk.Button(root, text="Download", command=download_file)
download_button.pack(pady=20)

# Start the main loop of the GUI
root.mainloop()
