def tokenize(s: str):

    l, r = 0, len(s)
    tokens = []
    while l<r:

        while l<r and s[l].isspace():
            l+=1

        if l==r:
            break

        in_single_quote = False
        in_double_quote = False

        word = ""
        while l<r:
            if not in_single_quote and not in_double_quote and s[l].isspace():
                break

            if s[l] == "'" and not in_double_quote:
                in_single_quote = not in_single_quote

            elif s[l] == '"' and not in_single_quote:
                in_double_quote = not in_double_quote

            else:
                word+=s[l]

            l+=1

        if word:
            tokens.append(word)

    return tokens
