from flask import Blueprint, Response, jsonify
from backend.services.data_service import *
api=Blueprint('api',__name__,url_prefix='/api')

@api.get('/health')
def health():
    try:
        m=load_metadata(); return jsonify({'status':'ok','service':'Jali PM2.5 Research Dashboard API','model_available':bool(m.get('final_model')),'selected_model':m.get('final_model'),'data_end':m.get('last_training_date')})
    except Exception as e: return jsonify({'status':'degraded','error':str(e)}),503

@api.get('/analysis')
def analysis(): return jsonify(load_analysis())
@api.get('/model')
def model():
    m=load_metadata(); return jsonify(m)
@api.get('/metrics')
def metrics():
    m=load_metadata(); return jsonify({'final_model':m['final_model'],'rmse':m['rmse'],'mae':m['mae'],'mape':m['mape'],'last_training_date':m['last_training_date'],'staleness':staleness_info(),'selection_rule':m['selection_rule']})
@api.get('/metrics/comparison')
def comparison(): return jsonify({'models':load_comparison()})
@api.get('/correlations')
def correlations(): return jsonify(load_correlations())
@api.get('/forecast')
def forecast(): return jsonify(native_payload())
@api.get('/forecast/live')
def forecast_live(): return jsonify(live_payload())
@api.get('/forecast/all')
def forecast_all(): return jsonify({'native_7day_accuracy':load_native_accuracy(),'records':records(load_csv('native_all'))})
@api.get('/forecast/live/download')
def live_download(): return Response(csv_bytes('live'),mimetype='text/csv',headers={'Content-Disposition':'attachment; filename="jali_pm25_live_capability_demo.csv"'})
@api.get('/forecast/download')
def download(): return Response(csv_bytes('native'),mimetype='text/csv',headers={'Content-Disposition':'attachment; filename="jali_pm25_random_forest_native_forecast.csv"'})
