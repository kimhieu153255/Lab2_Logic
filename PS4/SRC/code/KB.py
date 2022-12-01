import itertools
import os


class KB:
    def __init__(self, clauses):
        self.clauses = clauses

    def negativeAtom(self, atom):
        if atom[0] == "-":
            return atom[1:]
        else:
            return "-" + atom

    def negativeQuery(self, query):
        arr = []
        for clause in query:
            temp = []
            for atom in clause:
                temp.append([self.negativeAtom(atom)])
            arr.append(temp)
        return list(itertools.chain.from_iterable(arr))

    def checkTrue(self, clause1, clause2):
        for atom in clause1:
            if self.negativeAtom(atom) in clause2:
                return True
        return False

    def compareClause(self, clause, clauses):
        for i in clauses:
            if set(i) == set(clause):
                return True
        return False

    def merge(self, clause1, clause2):
        temp = clause1 + clause2
        count = 0
        for atom in clause1:
            negative = self.negativeAtom(atom)
            if (atom in clause1) and (negative in clause2):
                temp.remove(atom)
                temp.remove(negative)
                count += 1
        temp = list(set(temp))
        if len(temp) == 0 and len(clause1) == 1:
            return ["{}"]
        if len(temp) == 1 and count > 1:
            return []
        if not self.compareClause(temp, self.clauses):
            return temp
        else:
            return []

    def PL_resolution(self, query):
        negative = self.negativeQuery(query)
        self.clauses += negative
        result = []
        while True:
            new = []
            pairs = list(itertools.combinations(range(len(self.clauses)), 2))
            for pair in pairs:
                clause1 = self.clauses[pair[0]]
                clause2 = self.clauses[pair[1]]
                if self.checkTrue(clause1, clause2):
                    temp = self.merge(clause1, clause2)
                    if (len(temp) != 0) and (
                        self.compareClause(temp, self.clauses) == False
                    ):
                        new.append(temp)
                        self.clauses += [temp]
                    if temp == ["{}"]:
                        self.clauses = self.clauses + new
                        result.append([str(len(new))])
                        result += new
                        result.append(["YES"])
                        return result, True
            if len(new) == 0:
                result += [["0"], ["NO"]]
                return result, False
            self.clauses = self.clauses + new
            result.append([str(len(new))])
            result += new


def sortClauses(clauses):
    arr = []
    for clause in clauses:
        temp = []
        for atom in clause:
            if atom[0] == "-":
                temp.append((atom[1:], -1))
            else:
                temp.append((atom, 1))
        arr.append(temp)
    for i in range(len(arr)):
        arr[i] = sorted(arr[i])
    result = []
    for clause in arr:
        temp = []
        for atom in clause:
            if atom[1] == -1:
                temp.append("-" + atom[0])
            else:
                temp.append(atom[0])
        result.append(temp)
    return result


def readData(fileName):
    file = open(fileName, "r").read().splitlines()
    query = []
    for i in file[0].split("OR"):
        query.append(i.strip(" "))
    numberKB = int(file[1].strip(" "))
    kb = []
    for i in file[2 : 2 + numberKB]:
        temp = []
        for j in i.split("OR"):
            temp.append(j.strip(" "))
        kb.append(temp)
    return kb, query


def writeData(fileName, clauses):
    file = open(fileName, "w")
    for clause in clauses:
        for atom in clause:
            file.write(atom)
            if clause.index(atom) < len(clause) - 1:
                file.write(" OR ")
        if clauses.index(clause) < len(clauses) - 1:
            file.write("\n")


def main():
    path = os.listdir("../file_Input/")
    for i in path:
        # print("../file_Input/" + i)
        kb, query = readData("../file_Input/" + i)
        # print("kb", kb)
        # print("query", query)
        c = KB(kb)
        result, flag = c.PL_resolution([query])
        sortedResult = sortClauses(result)
        # print("result: ", sortedResult)
        # print("flag: ", flag)
        i = i.replace("input", "output")
        writeData("../file_Output/" + i, sortedResult)


if __name__ == "__main__":
    main()
