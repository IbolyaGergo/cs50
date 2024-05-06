from cs50 import get_string

#text = "A large class of computational problems involve the determination of properties of graphs, digraphs, integers, arrays of integers, finite families of finite sets, boolean formulas and elements of other countable domains."
text = get_string("Text: ")


# Computing the Coleman-Liau index

def CLindex(text):
    spnum = 0
    sentnum = 0
    lettnum = 0

    # Counting the number of spaces, sentences, letters
    for c in text:
        if c == " ":
            spnum += 1
        elif c in (".", "!", "?"):
            sentnum += 1
        elif c.isalpha():
            lettnum += 1

    wordnum = spnum + 1

    L = lettnum / wordnum * 100
    S = sentnum / wordnum * 100

    index = round(0.0588 * L - 0.296 * S - 15.8)

    return (index)


if CLindex(text) > 15:
    print("Grade 16+")
elif CLindex(text) < 1:
    print("Before Grade 1")
else:
    print(f"Grade {CLindex(text)}")
