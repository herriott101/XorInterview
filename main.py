import pandas as pd
from influxdb_client_3 import InfluxDBClient3, flight_client_options
import certifi
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import asksaveasfile
from pandastable import Table


def main_menu():
    """Creates a main menu GUI"""
    clear_gui()

    for row_num in range(3):
        tk.Grid.rowconfigure(root, row_num, weight=1)
    for col_num in range(2):
        tk.Grid.columnconfigure(root, col_num, weight=1)

    ttk.Label(root, text="Please select an option:", anchor="center").grid(column=0, row=0, columnspan=2, sticky="NSEW")

    ttk.Button(root, text="Import data", command=import_menu, padding=2).grid(column=0, row=1, sticky="NSEW")
    ttk.Button(root, text="Export data", command=lambda: export_to_csv(df), padding=2)\
        .grid(column=0, row=2,sticky="NSEW")
    ttk.Button(root, text="View data", command=view_data, padding=2).grid(column=1, row=1, sticky="NSEW")

    root.mainloop()


def clear_gui():
    """Clears the GUI so a new menu can be used"""
    for ele in root.winfo_children():
        ele.destroy()


def import_menu():
    """Menu for importing data from the database"""
    clear_gui()

    for row_num in range(7):
        tk.Grid.rowconfigure(root, row_num, weight=1)
    for col_num in range(2):
        tk.Grid.columnconfigure(root, col_num, weight=1)

    ttk.Label(root, text="Please enter the InfluxDB host:", padding=2).grid(column=0, row=0, sticky="NSEW")
    ttk.Entry(root, textvariable=host_in).grid(column=1, row=0, sticky="NSEW", padx=2)

    ttk.Label(root, text="Please enter the org name:", padding=2).grid(column=0, row=1, sticky="NSEW")
    ttk.Entry(root, textvariable=org_in).grid(column=1, row=1, sticky="NSEW", padx=2)

    ttk.Label(root, text="Please enter the database name:", padding=2).grid(column=0, row=2, sticky="NSEW")
    ttk.Entry(root, textvariable=database_in).grid(column=1, row=2, sticky="NSEW", padx=2)

    ttk.Label(root, text="Please enter the token:", padding=2).grid(column=0, row=3, sticky="NSEW")
    ttk.Entry(root, textvariable=token_in).grid(column=1, row=3, sticky="NSEW", padx=2)

    ttk.Label(root, text="Please enter SQL query:", padding=2).grid(column=0, row=4, sticky="NSEW")
    ttk.Entry(root, textvariable=query_in).grid(column=1, row=4, sticky="NSEW", padx=2)

    ttk.Button(root, text="Import data", command=import_database, padding=2) \
        .grid(column=0, row=5, columnspan=2, sticky="NSEW")

    ttk.Button(root, text="Main Menu", command=main_menu, padding=2).grid(column=0, row=6, columnspan=2, sticky="NSEW")

    root.mainloop()


def view_data():
    """Uses pandastable to view, edit, and graph the imported data"""
    data_window = tk.Toplevel(root)
    data_window.title("Data")

    global df

    table = Table(data_window, dataframe=df, showtoolbar=True, showstatusbar=True)
    table.show()


def import_database():
    """Imports the database from InfluxDB"""
    # Need to specify the root certificate in non-POSIX-compliant systems - code snippet from
    # https://docs.influxdata.com/influxdb/clustered/reference/client-libraries/v3/python/
    fh = open(certifi.where(), "r")
    cert = fh.read()
    fh.close()

    token = token_in.get()
    org = org_in.get()
    host = host_in.get()
    query = query_in.get()
    database = database_in.get()

    try:
        client = InfluxDBClient3(host=host, token=token, org=org,
                                 flight_client_options=flight_client_options(tls_root_certs=cert))
        table = client.query(query=query, database=database, language="sql")
    except Exception as e:
        mess = "An error occurred:\n" + str(e)
        messagebox.showerror(title=type(e).__name__, message=mess)
        return

    global df
    df = table.to_pandas().sort_values(by="time")

    main_menu()


def export_to_csv(df_in):
    """Exports the database to a CSV (or other) file"""
    files = [('CSV', '*.csv'), ('All Files', '*.*'), ('Text Document', '*.txt')]
    file = asksaveasfile(mode="w", filetypes=files, defaultextension=files)
    if file is None:
        return

    df_in.to_csv(file, index=False)


if __name__ == "__main__":
    """Main function, sets up variables and initial GUI"""

    df = pd.DataFrame()

    root = tk.Tk()
    root.title("InfluxDB Tool")

    # Initialise variables used within menu
    token_in = tk.StringVar("")
    org_in = tk.StringVar("")
    host_in = tk.StringVar("")
    query_in = tk.StringVar("")
    database_in = tk.StringVar("")

    main_menu()
