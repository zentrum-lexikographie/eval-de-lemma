import openai
import os

# bash command: export OPEN_AI_KEY=INSERT_KEY_HERE
openai.api_key = os.environ(["OPEN_AI_KEY"])

x_test = [["Die", "grünen", "Schuhe", "haben", "mir", "nie", "gehört", "."],
          ["Wir", "haben", "Rindfleischetikettierungsüberwachungsgesetze", "gehört", "?"]]

lemmata = []
for sent in x_test:
    prompt = f"Lemmatisiere: {str(sent)}"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024
    )
    answer = response["choices"][0]["text"]
    print(answer)
    try:
        lemmata.append(answer.split('\n\n')[0])
    except Exception as e:
        print(e)

print(lemmata)
