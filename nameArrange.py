def delTeam(name,word='team'):
    if not word in name.lower():
        return name
    names = list(name.split())
    if len(names) == 1:
        return name
    new_names = []
    for n in names:
        if not word in n.lower():
            new_names.append(n)
    if len(new_names) == 1:
        return new_names[0]
    elif new_names:
        if word == 'mk':
            return new_names[0]
        return delTeam(' '.join(new_names),'mk')
    return name

def delFromList(name):
    delList = ['チーム','スクアッド','💎','*','私立','幼稚園']
    for d in delList:
        name = name.replace(d,'')
    return name

def splitFromList(name):
    splitList = ['の',"'s",'(','（',' ','.']
    for s in splitList:
        if name.split(s)[0] != '':
            name = name.split(s)[0]
    return name

def arg(name,id=0):
    idDict = {}
    if id in idDict:
        return idDict[id]
    else:
        name = delTeam(name)
        name = delFromList(name)
        name = splitFromList(name)
        return name

