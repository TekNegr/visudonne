############################DEFINITION##############################################################################################


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def get_data():
    data_test = pd.read_csv("c:/Users/hsoci/Desktop/devstar/visudonne/tp3/Testing_BOP.csv", sep=",")
    data_train = pd.read_csv("c:/Users/hsoci/Desktop/devstar/visudonne/tp3/Training_BOP.csv", sep=",")
    return data_test,data_train


############################CODE##############################################################################################

class DataAnalysisApp:
    
    def __init__(self, root : tk.Tk, data_train, data_test):
        self.root = root
        self.root.title("Data Analysis GUI")
        self.data_train = data_train
        self.data_test = data_test
        self.backup_train = data_train.copy()
        self.backup_test = data_test.copy()
        self.display_type = ""
        self.current_data = self.data_train
        self.current_data_type = "Training"
        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface."""
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        self.title_label = tk.Label(self.frame, text=self.display_type)
        self.title_label.grid(row=0, column=0, columnspan=2)

        self.text_area = tk.Text(self.frame, height=50, width=200)
        self.text_area.grid(row=1, column=0, columnspan=2)

        # Add buttons or other UI elements to set display_type and update the GUI
        
        
        button_frame = tk.Frame(self.frame)
        button_frame.grid(row=2, column=1, columnspan=2, pady=10)
        
        show_button = tk.Button(button_frame, text="Show Data", command=self.show_data)
        show_button.grid(row=0, column=0, padx=5, pady=5)

        describe_button = tk.Button(button_frame, text="Describe Data", command=self.describe_data)
        describe_button.grid(row=0, column=1, padx=5, pady=5)

        btn_show_missing_data = tk.Button(button_frame, text="Show Missing Data", command=self.missing_data)
        btn_show_missing_data.grid(row=1, column=0, padx=5, pady=5)

        btn_clean_data = tk.Button(button_frame, text="Clean Data", command=self.clean_all_data)
        btn_clean_data.grid(row=1, column=1, padx=5, pady=5)

        btn_correlate_data = tk.Button(button_frame, text="Correlate Data", command=self.matrix_correlate)
        btn_correlate_data.grid(row=2, column=0, padx=5, pady=5)

        btn_show_corr_fig = tk.Button(button_frame, text="Show Correlation Figure")
        btn_show_corr_fig.grid(row=2, column=1, padx=5, pady=5)

        self.selector = ttk.Combobox(self.frame, values=["Training", "Testing"], state="readonly")
        self.selector.grid(row=2, column=0, padx=5, pady=5)
        self.selector.current(0)  # Set default to "Training"
        self.selector.bind("<<ComboboxSelected>>", lambda event: self.select_data(self.selector.get()))

        self.modifier_frame = tk.Frame(self.frame)
        self.modifier_frame.grid(row=2, column=2, columnspan=2, padx=5,pady=5)
        
        
        self.check = tk.BooleanVar()
        self.drop_check = tk.Checkbutton(self.modifier_frame, text="Drop boolean columns", variable=self.check)
        self.drop_check.grid(row=0, column=0, columnspan=2, padx=5,pady=5)
        
        self.reset_btn = tk.Button(self.modifier_frame, text="RESET", command=self.reset_data)
        self.reset_btn.grid(row=1, column=0, columnspan=2, padx=5,pady=5)

    #STATE CHANGERS
    
    def show_data(self):
        """Display the data in the text area."""
        self.display_type = "Show"
        self.update_gui()

    def describe_data(self):
        """Display the description of the data in the text area."""
        self.display_type = "Describe"
        self.update_gui()
    
    def missing_data(self):
        """Display the missing data in the text area."""
        self.display_type = "Missing"
        self.update_gui()
    
    def matrix_correlate(self):
        print("Correlation in progress")
        self.display_type == "Correlate"
        self.update_gui()
    
    
    
    
    #GUI UPDATERS 

    def blank_screen(self, text:str ):
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, text)

    def update_gui(self):
        print("Updating GUI")
        """Update the GUI based on the selected display type."""
        self.text_area.delete(1.0, tk.END)  # Clear previous content
        if self.display_type == "Show":
            self.show_GUI_data()
        elif self.display_type == "Describe":
            self.show_GUI_data_describe()
        elif self.display_type == "Missing":
            self.show_GUI_missing()
        elif self.display_type =="Correlate":
            self.show_GUI_correlation()
        elif self.display_type == "Plot":
            # self.plot_correlate()
            pass
        
        if self.current_data_type == "Training":
            self.select_data("Training")
        elif self.current_data_type == "Testing":
            self.select_data("Testing")
           
        title = f"{self.display_type} - {self.current_data_type}"   
        
        self.title_label = tk.Label(self.frame, text=title)
        self.title_label.grid(row=0, column=0, columnspan=2)

        print(f"Display type :{self.display_type} ; Data Type : {self.current_data_type}")

    def show_GUI_data(self):
         
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, str(self.current_data.head))
        print(self.current_data.head)
        print(self.current_data_type)
        
    def show_GUI_data_describe(self):
                   
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, str(self.current_data.describe))
        print(self.current_data.describe)
        print(self.current_data_type)

    def get_miss_data(self, data):
        return data.isnull().mean() *100

    def show_GUI_missing(self):
        print("Showing missing data")
        missing_data = self.get_miss_data(self.current_data)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, str(missing_data))
        print(missing_data)
        print(self.current_data_type)

    def show_GUI_correlation(self):
        print("Showing correlation")
        matrix_corr = self.correlate_data(self.current_data, self.current_data_type)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, str(matrix_corr))
        print(matrix_corr)
        print(self.current_data_type)
        
        
        
    #DATA MANIPULATORS

    def reset_data(self):
        print('resetting')
        self.data_test = self.backup_test
        self.data_train = self.backup_train
        if self.current_data_type == "Training":
            self.current_data = self.data_train
        else : 
            self.current_data = self.data_test
        self.update_gui()

    def select_data(self, type :str):
        """Select the data based on the given type."""
        if type == "Training":
            self.current_data_type = "Training"
            self.current_data = self.data_train
        elif type == "Testing":
            self.current_data_type = "Testing"
            self.current_data = self.data_test
        else : 
            raise ValueError("Impossible to choose this type")

    def clean_all_data(self):
        self.data_test = self.clean_data(self.data_test, self.check.get())
        self.data_train = self.clean_data(self.data_train, self.check.get())
        self.update_gui()
    
    def clean_data(self, data, dropping:bool=True):
        for column in data.columns:
            if data[column].isnull().sum()>0:
                if data[column].dtype == "float64" or data[column].dtype == "int64":
                    data[column].fillna(data[column].mean(), inplace=True)
                else:
                    data[column].fillna("Unkown", inplace=True)
                    
        data = self.convert_bool(data)

        if dropping:
            data.drop(["deck_risk"], axis=1, inplace=True)
            data.drop(["oe_constraint"], axis=1, inplace=True)
            data.drop(["ppap_risk"], axis=1, inplace=True)
            data.drop(["stop_auto_buy"], axis=1, inplace=True)
            data.drop(["rev_stop"], axis=1, inplace=True)
            data.drop(["went_on_backorder"], axis=1, inplace=True)
        
        
        return data
        
    def correlate_data(self, data, sample_fraction: float = 0.001):
        print("Starting Correlation...\n")
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input data must be a pandas DataFrame.")
        
        if sample_fraction>0:
            data_sample = data.sample(frac=sample_fraction, random_state=1)
            print("Sampling Successful. Encoding...\n")
        else:
            data_sample = data
            print("No sampling performed. Using the entire dataset.\n")
            
        data_encoded = pd.get_dummies(data_sample, drop_first=True)
        # data_encoded = convert_bool(data_encoded)/
        print(f"Encoding Successful. Encoded {data_encoded.shape[1]} features for {data_encoded.shape[0]} rows.\n")
        
        print("Calculating correlation matrix...\n")
        matrix_corr = data_encoded.corr()
        print("Correlation calculation completed successfully.\n")
        
        return matrix_corr
    
    def show_corr_fig(self, data_corr, TYPE:str):
        print("Creating correlation plot...\n")
        plt.figure()
        sns.heatmap(data_corr, annot=True, fmt=".2f", cmap="coolwarm", square=True, cbar_kws={"shrink": .8})
        title = f"MATRICE DE CORRELATION DE {TYPE}"
        plt.title(title)
        plt.show()
        print("Printing matrix....\n")
    
    def convert_bool(self, data):
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input must be a pandas dataframe")
        return data.replace({'Yes': True, 'No':False})



    

    




############################LAUNCHER##############################################################################################

    
def main():
    data_test, data_train = get_data()
    # main_GUI(data_train,  data_test)
    root = tk.Tk()
    app = DataAnalysisApp(root, data_train, data_test)
    root.mainloop()
    
    
    
if __name__ == "__main__":
    main()