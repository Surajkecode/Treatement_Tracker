import pandas as pd
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from datetime import datetime
from PIL import Image, ImageTk


# Load and Save Data Functions
def load_data():
    try:
        df = pd.read_csv('treatments.csv')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['date', 'disease', 'symptoms', 'treatment', 'yoga'])
    return df


def save_data(df):
    df.to_csv('treatments.csv', index=False)


# Admin Functions
def add_treatment():
    disease = disease_entry.get()
    symptoms = symptoms_entry.get()
    treatment = treatment_entry.get()
    yoga = yoga_entry.get()

    if disease and symptoms and treatment and yoga:
        df = load_data()
        new_entry = {
            'date': datetime.today().strftime('%Y-%m-%d'),
            'disease': disease,
            'symptoms': symptoms,
            'treatment': treatment,
            'yoga': yoga
        }
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        save_data(df)
        messagebox.showinfo("Success", "उपचार यशस्वीरित्या जोडला गेला.", parent=root)
        clear_entries()
    else:
        messagebox.showerror("Error", "सर्व फील्ड भरलेले असले पाहिजेत.", parent=root)


def clear_entries():
    disease_entry.delete(0, tk.END)
    symptoms_entry.delete(0, tk.END)
    treatment_entry.delete(0, tk.END)
    yoga_entry.delete(0, tk.END)


# Patient Functions
def search_treatment():
    disease = search_entry.get()
    df = load_data()
    result = df[df['disease'].str.contains(disease, case=False)].sort_values(by='date', ascending=False)

    if not result.empty:
        date_options = ['All'] + result['date'].unique().tolist()
        date_var.set(date_options[0])  # Set 'All' as default
        date_menu['menu'].delete(0, 'end')
        for date in date_options:
            date_menu['menu'].add_command(label=date, command=tk._setit(date_var, date))
        result_label.config(text="तुम्हाला कोणती तारीख हवी आहे?")
    else:
        result_label.config(text="या आजारासाठी कोणताही उपचार सापडला नाही.")


def display_treatment_by_date():
    selected_date = date_var.get()
    disease = search_entry.get()
    df = load_data()

    if selected_date == "All":
        result = df[df['disease'].str.contains(disease, case=False)]
    else:
        result = df[(df['disease'].str.contains(disease, case=False)) & (df['date'] == selected_date)]

    if not result.empty:
        result_text = ""
        for index, row in result.iterrows():
            result_text += f"तारीख: {row['date']}\nआजार: {row['disease']}\nलक्षणे: {row['symptoms']}\nउपचार: {row['treatment']}\nयोगा: {row['yoga']}\n\n"
        result_label.config(text=result_text)
    else:
        result_label.config(text="या आजारासाठी कोणताही उपचार सापडला नाही.")


# Exporting to Excel
def export_to_excel():
    df = load_data()
    if df.empty:
        messagebox.showinfo("No Data", "निर्यात करण्यासाठी काहीही नाही.", parent=root)
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                             filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    if file_path:
        try:
            df.to_excel(file_path, index=False, engine='openpyxl')
            messagebox.showinfo("Exported", "उपचार यशस्वीरित्या Excel मध्ये निर्यात झाले.", parent=root)
        except Exception as e:
            messagebox.showerror("Error", f"Excel निर्यात करताना त्रुटी आली:\n{e}", parent=root)


# Zoom In/Out Functions
def zoom(event):
    scale = 1.1 if event.delta > 0 else 0.9
    scale_widgets(scale)


def scale_widgets(scale):
    for widget in root.winfo_children():
        widget_font = widget.cget("font")
        if widget_font:
            font_family, font_size = widget_font.split()[0], int(widget_font.split()[1])
            new_size = int(font_size * scale)
            widget.config(font=(font_family, new_size))


def key_zoom(event):
    if event.keysym in ['plus', 'KP_Add']:
        scale_widgets(1.1)
    elif event.keysym in ['minus', 'KP_Subtract']:
        scale_widgets(0.9)


# Tkinter GUI Setup
root = tk.Tk()
root.title("उपचार ट्रॅकर")
root.geometry("2560x1440")

