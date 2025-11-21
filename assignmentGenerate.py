import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import webbrowser

HANDWRITING_FONTS = {
    "Patrick Hand": "https://fonts.googleapis.com/css2?family=Patrick+Hand&display=swap",
    "Caveat": "https://fonts.googleapis.com/css2?family=Caveat&display=swap",
    "Indie Flower": "https://fonts.googleapis.com/css2?family=Indie+Flower&display=swap",
    "Kalam": "https://fonts.googleapis.com/css2?family=Kalam&display=swap",
    "Shadows Into Light": "https://fonts.googleapis.com/css2?family=Shadows+Into+Light&display=swap",
    "Covered By Your Grace": "https://fonts.googleapis.com/css2?family=Covered+By+Your+Grace&display=swap",
    "Just Another Hand": "https://fonts.googleapis.com/css2?family=Just+Another+Hand&display=swap",
    "Rock Salt": "https://fonts.googleapis.com/css2?family=Rock+Salt&display=swap",
    "Gloria Hallelujah": "https://fonts.googleapis.com/css2?family=Gloria+Hallelujah&display=swap"
}

def start_generation_thread(root, controls):
    controls["generate_btn"].config(state="disabled")
    
    params = {
        "assign_text": controls["assign_text_widget"].get("1.0", tk.END).strip(),
        "answer_text": controls["answer_text_widget"].get("1.0", tk.END).strip(),
        "font_name": controls["font_combobox"].get(),
        "font_size": controls["font_size_var"].get().strip(),
        "title_assignment": controls["assign_title_var"].get().strip() or "Assignment",
        "title_answer": controls["answer_title_var"].get().strip() or "Answer",
        "output_filename": controls["output_filename_var"].get().strip() or "handwritten.html",
        "status_var": controls["status_var"]
    }

    if not params["assign_text"] and not params["answer_text"]:
        messagebox.showwarning("Input Missing", "Please provide text for the assignment or answer.")
        controls["generate_btn"].config(state="normal")
        return

    threading.Thread(target=generate_html_worker, args=(params, controls), daemon=True).start()

