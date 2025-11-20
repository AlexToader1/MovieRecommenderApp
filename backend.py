# --- backend.py ---

def get_recommendations(keywords_input):
    """
    Această funcție este apelată de Front-End.
    Primește textul scris de user și returnează o listă de filme.
    """
    
    # 1. O mică "bază de date" (doar pentru test)
    # Format obligatoriu: "Titlu, Gen, An, Nota"
    baza_de_date = [
        "Avatar, Sci-Fi, 2009, 7.8",
        "The Matrix, Sci-Fi, 1999, 8.7",
        "Titanic, Romance, 1997, 7.8",
        "Shrek, Animation, 2001, 7.9",
        "Inception, Sci-Fi, 2010, 8.8",
        "The Godfather, Crime, 1972, 9.2",
        "Joker, Drama, 2019, 8.4"
    ]

    results = []
    
    # 2. Logica simplă de filtrare
    # Căutăm cuvântul scris de tine în lista de filme
    termen_cautat = keywords_input.lower() # Facem totul cu litere mici

    for film in baza_de_date:
        if termen_cautat in film.lower():
            results.append(film)

    # 3. Dacă nu găsim nimic, returnăm un mesaj de eroare "mascat" ca film
    if not results:
        return ["Nu am gasit nimic, N/A, 0000, 0.0"]

    # 4. Returnăm lista filtrată către Frontend
    return results