current_font_size = 14  # Initial font size

# Background Image Setup
background_image = Image.open("doctor.jpg")
background_image = background_image.resize((2560, 1440), Image.LANCZOS)  # Use Image.LANCZOS directly
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

# Frame Setup
main_frame = tk.Frame(root, bg='#f0f0f0', bd=10)
main_frame.place(relx=0.5, rely=0.42, anchor=tk.CENTER)

# Admin Section
admin_frame = tk.Frame(main_frame, bg='#e1f5fe')
admin_frame.pack(pady=10, fill=tk.X)

tk.Label(admin_frame, text="प्रशासन: उपचार जोडा", bg='#e1f5fe', font=('Helvetica', 18, 'bold')).grid(row=0,
                                                                                                     columnspan=2,
                                                                                                     pady=10)

tk.Label(admin_frame, text="आजार:", bg='#e1f5fe', font=('Helvetica', 14)).grid(row=1, column=0, pady=5)
disease_entry = tk.Entry(admin_frame, font=('Helvetica', 14))
disease_entry.grid(row=1, column=1, pady=5)

tk.Label(admin_frame, text="लक्षणे:", bg='#e1f5fe', font=('Helvetica', 14)).grid(row=2, column=0, pady=5)
symptoms_entry = tk.Entry(admin_frame, font=('Helvetica', 14))
symptoms_entry.grid(row=2, column=1, pady=5)

tk.Label(admin_frame, text="उपचार:", bg='#e1f5fe', font=('Helvetica', 14)).grid(row=3, column=0, pady=5)
treatment_entry = tk.Entry(admin_frame, font=('Helvetica', 14))
treatment_entry.grid(row=3, column=1, pady=5)

tk.Label(admin_frame, text="योगा:", bg='#e1f5fe', font=('Helvetica', 14)).grid(row=4, column=0, pady=5)
yoga_entry = tk.Entry(admin_frame, font=('Helvetica', 14))
yoga_entry.grid(row=4, column=1, pady=5)

tk.Button(admin_frame, text="उपचार जोडा", command=add_treatment, bg='#0288d1', fg='white', font=('Helvetica', 14)).grid(
    row=5, columnspan=2, pady=15)

# Patient Section
patient_frame = tk.Frame(main_frame, bg='#e8f5e9')
patient_frame.pack(pady=10, fill=tk.X)

tk.Label(patient_frame, text="रुग्ण: उपचार शोधा", bg='#e8f5e9', font=('Helvetica', 18, 'bold')).grid(row=0,
                                                                                                     columnspan=2,
                                                                                                     pady=10)

tk.Label(patient_frame, text="आजार प्रविष्ट करा:", bg='#e8f5e9', font=('Helvetica', 14)).grid(row=1, column=0, pady=5)
search_entry = tk.Entry(patient_frame, font=('Helvetica', 14))
search_entry.grid(row=1, column=1, pady=5)

tk.Button(patient_frame, text="शोधा", command=search_treatment, bg='#388e3c', fg='white', font=('Helvetica', 14)).grid(
    row=2, columnspan=2, pady=5)

date_var = tk.StringVar()
date_menu = ttk.OptionMenu(patient_frame, date_var, '')
date_menu.grid(row=3, columnspan=2)

tk.Button(patient_frame, text="उपचार दाखवा", command=display_treatment_by_date, bg='#388e3c', fg='white',
          font=('Helvetica', 14)).grid(row=4, columnspan=2, pady=5)

result_label = tk.Label(patient_frame, text="", justify=tk.LEFT, bg='#e8f5e9', font=('Helvetica', 14))
result_label.grid(row=5, columnspan=2)

# Export to Excel Button
export_button = tk.Button(main_frame, text="सर्व उपचार Excel मध्ये निर्यात करा", command=export_to_excel, bg='#0288d1',
                          fg='white', font=('Helvetica', 14))
export_button.pack(pady=20)

# Bind zoom functions
root.bind('<MouseWheel>', zoom)
root.bind('<Key>', key_zoom)

root.mainloop()
