import math
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from fpdf import FPDF
import csv
results = None
# Function: Calculate doping concentrations

def calculate_doping(ND, NA, ni):

    # Determine semiconductor type
    if ND > NA:
        material = "n-type"
        n = ((ND - NA) + math.sqrt((ND - NA)**2 + 4 * ni**2)) / 2
        p = ni**2 / n
        majority = "Electrons"
        minority = "Holes"

    elif NA > ND:
        material = "p-type"
        p = ((NA - ND) + math.sqrt((NA - ND)**2 + 4 * ni**2)) / 2
        n = ni**2 / p
        majority = "Holes"
        minority = "Electrons"

    else:
        material = "Intrinsic (pure)"
        n = p = ni
        majority = minority = "None"

    # Charge neutrality check
    neutrality = ND + p - NA - n

    # Doping strength level
    doping_strength = abs(ND - NA)
    if doping_strength < 1e12:
        doping_level = "Very Weak Doping"
    elif doping_strength < 1e15:
        doping_level = "Moderate Doping"
    else:
        doping_level = "Strong Doping"

    return material, n, p, majority, minority, neutrality, doping_level


# ================================================
# Tab 1: Perform calculation
# ================================================
def calculate():
    try:
        ND = float(entry_ND.get())
        NA = float(entry_NA.get())
        ni = float(entry_ni.get())

        global results
        results = calculate_doping(ND, NA, ni)

        material, n, p, majority, minority, neutrality, doping = results

        output.delete("1.0", tk.END)
        output.insert(tk.END,
            f"Material Type: {material}\n"
            f"Electron concentration n = {n:.3e}\n"
            f"Hole concentration p = {p:.3e}\n"
            f"Majority Carrier: {majority}\n"
            f"Minority Carrier: {minority}\n"
            f"Charge Neutrality: {neutrality:.3e}\n"
            f"Doping Strength: {doping}\n"
        )

    except ValueError:
        messagebox.showerror("Error", "Enter valid numeric values.")
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {e}")


# ================================================
# Tab 2: Plot graph
# ================================================
def plot_graph():
    if results is None:
        messagebox.showerror("Error", "Calculate first before plotting")
        return
    try:
        material, n, p, _, _, _, _ = results

        plt.bar(["Electrons (n)", "Holes (p)"], [n, p], color=["blue", "red"])
        plt.title(f"Carrier Concentrations — {material}")
        plt.ylabel("Concentration (cm⁻³)")
        plt.show()

    except NameError:
        messagebox.showerror("Error", "Calculate first before plotting")
    except Exception as e:
         messagebox.showerror("Error", f"Unexpected error: {e}")    


# ================================================
# Tab 3: Export PDF
# ================================================
def export_pdf():
    if results is None:
        messagebox.showerror("Error", "Calculate first before plotting")
        return
    try:
        material, n, p, majority, minority, neutrality, doping = results

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, "Doping Report", ln=1, align="C")
        pdf.ln(5)

        pdf.cell(0, 10, f"Material Type: {material}", ln=1)
        pdf.cell(0, 10, f"Electron concentration (n): {n:.3e}", ln=1)
        pdf.cell(0, 10, f"Hole concentration (p): {p:.3e}", ln=1)
        pdf.cell(0, 10, f"Majority Carrier: {majority}", ln=1)
        pdf.cell(0, 10, f"Minority Carrier: {minority}", ln=1)
        pdf.cell(0, 10, f"Charge Neutrality: {neutrality:.3e}", ln=1)
        pdf.cell(0, 10, f"Doping Strength: {doping}", ln=1)

        filename = filedialog.asksaveasfilename(defaultextension=".pdf")

        if filename:
            pdf.output(filename)
            messagebox.showinfo("Success", "PDF Saved Successfully!")

    except NameError:
        messagebox.showerror("Error", "Calculate first before exporting")
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error:{e}")
# ================================================
# Tab 4: Load CSV
# ================================================
def load_csv():
    try:
        path = filedialog.askopenfilename()

        with open(path, "r") as f:
            reader = csv.reader(f)
            data = list(reader)

        entry_ND.delete(0, tk.END)
        entry_ND.insert(0, data[0][0])

        entry_NA.delete(0, tk.END)
        entry_NA.insert(0, data[1][0])

        entry_ni.delete(0, tk.END)
        entry_ni.insert(0, data[2][0])

        messagebox.showinfo("Loaded", "CSV Loaded Successfully!")

    except FileNotFoundError:
        messagebox.showerror("Error", "could not load CSV file")
    except Exception as e:
        messagebox.showerror("Erorr", f"Unexpected error: {e}")
        # ================================================
# GUI LAYOUT
# ================================================
root = tk.Tk()
root.title("Semiconductor Doping Calculator — Project Version")
root.geometry("520x460")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# -------------------------
# Tab 1 — Calculate
# -------------------------
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Calculate")

ttk.Label(tab1, text="Donor ND:").pack()
entry_ND = ttk.Entry(tab1)
entry_ND.pack()

ttk.Label(tab1, text="Acceptor NA:").pack()
entry_NA = ttk.Entry(tab1)
entry_NA.pack()

ttk.Label(tab1, text="Intrinsic ni:").pack()
entry_ni = ttk.Entry(tab1)
entry_ni.pack()

ttk.Button(tab1, text="Calculate", command=calculate).pack(pady=10)

output = tk.Text(tab1, width=60, height=12)
output.pack()

# -------------------------
# Tab 2 — Graph
# -------------------------
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Graph")

ttk.Button(tab2, text="Plot Carrier Graph", command=plot_graph).pack(pady=50)

# -------------------------
# Tab 3 — Export PDF
# -------------------------
tab3 = ttk.Frame(notebook)
notebook.add(tab3, text="PDF Report")

ttk.Button(tab3, text="Save PDF Report", command=export_pdf).pack(pady=50)

# -------------------------
# Tab 4 — Load CSV
# -------------------------
tab4 = ttk.Frame(notebook)
notebook.add(tab4, text="Load CSV")

ttk.Button(tab4, text="Load CSV File", command=load_csv).pack(pady=60)

root.mainloop()