from explain_shap import compute_shap
from explain_lime import compute_lime
from insert_logs_mongodb import insert_to_mongo

# Process SHAP explanations
shap_results = compute_shap()
insert_to_mongo(shap_results, collection="shap_explanations")

# Process LIME explanations
lime_results = compute_lime()
insert_to_mongo(lime_results, collection="lime_explanations")

print("✅ SHAP & LIME processed and inserted into MongoDB.")

