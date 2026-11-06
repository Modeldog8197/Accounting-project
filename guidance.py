"""Short, practical wellbeing suggestions; no diagnoses or tracking engine.

Sources and scope are documented in README.md.
"""

SLEEP_STEPS = (
    '1. Choose a regular bedtime and wake-up time, including weekends.\n'
    '2. Put screens away before bed; keep the room quiet and comfortably cool.\n'
    '3. Avoid caffeine later in the day. If sleep problems persist, discuss them '
    'with a healthcare professional.'
)

ACTIVITY_STEPS = (
    '1. Choose a manageable activity you enjoy, such as walking or cycling.\n'
    '2. Pick a time that fits your day, such as a break after lunch. Start gently '
    'and build up gradually rather than trying to catch up all at once.\n'
    '3. Write the activity and time in your exercise plan. Adapt it to your '
    'abilities and any advice from your healthcare professional.'
)

GUIDES = {
    'nutrition': (
        'Plan your next meal',
        '1. Choose a mix of vegetables, a whole grain and a protein source. For '
        'example, try whole-wheat roti, dal and vegetables.\n'
        '2. Add the ingredients you need to a shopping list; prepare what you can '
        'before a busy day.\n'
        '3. Keep a simple snack available, such as fruit or plain yogurt if suitable '
        'for you. Adapt choices to allergies and any prescribed diet.'),
    'exercise': ('Make a workable activity plan', ACTIVITY_STEPS),
    'care': (
        'Prepare for your appointment',
        '1. Write your main question first, then any changes you want to discuss '
        'and when you noticed them.\n'
        '2. List medicines, supplements and allergies so you can explain them clearly.\n'
        '3. Leave space for the advice you receive and any follow-up date. '
        'These notes do not diagnose symptoms or replace medical care.'),
}
