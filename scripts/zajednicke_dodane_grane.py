import sys
import re
import os

def find_file(filename):
    for root, dirs, files in os.walk(".."):
        if filename in files:
            return root+"/"+filename
    return None

def get_added_edges(filename):
    rex = "\d+:[\s]+[\d]+[\s]+[\d]+[\s]+[0][\s]+[0|1].[\d]+"
    p = re.compile(rex)
    filename = find_file(filename)
    if not filename:
        return []
    with open(filename, 'r') as f:
        content_file = f.read()
    added_lines = p.findall(content_file)
    added_edges = []
    for line in added_lines:
        e1 = line.split()[1] + " " + line.split()[2]
        e2 = line.split()[2] + " " + line.split()[1]
        if e1 not in added_edges and e2 not in added_edges:
            added_edges.append(e1)
    return added_edges

if __name__ == '__main__':
    extensen = ".out"
    filenameout = "added_edges"
    file_location = "../results_of_execute_scripts/"
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    filenameout += "-" + file1 + "-" + file2

    added_edges_in_file1 = get_added_edges(file1 + extensen)
    added_edges_in_file2 = get_added_edges(file2 + extensen)
    added_edges = [edge for edge in added_edges_in_file1 if edge in added_edges_in_file2]
    
    if len(sys.argv) > 3:
        for file_ in sys.argv[3:]:
            filenameout += "-" + file_
            added_edges_in_file = get_added_edges(file_ + extensen)
            added_edges = [edge for edge in added_edges_in_file if edge in added_edges]

    filenameout = file_location + "/" + filenameout + ".out"
    if not os.path.exists(file_location):
        os.mkdir(file_location)
    
    s = "\n" * 2
    s += "Komandna linija: "
    for arg in sys.argv:
        s+= arg + " "
    s += "\n"
    for i, inst in enumerate(sys.argv[1:]):
        s += "Instanca %d: %s\n" %(i+1, inst)
    s += "Dodano zajednikih %d grana\n" % len(added_edges)
    s += "Dodane grane su:\n"
    for e in added_edges:
        s += e + "\n"

    with open(filenameout, "w") as f:
        f.write(s)
