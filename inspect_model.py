import pickle
import sys

try:
    with open('heart_sound_rf_model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    print("="*60)
    print("MODEL INSPECTION")
    print("="*60)
    print(f"\nModel Type: {type(model)}")
    print(f"Model Class: {model.__class__.__name__}")
    
    print("\n" + "="*60)
    print("AVAILABLE ATTRIBUTES/METHODS:")
    print("="*60)
    attrs = dir(model)
    
    # Show methods
    methods = [attr for attr in attrs if callable(getattr(model, attr)) and not attr.startswith('_')]
    print(f"\nMethods ({len(methods)}):")
    for method in methods[:20]:  # Show first 20
        print(f"  - {method}")
    
    # Show properties
    props = [attr for attr in attrs if not callable(getattr(model, attr)) and not attr.startswith('_')]
    print(f"\nProperties ({len(props)}):")
    for prop in props[:20]:  # Show first 20
        print(f"  - {prop}")
    
    # Check for predict
    print("\n" + "="*60)
    print("PREDICTION CAPABILITY:")
    print("="*60)
    has_predict = hasattr(model, 'predict')
    has_predict_proba = hasattr(model, 'predict_proba')
    
    print(f"Has 'predict' method: {has_predict}")
    print(f"Has 'predict_proba' method: {has_predict_proba}")
    
    # If it's a dictionary or other structure
    if isinstance(model, dict):
        print("\n⚠️  Model is a DICTIONARY with keys:")
        for key in model.keys():
            print(f"  - {key}: {type(model[key])}")
    
    print("\n" + "="*60)
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
