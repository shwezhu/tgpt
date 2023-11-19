def with_multiline() -> str | None:
    prompt = []
    try:
        line = input()
    except (EOFError, KeyboardInterrupt):
        return None
    while line:
        prompt.append(line)
        try:
            line = input()
        except (EOFError, KeyboardInterrupt):
            return None

    return "\n".join(prompt)


def with_line() -> str | None:
    try:
        line = input()
    # Ctrl + C will raise KeyboardInterrupt, command + D will raise EOFError on macOS
    except (EOFError, KeyboardInterrupt):
        return None
    if line.lower() == "quit" or line.lower() == "exit":
        return None
    return line
