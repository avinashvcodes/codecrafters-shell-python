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
            if not in_single_quote and not in_double_quote:
                if s[l].isspace():
                    break
                if s[l] == ">":
                    if word:
                        if word != "1":
                            tokens.append(word)
                        word = ""
                    tokens.append(">")
                    l+=1
                    break
                if s[l] == "\\" and l+1 < r:
                    word+=s[l+1]
                    l+=2
                    continue

            if in_double_quote and s[l] == "\\" and l+1 < r and s[l+1] in ("\"", "\\", "$", "`"):
                word+=s[l+1]
                l+=2
                continue


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

# def lex(s: str) -> list[str]:

#     tokens = []
#     word = ""

#     in_double_quotes = False
#     in_single_quotes = False
#     backslash = False

#     for ch in s:

#         if ch == "\\" and in_double_quotes:
#             backslash = True
#         elif ch == "'" and not in_double_quotes:
#             in_single_quotes = not in_single_quotes
#         elif ch == "\"" and not in_single_quotes:
#             in_double_quotes = not in_double_quotes
        
#         word += ch
#         if ch.isspace() and not in_double_quotes and not in_single_quotes:
#             if word:
#                 tokens.append(word)
        
        

