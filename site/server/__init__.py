from app import *
import routes
from match_predictor import predict_proba

if __name__ == "__main__":
    print(predict_proba("Germany", "Brazil"))
    app.run(debug=True)