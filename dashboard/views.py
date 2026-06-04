from django.shortcuts import render
import requests
import json  # Naya import graph data ke liye

def dashboard_home(request):
    fastapi_history_url = "http://127.0.0.1:8000/prediction-history?limit=10"
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

    # --- NAYA CODE: Graph ke liye data prepare karna ---
    chart_labels = []
    chart_prices = []
    
    # Hum data ko ulta kar rahe hain taaki purana data left mein aur naya right mein dikhe
    for record in reversed(history_data):
        # Label mein hum Crop aur Region dikhayenge
        chart_labels.append(f"{record['crop_name']} ({record['region']})")
        chart_prices.append(record['predicted_price'])

    context = {
        'history': history_data,
        'error': error_message,
        'new_prediction': new_prediction,
        # Data ko JSON mein convert karke frontend par bhej rahe hain
        'chart_labels': json.dumps(chart_labels),
        'chart_prices': json.dumps(chart_prices)
    }
    
    return render(request, 'dashboard/home.html', context)