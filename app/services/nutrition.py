MEAL_PLANS = {
    "diabetes": {
        "label": "Diabetes friendly",
        "summary": "Low glycemic index meals that help keep blood sugar steady through the day.",
        "avoid": ["Refined sugar and sweets", "White rice and maida", "Sugary drinks and packaged juice", "Fried snacks"],
        "days": [
            {
                "day": "Everyday pattern",
                "breakfast": "Vegetable oats or besan chilla with mint chutney",
                "lunch": "Multigrain roti, bottle gourd sabzi, cucumber salad, small bowl of dal",
                "snack": "Roasted chana or a handful of walnuts",
                "dinner": "Grilled paneer or fish with sauteed vegetables and one roti",
            }
        ],
    },
    "hypertension": {
        "label": "Blood pressure friendly",
        "summary": "Low sodium, potassium rich meals that support healthy blood pressure.",
        "avoid": ["Extra table salt", "Pickles and papad", "Processed and packaged foods", "Excess caffeine"],
        "days": [
            {
                "day": "Everyday pattern",
                "breakfast": "Vegetable poha with minimal salt and lemon",
                "lunch": "Brown rice, spinach dal, steamed vegetables, curd",
                "snack": "Fresh fruit such as banana or papaya",
                "dinner": "Khichdi with mixed vegetables and a side salad",
            }
        ],
    },
    "heart": {
        "label": "Heart friendly",
        "summary": "Low saturated fat meals rich in fibre and healthy oils for heart health.",
        "avoid": ["Deep fried food", "Red meat in excess", "Butter and ghee in large amounts", "Trans fats and bakery items"],
        "days": [
            {
                "day": "Everyday pattern",
                "breakfast": "Oats porridge with flaxseeds and fruit",
                "lunch": "Roti, rajma or chana curry, salad, small portion of rice",
                "snack": "Sprouts chaat or a fistful of almonds",
                "dinner": "Grilled fish or tofu with stir fried vegetables",
            }
        ],
    },
    "weight-management": {
        "label": "Weight management",
        "summary": "Portion controlled, high protein and high fibre meals to support a healthy weight.",
        "avoid": ["Sugary beverages", "Late night heavy meals", "Refined carbohydrates", "Fried and oily snacks"],
        "days": [
            {
                "day": "Everyday pattern",
                "breakfast": "Moong dal chilla or boiled eggs with vegetables",
                "lunch": "Roti, seasonal vegetable sabzi, dal, large bowl of salad",
                "snack": "Buttermilk or a small bowl of fruit",
                "dinner": "Vegetable soup with grilled paneer or chicken",
            }
        ],
    },
    "digestive-health": {
        "label": "Digestive health",
        "summary": "Fibre rich, easy to digest meals that support gut health.",
        "avoid": ["Excess spicy food", "Carbonated drinks", "Heavy fried meals", "Late night eating"],
        "days": [
            {
                "day": "Everyday pattern",
                "breakfast": "Ragi porridge or idli with sambhar",
                "lunch": "Roti, curd, lightly cooked seasonal vegetables, dal",
                "snack": "Papaya or a banana",
                "dinner": "Khichdi with ghee and a side of curd",
            }
        ],
    },
    "general-wellness": {
        "label": "General wellness",
        "summary": "A balanced everyday plate for people with no specific condition.",
        "avoid": ["Excess processed food", "Sugary drinks", "Skipping meals", "Overeating at night"],
        "days": [
            {
                "day": "Everyday pattern",
                "breakfast": "Vegetable upma or whole wheat toast with eggs",
                "lunch": "Roti or rice, dal, seasonal vegetable, curd",
                "snack": "Seasonal fruit or roasted makhana",
                "dinner": "Light khichdi or soup with vegetables",
            }
        ],
    },
}


def list_conditions():
    return [{"id": key, "label": value["label"]} for key, value in MEAL_PLANS.items()]


def get_plan(condition_id):
    return MEAL_PLANS.get(condition_id)