def generate_html_worker(params, controls):
    try:
        status_var = params["status_var"]
        status_var.set("Generating HTML page...")

        font_name = params.get("font_name", "Patrick Hand")
        font_url = HANDWRITING_FONTS.get(font_name, HANDWRITING_FONTS["Patrick Hand"])
        
        try:
            font_size = int(params.get("font_size", 24))
        except ValueError:
            font_size = 24
            
        line_height = int(font_size * 1.66)
        padding_top = int(line_height * 2.25)
        
        font_family = font_name
        if "family=" in font_url:
            try:
                font_family = font_url.split("family=")[1].split("&")[0].replace("+", " ")
            except Exception:
                pass

        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{params['title_assignment']}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="{font_url}" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <style>
        body {{
            background-color: #e0e0e0;
            color: #000000;
            font-family: '{font_family}', cursive;
            font-size: {font_size}px;
            line-height: {line_height}px;
            margin: 0;
            padding: 40px;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(30px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .page-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 80px;
            animation: fadeIn 1s ease-out;
        }}
        .page {{
            position: relative;
            width: 21cm;
            min-height: 29.7cm;
            background-color: #fdfaf2;
            padding: {padding_top}px 2cm 2cm 2.5cm;
            background-image: linear-gradient(to bottom, #fdfaf2 {line_height - 2}px, #222222 {line_height - 2}px, #222222 {line_height}px);
            background-size: 100% {line_height}px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
            box-sizing: border-box;
        }}
        .page::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 2cm;
            bottom: 0;
            width: 2px;
            background-color: #ffb3b3;
        }}
        h1 {{
            font-size: 1.8em;
            line-height: {line_height * 2}px;
            margin-top: 0;
            margin-bottom: {line_height}px;
            text-align: center;
        }}
        p {{
            white-space: pre-wrap;
            margin: 0;
        }}
        .no-print {{
            text-align: center;
            margin-top: 2em;
            font-family: sans-serif;
            font-size: 14px;
            color: #888;
            display: flex;
            flex-direction: row;
            justify-content: center;
            flex-wrap: wrap;
            gap: 20px;
            padding-bottom: 2em;
        }}
        .btn {{
            background-color: #0078d4;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            font-family: sans-serif;
            text-decoration: none;
            transition: background-color 0.3s, transform 0.2s;
        }}
        .btn:hover {{
            background-color: #005a9e;
            transform: scale(1.05);
        }}
        @media print {{
            body {{
                background-color: white;
                padding: 0;
            }}
            .page-container {{
                display: block;
                gap: 0;
            }}
            .page {{
                margin: 0;
                padding: 1.5cm;
                padding-left: 2cm;
                box-shadow: none;
                page-break-after: always;
                background-image: linear-gradient(to bottom, white {line_height - 2}px, #222222 {line_height - 2}px, #222222 {line_height}px);
                background-size: 100% {line_height}px;
            }}
            .page:last-child {{
                page-break-after: auto;
            }}
            .no-print {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="page-container">
"""
        buttons_html = ""

        if params["assign_text"]:
            html_content += f"""
        <div id="page-assignment" class="page">
            <h1>{params['title_assignment']}</h1>
            <p>{params['assign_text']}</p>
        </div>
"""
            buttons_html += '<button class="btn" onclick="downloadPage(\'page-assignment\', \'assignment.jpg\', this)">Download Assignment JPG</button>'
        
        if params["answer_text"]:
            html_content += f"""
        <div id="page-answer" class="page">
            <h1>{params['title_answer']}</h1>
            <p>{params['answer_text']}</p>
        </div>
"""
            buttons_html += '<button class="btn" onclick="downloadPage(\'page-answer\', \'answer.jpg\', this)">Download Answer JPG</button>'

        html_content += f"""
    </div>
    <div class="no-print">
        {buttons_html}
        <p style="width: 100%;">Use your browser's print function (Ctrl+P) to print all pages.</p>
    </div>

    <script>
        function downloadPage(elementId, filename, btn) {{
            const element = document.getElementById(elementId);
            const originalText = btn.innerText;
            btn.innerText = "Generating...";
            
            html2canvas(element, {{
                scale: 2,
                useCORS: true, 
                allowTaint: true,
                backgroundColor: '#fdfaf2'
            }}).then(canvas => {{
                const link = document.createElement('a');
                link.download = filename;
                link.href = canvas.toDataURL('image/jpeg', 0.9);
                link.click();
                btn.innerText = originalText;
            }}).catch(err => {{
                console.error(err);
                alert("Error generating image. Please check console.");
                btn.innerText = originalText;
            }});
        }}
    </script>
</body>
</html>
"""
        output_dir = "handwritten_html"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, params["output_filename"])

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        webbrowser.open("file://" + os.path.abspath(output_path))
        
        status_var.set(f"Saved HTML page to '{output_path}'")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")
        status_var.set("An error occurred.")
    finally:
        controls["root"].after(0, lambda: controls["generate_btn"].config(state="normal"))

def main():
    root = tk.Tk()
    root.title("Handwritten HTML Page Generator")
    root.geometry("900x700")

    main_frame = ttk.Frame(root, padding=10)
    main_frame.pack(fill="both", expand=True)

    controls_frame = ttk.Frame(main_frame)
    controls_frame.pack(fill="x", pady=5)

    ttk.Label(controls_frame, text="Assignment Title:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
    assign_title_var = tk.StringVar(value="Assignment")
    ttk.Entry(controls_frame, textvariable=assign_title_var, width=40).grid(row=0, column=1, sticky="ew", padx=5, pady=2)

    ttk.Label(controls_frame, text="Answer Title:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
    answer_title_var = tk.StringVar(value="Answer")
    ttk.Entry(controls_frame, textvariable=answer_title_var, width=40).grid(row=1, column=1, sticky="ew", padx=5, pady=2)

    ttk.Label(controls_frame, text="Output Filename:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
    output_filename_var = tk.StringVar(value="handwritten.html")
    ttk.Entry(controls_frame, textvariable=output_filename_var, width=40).grid(row=2, column=1, sticky="ew", padx=5, pady=2)

    ttk.Label(controls_frame, text="Select Handwriting Font:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
    font_var = tk.StringVar(value="Patrick Hand")
    font_combobox = ttk.Combobox(controls_frame, textvariable=font_var, values=list(HANDWRITING_FONTS.keys()), state="readonly")
    font_combobox.grid(row=3, column=1, sticky="ew", padx=5, pady=2)

    ttk.Label(controls_frame, text="Font Size:").grid(row=4, column=0, sticky="w", padx=5, pady=2)
    font_size_var = tk.StringVar(value="24")
    font_size_spinbox = ttk.Spinbox(controls_frame, from_=12, to=72, textvariable=font_size_var, width=5)
    font_size_spinbox.grid(row=4, column=1, sticky="w", padx=5, pady=2)
    
    controls_frame.columnconfigure(1, weight=1)

    text_area_frame = ttk.Frame(main_frame)
    text_area_frame.pack(fill="both", expand=True, pady=10)
    text_area_frame.columnconfigure(0, weight=1)
    text_area_frame.columnconfigure(1, weight=1)
    text_area_frame.rowconfigure(1, weight=1)

    ttk.Label(text_area_frame, text="Assignment Text").grid(row=0, column=0, sticky="w", padx=5)
    assign_text_widget = scrolledtext.ScrolledText(text_area_frame, wrap="word", height=10, width=50)
    assign_text_widget.grid(row=1, column=0, sticky="nsew", padx=(0, 5))

    ttk.Label(text_area_frame, text="Answer Text").grid(row=0, column=1, sticky="w", padx=5)
    answer_text_widget = scrolledtext.ScrolledText(text_area_frame, wrap="word", height=10, width=50)
    answer_text_widget.grid(row=1, column=1, sticky="nsew", padx=(5, 0))

    bottom_frame = ttk.Frame(main_frame)
    bottom_frame.pack(fill="x", pady=5)

    status_var = tk.StringVar(value="Ready.")
    status_label = ttk.Label(bottom_frame, textvariable=status_var, anchor="w")
    status_label.pack(side="left", fill="x", expand=True)

    controls = {
        "root": root,
        "assign_text_widget": assign_text_widget,
        "answer_text_widget": answer_text_widget,
        "font_combobox": font_combobox,
        "font_size_var": font_size_var,
        "assign_title_var": assign_title_var,
        "answer_title_var": answer_title_var,
        "output_filename_var": output_filename_var,
        "status_var": status_var,
    }

    generate_btn = ttk.Button(bottom_frame, text="Generate HTML Page", command=lambda: start_generation_thread(root, controls))
    generate_btn.pack(side="right")
    controls["generate_btn"] = generate_btn

    root.mainloop()

if __name__ == "__main__":
        main()
