import os
import json
import openai



def translate_fields_arm_to_eng(chapter_content: str, application_area: str) -> tuple:
    user_prompt=f'Translate\n{{"applciation_area": {application_area}, "chapter_content": "{chapter_content}"}}'
    translated_fields = generate(messages=[
        {"role": "system", "content": "Translate Armenian to English."},
        {"role": "user", "content": 'Translate\n{"application_area": "ֆիզիկա",  "chapter_content": "քառակուսային ֆունկցիա"}'},
        {"role": "assistant", "content": '{"application_area": "physics",  "chapter_content": "quadratic function"}'},
        {"role": "user", "content": user_prompt}
    ])
    translated_fields = json.loads(translated_fields)
    return translated_fields["chapter_content"], translated_fields["application_area"]



def translate_text_arm_to_eng(text: str) -> str:
    return generate(messages=[
        {"role": "system", "content": "Translate Armenian to English."},
        {"role": "user", "content": text}
    ])



def translate_text_eng_to_arm(text: str) -> str:
    return generate(messages=[
        {"role": "system", "content": "Translate English to Armenian."},
        {"role": "user", "content": text}
    ])



def generate(messages):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=os.getenv("MODEL_NAME"),
        messages=messages
    )
    return response.choices[0].message.content