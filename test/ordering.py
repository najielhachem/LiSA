import sys

def main(argv=None):
    if (argv is None):
        argv = sys.argv

    f = open(argv[1], "r")
    lines = f.readlines()

    dico = {}
    for l in lines[1:]:
        for w in l.split(",")[3].split():
            if w not in dico:
                dico[w] = 1
            else:
                dico[w] = dico[w] + 1

    print([(w, dico[w]) for w in sorted(dico, key=dico.__getitem__, reverse = True)][:10])
    f.close()


if __name__ == '__main__':
    main()
