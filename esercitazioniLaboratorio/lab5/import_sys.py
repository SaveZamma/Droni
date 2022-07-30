import sys
f = sys.argv
print(f)
print(len(f))

nome_script, primo, secondo = sys.argv

print(f"""
Il nome dello script è: {nome_script}
Il primo parametro passato è: {primo}
Il secondo parametro passato è: {secondo}""")
