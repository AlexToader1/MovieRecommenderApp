import customtkinter as ctk
import os
from PIL import Image
from tkinter import PhotoImage

# --- GET THE SCRIPT'S OWN DIRECTORY ---
script_directory = os.path.dirname(os.path.abspath("MovieRecommenderApp/front.py"))

class MovieAppUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- 1. General Configuration ---
        self.title("AI Movie Recommender")
        self.geometry("1100x700")
        
        # --- THEME CHANGED BACK TO DARK ---
        ctk.set_appearance_mode("dark") 
        
        ctk.set_default_color_theme("blue") 

        # --- COLOR CHANGED BACK TO DARK ---
        self.configure(fg_color="#1a1a1a") 

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1) 

        # --- Load Window Icon (.png) ---
        icon_path= os.path.join(script_directory, "icon.ico")
        try:
            self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error: Could not load window icon from {icon_path}: {e}")

        # --- Load Icons (Back to WHITE icons) ---
        try:
            # --- UPDATED ICON NAMES (no _dark) ---
            genre_icon_path = os.path.join("MovieRecommenderApp", "icon_genre.png")
            year_icon_path = os.path.join("MovieRecommenderApp", "icon_calendar.png")
            rating_icon_path = os.path.join(script_directory, "rating_icon.png")

            self.genre_icon = ctk.CTkImage(Image.open(genre_icon_path), size=(20, 20))
            self.year_icon = ctk.CTkImage(Image.open(year_icon_path), size=(20, 20))
            self.rating_icon = ctk.CTkImage(Image.open(rating_icon_path), size=(20, 20))
        except FileNotFoundError:
            print(f"Error: Could not find WHITE icon .png files in {script_directory}.")
            print("Please make sure 'genre_icon.png', 'year_icon.png', 'rating_icon.png' are present.")
            self.genre_icon = None
            self.year_icon = None
            self.rating_icon = None

        self.build_ui()

    def build_ui(self):
        # --- 2. TITLE (Header) ---
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, pady=(40, 20), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)
        
        title_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_container.grid(row=0, column=0)

        # --- COLOR CHANGED BACK TO WHITE ---
        title_p1 = ctk.CTkLabel(title_container, text="Find Your ", 
                                font=ctk.CTkFont(family="Roboto", size=32, weight="bold"),
                                text_color="white") # Changed from black
        title_p1.pack(side="left")

        title_p2 = ctk.CTkLabel(title_container, text="Perfect", 
                                font=ctk.CTkFont(family="Roboto", size=32, weight="bold"),
                                text_color="#E91E63") # Pink accent
        title_p2.pack(side="left")

        # --- 3. MAIN INPUT (Search Bar) ---
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.grid(row=1, column=0, pady=(10, 30))

        # --- COLORS CHANGED BACK TO DARK ---
        self.search_entry = ctk.CTkEntry(
            search_frame, 
            placeholder_text="Describe what you want to see (e.g., aliens, detective, love in paris...)", 
            width=700, height=50,
            font=ctk.CTkFont(size=16),
            corner_radius=25,
            border_width=2,
            border_color="#333", # Changed from #d3d3d3
            fg_color="#2b2b2b" # Changed from #ffffff
        )
        self.search_entry.pack()

        # --- 4. SECONDARY FILTERS ---
        # --- COLORS CHANGED BACK TO DARK ---
        filters_container = ctk.CTkFrame(self, fg_color="#2b2b2b", corner_radius=15) # Removed border args
        filters_container.grid(row=2, column=0, pady=10, padx=100, sticky="ew")
        filters_container.grid_columnconfigure((0, 1, 2), weight=1)

        # --- A. Genre ---
        box_genre = ctk.CTkFrame(filters_container, fg_color="transparent")
        box_genre.grid(row=0, column=0, padx=20, pady=20)
        label_g = ctk.CTkLabel(box_genre, text="Genre", font=ctk.CTkFont(weight="bold"), image=self.genre_icon, compound="left")
        label_g.pack(anchor="w", pady=(0, 10))
        self.genre_var = ctk.StringVar(value="All")
        genres = ["All", "Action", "Comedy", "Drama", "Sci-Fi", "Thriller", "Horror", "Animation"]
        # --- COLORS CHANGED BACK TO DARK ---
        self.genre_combo = ctk.CTkComboBox(box_genre, values=genres, variable=self.genre_var, width=200, height=35,
                                           fg_color="#343638", border_color="#343638", button_color="#E91E63",
                                           button_hover_color="#C2185B", dropdown_hover_color="#E91E63")
        self.genre_combo.pack()

        # --- B. Period ---
        box_year = ctk.CTkFrame(filters_container, fg_color="transparent")
        box_year.grid(row=0, column=1, padx=20, pady=20)
        label_y = ctk.CTkLabel(box_year, text="Period", font=ctk.CTkFont(weight="bold"), image=self.year_icon, compound="left")
        label_y.pack(anchor="w", pady=(0, 10))
        self.year_var = ctk.StringVar(value="Anytime")
        decades = ["Anytime"] + [f"{year}s" for year in range(2020, 1949, -10)]
        # --- COLORS CHANGED BACK TO DARK ---
        self.year_combo = ctk.CTkComboBox(box_year, values=decades, variable=self.year_var, width=200, height=35,
                                          fg_color="#343638", border_color="#343638", button_color="#E91E63",
                                          button_hover_color="#C2185B", dropdown_hover_color="#E91E63")
        self.year_combo.pack()

        # --- C. Minimum Rating ---
        box_rating = ctk.CTkFrame(filters_container, fg_color="transparent")
        box_rating.grid(row=0, column=2, padx=20, pady=20)
        label_r = ctk.CTkLabel(box_rating, text="Minimum Rating", font=ctk.CTkFont(weight="bold"), image=self.rating_icon, compound="left")
        label_r.pack(anchor="w", pady=(0, 10))
        self.rating_var = ctk.DoubleVar(value=6.0)
        self.rating_slider = ctk.CTkSlider(
            box_rating, from_=0, to=9, number_of_steps=9, 
            variable=self.rating_var, command=self.update_rating_label,
            width=200, height=18, button_color="#E91E63", button_hover_color="#C2185B",
            progress_color="#E91E63"
        )
        self.rating_slider.pack(pady=(5,0))
        self.rating_label = ctk.CTkLabel(box_rating, text="6.0+", font=ctk.CTkFont(size=12))
        self.rating_label.configure(text_color="#E91E63")
        self.rating_label.pack()

        # --- 5. ACTION BUTTON ---
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=3, column=0, pady=30)

        self.search_btn = ctk.CTkButton(
            btn_frame, text="🔍 Search Recommendations", width=300, height=55,
            font=ctk.CTkFont(size=18, weight="bold"),
            corner_radius=25,
            fg_color="#E91E63", 
            hover_color="#C2185B",
            text_color="white", # Button text is white
            command=self.start_search
        )
        self.search_btn.pack()
        
        # --- 6. RESULTS AREA (Scrollable Frame) ---
        # --- COLORS CHANGED BACK TO DARK ---
        self.results_frame = ctk.CTkScrollableFrame(self, height=200, fg_color="#242424", border_color="#333", border_width=1)
        self.results_frame.grid(row=4, column=0, sticky="ew", padx=100)
        self.results_placeholder = ctk.CTkLabel(self.results_frame, text="Your recommendations will appear here...",
                                                font=ctk.CTkFont(size=14, slant="italic"), text_color="gray")
        self.results_placeholder.pack(expand=True, pady=50)

    def update_rating_label(self, value):
        self.rating_label.configure(text=f"{value:.1f}+")
        
    def start_search(self):
        
        # -----------------------------------------------------------------
        # --- HERE IS THE CHANGE YOU REQUESTED ---
        #
        # The .get() method reads the text from the search box
        # and stores it in the 'keywords' string variable.
        # This variable is now ready for you to use.
        #
        keywords = self.search_entry.get()
        #
        # -----------------------------------------------------------------
        
        
        # --- NEW CODE TO SAVE KEYWORDS TO A FILE ---
        # We will save a file named 'keywords.txt' in the same folder as the script
        keywords_file_path = os.path.join(script_directory, "keywords.txt")
        
        try:
            # 'w' means 'write' mode (it will overwrite the file each time)
            # Use 'a' (append) if you want to add to the file instead
            with open(keywords_file_path, 'w', encoding='utf-8') as f:
                f.write(keywords)
            print(f"Successfully saved keywords to {keywords_file_path}")
            
        except Exception as e:
            print(f"Error: Could not save keywords to file: {e}")
        # ---------------------------------------------

        
        # The rest of the function gets the other filter values
        genre = self.genre_var.get()
        year = self.year_var.get()
        rating = self.rating_var.get()

        print(f"ML Search initiated for: '{keywords}'")
        print(f"Filters: {genre} | {year} | Rating > {rating}")
        
        
        self.results_placeholder.configure(text="Processing data...")

if __name__ == "__main__":
    app = MovieAppUI()
    
    app.mainloop()