text = u'aweerwqشسشسصضささごお'
stripped_text = ''
for c in text:
   stripped_text += c if len(c.encode(encoding='utf_8'))==1 else ''
print(stripped_text)
