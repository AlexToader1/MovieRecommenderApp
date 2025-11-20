import customtkinter as ctk
import os
import requests
from PIL import Image
from io import BytesIO

# --- IMPORT BACKEND ---
# Această linie leagă frontend-ul de logica ta
try:
    import backend
except ImportError:
    print("⚠️ ATENȚIE: Fișierul 'backend.py' nu a fost găsit!")

# --- API KEY TMDB ---
# Pune cheia ta aici
TMDB_API_KEY = "873e9f0f953fa2189413de6263c341ec" 

# --- Calea Scriptului ---
script_directory = os.path.dirname(os.path.abspath("MovieRecommenderApp"))

class MovieAppUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- 1. Configurare Generală (Design Original) ---
        self.title("AI Movie Recommender")
        self.geometry("1100x700")
        
        ctk.set_appearance_mode("dark") 
        ctk.set_default_color_theme("blue") 
        self.configure(fg_color="#1a1a1a") # Background Dark

        icon_path= os.path.join(script_directory, "icon.ico")
        try:
            self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error: Could not load window icon from {icon_path}: {e}")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1) 

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        app_width = 1100
        app_height = 700

        # Calculăm coordonatele x și y pentru mijlocul ecranului
        x = (screen_width - app_width) // 2
        y = (screen_height - app_height) // 2

        # Aplicăm dimensiunile și poziția: LățimexÎnălțime+X+Y
        self.geometry(f"{app_width}x{app_height}+{x}+{y}")
        # -------------------------------
        
        ctk.set_appearance_mode("dark") 
        ctk.set_default_color_theme("blue") 
        self.configure(fg_color="#1a1a1a") 

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

        # --- 2. Încărcare Iconițe ---
        self.load_icons()

        # --- 3. Construire Interfață ---
        self.build_ui()

    def load_icons(self):
        self.genre_icon = None
        self.year_icon = None
        self.rating_icon = None
        try:
            self.genre_icon = ctk.CTkImage(Image.open(os.path.join(script_directory, "icon_genre.png")), size=(20, 20))
            self.year_icon = ctk.CTkImage(Image.open(os.path.join(script_directory, "period.png")), size=(20.5, 20.5))
            self.rating_icon = ctk.CTkImage(Image.open(os.path.join(script_directory, "rating.png")), size=(18, 18))
        except Exception:
            pass # Dacă nu găsește iconițele, merge și fără

    def build_ui(self):
        # --- HEADER (Titlu Colorat) ---
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, pady=(40, 20), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)
        
        title_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_container.grid(row=0, column=0)

        ctk.CTkLabel(title_container, text="Find Your ", font=("Roboto", 32, "bold"), text_color="white").pack(side="left")
        ctk.CTkLabel(title_container, text="Perfect", font=("Roboto", 32, "bold"), text_color="#E91E63").pack(side="left")

        # --- SEARCH BAR (Design Rotunjit) ---
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.grid(row=1, column=0, pady=(10, 30))

        self.search_entry = ctk.CTkEntry(
            search_frame, 
            placeholder_text="Describe what you want to see (e.g., aliens, detective...)", 
            width=700, height=50,
            font=ctk.CTkFont(size=16),
            corner_radius=25,
            border_width=2,
            border_color="#333",
            fg_color="#2b2b2b"
        )
        self.search_entry.pack()

        # --- FILTRE (Cele 3 coloane originale) ---
        filters_container = ctk.CTkFrame(self, fg_color="#2b2b2b", corner_radius=15)
        filters_container.grid(row=2, column=0, pady=10, padx=100, sticky="ew")
        filters_container.grid_columnconfigure((0, 1, 2), weight=1)

        # A. Genre
        box_genre = ctk.CTkFrame(filters_container, fg_color="transparent")
        box_genre.grid(row=0, column=0, padx=20, pady=20)
        ctk.CTkLabel(box_genre, text="Genre", font=ctk.CTkFont(weight="bold"), image=self.genre_icon, compound="left").pack(anchor="w", pady=(0, 10))
        self.genre_var = ctk.StringVar(value="All")
        ctk.CTkComboBox(box_genre, values=["All", "Action", "Comedy", "Drama", "Sci-Fi", "Horror"], variable=self.genre_var, 
                        width=200, height=35, fg_color="#343638", button_color="#E91E63").pack()

        # B. Period (RESTAURAT)
        box_year = ctk.CTkFrame(filters_container, fg_color="transparent")
        box_year.grid(row=0, column=1, padx=20, pady=20)
        ctk.CTkLabel(box_year, text="Period", font=ctk.CTkFont(weight="bold"), image=self.year_icon, compound="left").pack(anchor="w", pady=(0, 10))
        self.year_var = ctk.StringVar(value="Anytime")
        decades = ["Anytime"] + [f"{year}s" for year in range(2020, 1949, -10)]
        ctk.CTkComboBox(box_year, values=decades, variable=self.year_var, 
                        width=200, height=35, fg_color="#343638", button_color="#E91E63").pack()

        # C. Minimum Rating
        box_rating = ctk.CTkFrame(filters_container, fg_color="transparent")
        box_rating.grid(row=0, column=2, padx=20, pady=20)
        ctk.CTkLabel(box_rating, text="Minimum Rating", font=ctk.CTkFont(weight="bold"), image=self.rating_icon, compound="left").pack(anchor="w", pady=(0, 10))
        self.rating_var = ctk.DoubleVar(value=6.0)
        self.rating_slider = ctk.CTkSlider(box_rating, from_=0, to=9, number_of_steps=9, variable=self.rating_var, 
                                           command=self.update_rating_label, width=200, button_color="#E91E63", progress_color="#E91E63")
        self.rating_slider.pack(pady=(5,0))
        self.rating_label = ctk.CTkLabel(box_rating, text="6.0+", font=ctk.CTkFont(size=12), text_color="#E91E63")
        self.rating_label.pack()

        # --- BUTON CĂUTARE ---
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=3, column=0, pady=30)
        self.search_btn = ctk.CTkButton(btn_frame, text="🔍 Search Recommendations", width=300, height=55,
                                        font=ctk.CTkFont(size=18, weight="bold"), corner_radius=25, fg_color="#E91E63", hover_color="#C2185B",
                                        command=self.start_search) # Leagă butonul de funcția nouă
        self.search_btn.pack()
        
        # --- ZONA REZULTATE ---
        self.results_frame = ctk.CTkScrollableFrame(self, height=200, fg_color="#242424", border_color="#333", border_width=1)
        self.results_frame.grid(row=4, column=0, sticky="ew", padx=100)
        self.results_placeholder = ctk.CTkLabel(self.results_frame, text="Your recommendations will appear here...",
                                                font=ctk.CTkFont(size=14, slant="italic"), text_color="gray")
        self.results_placeholder.pack(expand=True, pady=50)

    def update_rating_label(self, value):
        self.rating_label.configure(text=f"{value:.1f}+")

    # --- 4. FUNCȚIA PENTRU POSTERE (TMDB API) ---
    def get_poster_url_from_tmdb(self, title):
        if "PUNE_AICI" in TMDB_API_KEY:
            return "N/A" # Nu avem cheie, nu căutăm
        try:
            # Facem request către TMDB
            search_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}"
            response = requests.get(search_url, timeout=2).json()
            
            if response.get('results'):
                poster_path = response['results'][0].get('poster_path')
                if poster_path:
                    # Construim linkul imaginii
                    return f"https://image.tmdb.org/t/p/w200{poster_path}"
        except Exception as e:
            print(f"Warning: Could not fetch poster for {title}")
        
        return "N/A"

    # --- 5. LOGICA DE CĂUTARE (NOUĂ - BACKEND INTEGRAT) ---
    def start_search(self):
        # 1. Luăm datele din interfață
        keywords = self.search_entry.get()
        genre = self.genre_var.get()
        year = self.year_var.get()
        rating = self.rating_var.get()

        # 2. Curățăm zona de rezultate
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # 3. Afișăm "Loading..."
        loading = ctk.CTkLabel(self.results_frame, text="AI is processing...", text_color="#E91E63")
        loading.pack(pady=20)
        self.update() # Forțăm actualizarea vizuală

        # 4. Apelăm Backend-ul
        results_list = []
        try:
            # AICI SE ÎNTÂMPLĂ MAGIA: Trimitem input-ul direct la backend
            # Backend-ul trebuie să aibă funcția 'get_recommendations'
            results_list = backend.get_recommendations(keywords)
            
        except Exception as e:
            loading.configure(text=f"Error calling backend: {e}")
            return

        loading.destroy()

        if not results_list:
            ctk.CTkLabel(self.results_frame, text="No movies found.", text_color="gray").pack(pady=20)
            return

        # 5. Procesăm fiecare rezultat primit
        for line in results_list:
            # Format așteptat de la backend: "Titlu, Gen, Data, Nota"
            parts = line.split(',')
            
            if len(parts) >= 4:
                title = parts[0].strip()
                genre_txt = parts[1].strip()
                date_txt = parts[2].strip()
                try:
                    score = float(parts[3].strip())
                except:
                    score = 0.0
                
                # Căutăm posterul pe loc
                poster_url = self.get_poster_url_from_tmdb(title)
                
                # Desenăm cardul
                self.create_movie_card(title, genre_txt, date_txt, score, poster_url)
                self.update() # Efect vizual de încărcare treptată

    # --- 6. DESENARE CARD FILM ---
    def create_movie_card(self, title, genre, date, rating, poster_url):
        card = ctk.CTkFrame(self.results_frame, fg_color="#2b2b2b", corner_radius=10)
        card.pack(fill="x", pady=5, padx=10)
        
        card.grid_columnconfigure(1, weight=1)

        # --- Imagine (Stânga) ---
        poster_image = None
        if poster_url != "N/A":
            try:
                response = requests.get(poster_url)
                img_data = Image.open(BytesIO(response.content))
                poster_image = ctk.CTkImage(img_data, size=(100, 150))
            except:
                pass
        
        if poster_image:
            lbl_img = ctk.CTkLabel(card, text="", image=poster_image)
        else:
            lbl_img = ctk.CTkLabel(card, text="No Img", width=100, height=150, fg_color="#444", corner_radius=5)
        
        lbl_img.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

        # --- Info (Mijloc) ---
        lbl_title = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=18, weight="bold"), anchor="w")
        lbl_title.grid(row=0, column=1, padx=10, sticky="sw")
        
        lbl_details = ctk.CTkLabel(card, text=f"{genre}  |  {date}", font=ctk.CTkFont(size=12), text_color="gray", anchor="w")
        lbl_details.grid(row=1, column=1, padx=10, sticky="nw")

        # --- Nota (Dreapta) ---
        color = "#4CAF50" if rating >= 7.5 else "#FFC107" if rating >= 5 else "#F44336"
        lbl_rating = ctk.CTkLabel(card, text=f"{rating}", font=ctk.CTkFont(size=24, weight="bold"), text_color=color)
        lbl_rating.grid(row=0, column=2, rowspan=2, padx=20)

if __name__ == "__main__":
    app = MovieAppUI()
    app.mainloop()