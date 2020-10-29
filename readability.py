l = float(0)
w = float(1)
s = float(0)
txt = input("Text: ")
for i in range(len(txt)):
    x = txt[i]
    prevx = txt[i - 1]
    if x.isalpha():
        l += 1
    elif x.isspace() and not prevx.isspace():
        w += 1
    elif x in [".", "!", "?"]:
        s += 1
l *= (100 / w)
s *= (100 / w)
output = round(0.0588 * l - 0.296 * s - 15.8)
if output < 1:
    print("Before Grade 1")
elif output > 16:
    print("Grade 16+")
else:
    print("Grade", output)