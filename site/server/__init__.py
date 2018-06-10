from app import *
import routes
from match_predictor.main import predict_proba

if __name__ == "__main__":
    print("-"*30)
    print(
        predict_proba(
            "Group A", 4000,
            "Brazil", [
                "A. BECKER", "T. SILVA",
                "MIRANDA", "GEROMEL",
                "CASEMIRO", "D. COSTA",
                "R. AUGUSTO", "NEYMAR JR",
                "P. COUTINHO", "MARCELO",
                "MARQUINHOS"
            ],
            "Germany", [
                "NEUER", "HECTOR",
                "HUMMELS", "KHEDIRA",
                "DRAXLER", "KROOS",
                "ÖZIL", "REUS",
                "MÜLLER", "BOATENG",
                "NEUER"
            ]
        )
    )
    print("-"*30)
    app.run(debug=True)
