from app import *
import routes
from match_predictor.main import predict_proba

if __name__ == "__main__":
    print("-"*30)
    print(predict_proba("Germany", [], "Brazil", []))
    print("-"*30)
    app.run(debug=True)
