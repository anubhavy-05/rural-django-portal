from django.shortcuts import render
import requests
import json

def dashboard_home(request):
    # NAYA UPDATE: Limit badha kar 100 kar di taaki trend analytics ke liye data mile
    fastapi_history_url = "http://127.0.0.1:8000/prediction-history?limit=100"
    fastapi_predict_url = "http://127.0.0.1:8000/predict-price"
    
    history_data = []
    error_message = None
    new_prediction = None

    if request.method == "POST":
        try:
            payload = {
                "state": request.POST.get("state"),
                "region": request.POST.get("region"),
                "crop_name": request.POST.get("crop_name"),
                "rainfall_mm": float(request.POST.get("rainfall_mm")),
                "temperature_c": float(request.POST.get("temperature_c"))
            }
            post_response = requests.post(fastapi_predict_url, json=payload)
            
            if post_response.status_code == 200:
                new_prediction = post_response.json().get("predicted_price_per_quintal")
            else:
                error_message = "Failed to get prediction from ML server."
        except Exception as e:
            error_message = f"Error communicating with ML API: {e}"

    try:
        response = requests.get(fastapi_history_url)
        if response.status_code == 200:
            history_data = response.json().get("data", [])
        else:
            if not error_message:
                error_message = "ML Server is responding with an error."
    except requests.exceptions.ConnectionError:
        error_message = "Could not connect to the ML Backend. Is FastAPI running on port 8000?"

    context = {
        # Table mein hum abhi bhi sirf top 10 records dikhayenge taaki page neat rahe
        'history': history_data[:10], 
        'error': error_message,
        'new_prediction': new_prediction,
        # NAYA CODE: Poora 100 records ka data JSON bankar frontend JS ke paas jayega
        'raw_history': json.dumps(history_data)
    }
    
    return render(request, 'dashboard/home.html', context)