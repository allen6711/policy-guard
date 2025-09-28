import csv
import random
from faker import Faker

# --- Configuration ---
TOTAL_RECORDS = 10000
TOXIC_PERCENTAGE = 0.05  # 5%
OUTPUT_FILE = 'data/large_generated_dataset.csv'
# --- End Configuration ---

fake = Faker()

# Templates for different types of text
CLEAN_TEMPLATES = [
    "The project's progress is {adj}.", "I think the {noun} is absolutely {adj}.",
    "What is the best way to {verb} the {noun}?", "The weather today is {adj}.",
    "Just finished a book about {noun}. It was captivating.", "The meeting is at {num} PM.",
    "The performance of the {noun} was impressive.", "I'm trying to learn about {noun}.",
    "The customer service was {adj}.", "The new policy affects all {noun}s.",
    fake.sentence, fake.bs, fake.catch_phrase
]

KEYWORD_TOXIC_TEMPLATES = [
    "You are such a {keyword}.", "That is a {keyword} idea.", "I {keyword} people like you.",
    "This whole project is {keyword}.", "What a {keyword} thing to say."
]
KEYWORDS = ["stupid", "idiot", "hate", "kill"] # From our policy

SUBTLE_TOXIC_TEMPLATES = [
    "If you actually knew what you were doing, this wouldn't be an issue.",
    "I'm not surprised someone like you would think that.",
    "People from your area are all the same.",
    "Maybe you should go back to school before commenting.",
    "This is the kind of quality I'd expect from a beginner."
]

def generate_sentence(templates, fillers=None):
    template = random.choice(templates)
    if callable(template): # Handle Faker functions
        return template()

    # Simple placeholder replacement for our own templates
    if fillers:
        for key, values in fillers.items():
            if f"{{{key}}}" in template:
                template = template.replace(f"{{{key}}}", random.choice(values))
    return template

# Main generation logic
print(f"Generating {TOTAL_RECORDS} records for '{OUTPUT_FILE}'...")

num_toxic = int(TOTAL_RECORDS * TOXIC_PERCENTAGE)
num_clean = TOTAL_RECORDS - num_toxic

records = []

# Generate toxic records
for i in range(num_toxic):
    if i % 2 == 0:  # 50% keyword-based, 50% subtle
        sentence = generate_sentence(KEYWORD_TOXIC_TEMPLATES, {'keyword': KEYWORDS})
    else:
        sentence = generate_sentence(SUBTLE_TOXIC_TEMPLATES)
    records.append(sentence)

# Generate clean records
fillers = {
    'adj': ['great', 'okay', 'impressive', 'adequate', 'sunny', 'interesting'],
    'noun': ['system', 'design', 'process', 'company', 'market', 'team'],
    'verb': ['improve', 'understand', 'build', 'organize', 'manage'],
    'num': ['2', '3', '4', '5']
}
for _ in range(num_clean):
    records.append(generate_sentence(CLEAN_TEMPLATES, fillers))

random.shuffle(records)

# Write to CSV
with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'text'])
    for i, text in enumerate(records):
        writer.writerow([i + 1, text])

print("Generation complete!")
print(f"File saved to '{OUTPUT_FILE}' with {len(records)} records.")