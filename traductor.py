from transformers import MarianMTModel, MarianTokenizer

modelo = "Helsinki-NLP/opus-mt-es-en"
tokenizer = MarianTokenizer.from_pretrained(modelo)
model = MarianMTModel.from_pretrained(modelo)

texto = "Coco siempre ha estado fascinada por la magia. Por desgracia, solo los hechiceros pueden practicar este arte y los agraciados son elegidos desde su nacimiento. Un día, Qifrey, un mago, llega al pueblo de la niña. Al espiarla, Coco comprende la verdadera naturaleza de la magia y recuerda un libro y un tintero que le compró a un misterioso desconocido cuando era niña... Pero, en su ignorancia, ¡Coco comete un acto trágico!"
tokens = tokenizer(texto, return_tensors="pt", padding=True, truncation=True)
traduccion = model.generate(**tokens)
texto_traducido = tokenizer.decode(traduccion[0], skip_special_tokens=True)

print(texto_traducido)  # "Hello, how are you?"