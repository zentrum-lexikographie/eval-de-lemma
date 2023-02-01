import openai
import os

openai.api_key = os.environ(["OPEN_AI_KEY"])

x_test = [["Die", "grünen", "Schuhe", "haben", "mir", "nie", "gehört", "."],
          ["Wir", "haben", "Rindfleischetikettierungsüberwachungsgesetze", "gehört", "?"]]

lemmata = []
for sent in x_test:
    prompt = f"Lemmatisiere bitte folgende Liste von Tokens: {str(sent)}"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024
    )
    answer = response["choices"][0]["text"]
    print(answer)
    lemmata.append(line.split(' - ')[1] for line in
                   answer.split('\n\n')[1].split('\n'))

print(lemmata)
