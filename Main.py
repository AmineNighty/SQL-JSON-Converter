import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import font
import json
from tkinter import filedialog
from tkinter import PhotoImage

class MainWindow:
    def __init__(self):

        #Fenetre principal GUI
        self.window = tk.Tk()
        self.window.title("SQL ↔ JSON Converter")
        self.window.geometry("900x600")
        self.main_frame = tk.Frame(self.window)
        self.main_frame.pack(fill="both", expand=True)
        # Load icons
        self.icon_sql = PhotoImage(file="assets/sql.png")
        self.icon_json = PhotoImage(file="assets/json.png")
        self.icon_save = PhotoImage(file="assets/save.png")
        #===============================================
        self.header_font = font.Font(
        family="Arial",
        size=14,
        weight="bold"
        )
        #===============================================
        self.label_input = tk.Label(self.main_frame)
        self.label_input["text"] = "University of Naama"
        self.label_input.pack(pady=5)
        self.label_input["font"] = self.header_font
        self.label_input["fg"] = "#000000"   
        self.label_input["bg"] = "#f0f0f0"
        #================================================
        self.label_input = tk.Label(self.main_frame)
        self.label_input["text"] = "NO SQL TO SQL CONVERTER ( et vice versa ) , made by : BOUCETTA Mohammed Amine"
        self.label_input["font"] = self.header_font
        self.label_input["fg"] = "#000000"
        self.label_input["bg"] = "#f0f0f0"
        self.label_input.pack(pady=5)
        # ================================================

        # ---------- BUTTONS ----------
        self.top_frame = tk.Frame(self.main_frame)
        self.top_frame.pack(fill="x", pady=4)
        self.center_frame = tk.Frame(self.top_frame)
        self.center_frame.pack(anchor="center")
        # ================================================
        # SQL TO JSON BUTTON
        self.sql_to_json_button = tk.Button(
         self.center_frame,
         text="SQL to JSON   ",
         image=self.icon_json,
         compound="right",
         width=150,
         command=self.on_sql_to_json
        )
        self.sql_to_json_button.pack(side="left", padx=4)
        # ================================================
        # JSON TO SQL BUTTON
        self.sql_to_json_button = tk.Button(
         self.center_frame,
         text="JSON to SQL   ",
         image=self.icon_sql,
         compound="right",
         width=150,
         command=self.on_json_to_sql
        )
        self.sql_to_json_button.pack(side="left", padx=4)
        # ================================================
        # Save Output Button
        self.sql_to_json_button = tk.Button(
         self.center_frame,
         text="Save results   ",
         image=self.icon_save,
         compound="right",
         width=150,
         command=self.on_save_output
        )
        self.sql_to_json_button.pack(side="left", padx=4)
        # ================================================
        # ---------- TEXT FIELDS ----------
        # Input label
        self.label_input = tk.Label(self.main_frame)
        self.label_input["text"] = "Input (SQL or JSON):"
        self.label_input.pack(pady=5)
        # ================================================
        # Input text area
        self.input_text_area = scrolledtext.ScrolledText(self.main_frame)
        self.input_text_area["width"] = 100
        self.input_text_area["height"] = 12
        self.input_text_area.pack(pady=5)
        # ================================================
        # Output label
        self.label_output = tk.Label(self.main_frame)
        self.label_output["text"] = "Output (Converted Result):"
        self.label_output.pack(pady=5)
        # ================================================
        # Output text area
        self.output_text_area = scrolledtext.ScrolledText(self.main_frame)
        self.output_text_area["width"] = 100
        self.output_text_area["height"] = 12
        self.output_text_area.pack(pady=5)
    # ================================================
    # METHODS
    # ================================================
    # ================================================
    def on_sql_to_json(self):
        text = self.input_text_area.get("1.0", tk.END).strip()
        if text is None or text == "":
            messagebox.showwarning("Empty Input", "Please paste SQL or JSON first.")
            return
        # ================================================
        # SQL to JSON conversion HERE
        # ================================================
        result = self.convert_sql_to_json(text)
        # ================================================
        if result is None:
            messagebox.showerror("Error", "Please set INSERT INTO Statement")
        else:
            self.output_text_area.delete("1.0", tk.END)
            self.output_text_area.insert(tk.END, result)
        # ================================================

    # ================================================
    def is_json(self, text):
        try:
            json.loads(text)
            return True
        except Exception:
            return False
    # ================================================
    def convert_sql_to_json(self, sql_text):
        try:
            # Split input by semicolon to get individual INSERT statements
            statements = [stmt.strip() for stmt in sql_text.split(";") if stmt.strip() != ""]

            if len(statements) == 0:
                return None

            json_list = []

            for stmt in statements:
                if "INSERT INTO" not in stmt.upper():
                    # Skip statements that are not INSERT
                    continue

                # ----------------------------------------------
                # 1. Extract column list
                # ----------------------------------------------
                start_cols = stmt.index("(")
                end_cols = stmt.index(")", start_cols)
                columns_text = stmt[start_cols + 1: end_cols]
                columns_raw_list = columns_text.split(",")

                # Clean column names
                columns = [col.strip() for col in columns_raw_list]

                # ----------------------------------------------
                # 2. Extract VALUES part
                # ----------------------------------------------
                part_after_values = stmt.split("VALUES", 1)[1].strip()

                # Remove parentheses
                part_after_values = part_after_values.replace("(", "").replace(")", "")

                # Split values
                values_raw_list = [v.strip() for v in part_after_values.split(",")]

                # Map columns to values
                row_map = {}
                for index in range(len(columns)):
                    key = columns[index]
                    value = values_raw_list[index]

                    # Remove quotes
                    if value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]

                    # Convert numbers
                    if value.isdigit():
                        value = int(value)
                    else:
                        try:
                            value_float = float(value)
                            value = value_float
                        except:
                            pass

                    row_map[key] = value

                json_list.append(row_map)

            if len(json_list) == 0:
                return None

            # Return JSON string
            return json.dumps(json_list, indent=4)

        except Exception:
            return None

    # ================================================
    def on_json_to_sql(self):
        text = self.input_text_area.get("1.0", tk.END).strip()
        if self.is_json(text) is False:
            self.output_text_area.delete("1.0", tk.END)
            self.output_text_area.insert("1.0", "ERROR: Input is not valid JSON.")
            return
        # ================================================
        result = self.json_to_sql(text)
        # ================================================
        self.output_text_area.delete("1.0", tk.END)
        self.output_text_area.insert("1.0", result)
    # ================================================
    def json_to_sql(self, json_text):
        try:
            data = json.loads(json_text)
        except Exception as ex:
            return "ERROR: Invalid JSON input. Details: " + str(ex)
        # ================================================
        # Data must be a list containing at least one dictionary
        if type(data) is not list:
            return "ERROR: JSON must contain a list of objects."
        if len(data) == 0:
            return "ERROR: JSON list is empty."
        # ================================================
        # Take first item as reference for table columns
        # ================================================
        first_item = data[0]
        if type(first_item) is not dict:
            return "ERROR: JSON items must be objects (key-value)."
        # ================================================
        # Extract column names
        column_names = list(first_item.keys())
        # ================================================
        # Default table name (we will later replace this with input field)
        table_name = "MiniProjet_Table"
        # ================================================
        sql_output = ""
        index = 0
        # ================================================
        # Build SQL INSERT statements
        for item in data:
            # Ensure item is dictionary
            if type(item) is not dict:
                return "ERROR: All items in the JSON list must be objects."
            # ================================================
            values_list = []
            for column in column_names:
                value = item.get(column)
                # ================================================
                # Convert Python values to SQL values
                if value is None:
                    sql_value = "NULL"
                elif type(value) is str:
                    # Escape single quotes
                    value = value.replace("'", "''")
                    sql_value = "'" + value + "'"
                else:
                    sql_value = str(value)
                # ================================================
                values_list.append(sql_value)
            # ================================================
            # Build INSERT statement
            sql_insert = "INSERT INTO " + table_name + " ("
            # ================================================
            # Join columns
            for i in range(len(column_names)):
                sql_insert += column_names[i]
                if i < len(column_names) - 1:
                    sql_insert += ", "
            sql_insert += ") VALUES ("
            # ================================================
            # Join values
            for i in range(len(values_list)):
                sql_insert += values_list[i]
                if i < len(values_list) - 1:
                    sql_insert += ", "
            sql_insert += ");\n"
            # ================================================
            sql_output += sql_insert
            index += 1
        # ================================================
        return sql_output

    # ================================================
    def on_save_output(self):
        # Get content from output area
        text_to_save = self.output_text_area.get("1.0", tk.END).strip()
        # ================================================
        if text_to_save == "":
            messagebox.showwarning("Empty Output", "There is nothing to save.")
            return
        # ================================================
        # Ask user for file location
        file_path = filedialog.asksaveasfilename(
            title="Save Output",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        # ================================================
        if file_path is None or file_path == "":
            # User cancelled save
            return
        # ================================================
        try:
            file = open(file_path, "w", encoding="utf-8")
            file.write(text_to_save)
            file.close()
            messagebox.showinfo("Saved", "Output saved successfully to:\n" + file_path)
        except Exception as ex:
            messagebox.showerror("Error", "Failed to save file.\nDetails: " + str(ex))
            # ================================================
            self.button_save = tk.Button(self.button_frame, text="Save Output", command=self.on_save_output)
            self.button_save.pack(side="left", padx=5)

    # ================================================s
    def run(self):
        # Start the Tkinter event loop
        self.window.mainloop()


# ---- MAIN EXECUTION ----
if __name__ == "__main__":
    app = MainWindow()
    app.run()
