import re
import os
import xlsxwriter

def funkcija(root):
    foldername = root.split("/")[-1]
    file_edges = root + "/" + foldername + ".edges"
    file_sol = root + "/" + foldername + ".sol"

    with open(file_edges, 'r') as fe:
        first_line = fe.readline()
        num_v = first_line.split()[0]
        num_e = first_line.split()[1]

    try:
        with open(file_sol, 'r') as fs:
            contain_sol = fs.read()
    except:
        row = [foldername, num_v, num_e, "NA", "NA", "NA"]
        return row

    rex_restul = "Razlika:[\s]+([\d]+)?"
    rex_time = "Trajalo[\s]+je:[\s]+([\d]+.[\d]+)?[\s]*sekundi"
    re_result = re.compile(rex_restul)
    all_results = re_result.findall(contain_sol)
    all_results = [int(res) for res in all_results]

    re_time = re.compile(rex_time)
    all_times = re_time.findall(contain_sol)
    all_times = [float(time) for time in all_times]

    best_result = min(all_results)
    average_result = sum(all_results)/len(all_results)
    average_time = sum(all_times)/len(all_times)

    row = [foldername, num_v, num_e, best_result, average_result, average_time]
    return row

def create_excel_file(data):
    filename = "statistika testiranja.xlsx"
    file_location = "../results_of_execute_scripts/"
    filename = file_location + filename
    
    if not os.path.exists(file_location):
        os.mkdir(file_location)
    workbook = xlsxwriter.Workbook(filename)

    for sheetname, data_ in data.items():
        worksheet = workbook.add_worksheet(sheetname)
        worksheet.set_column('A:F', 18)
        cell_header = workbook.add_format({'bold': True})
        # redovi tabele
        for i, row in enumerate(data_):
            # kolone u redovima
            for j, column in enumerate(row):
                if i == 0:
                    worksheet.write(i, j, column, cell_header)
                else:
                    worksheet.write(i, j, column)
    workbook.close()

if __name__ == '__main__':
    cyc = [["naziv mreže", "broj čvorova", "broj grana", "najbolji rezultat", "prosječan rezultat", "prosječno vrijeme"]]
    mips = [["naziv mreže", "broj čvorova", "broj grana", "najbolji rezultat", "prosječan rezultat", "prosječno vrijeme"]]
    tap06 = [["naziv mreže", "broj čvorova", "broj grana", "najbolji rezultat", "prosječan rezultat", "prosječno vrijeme"]]
    sgd = [["naziv mreže", "broj čvorova", "broj grana", "najbolji rezultat", "prosječan rezultat", "prosječno vrijeme"]]
    for root, dirs, files in os.walk(".."):
        for dir in dirs:
            if(dir.endswith("cyc")):
                cyc.append(funkcija(root+"/"+dir))
            elif(dir.endswith("mips")):
                mips.append(funkcija(root+"/"+dir))
            elif(dir.endswith("tap06")):
                tap06.append(funkcija(root+"/"+dir))
            elif(dir.endswith("sgd")):
                sgd.append(funkcija(root+"/"+dir))

    data = {
        "CYC" : cyc,
        "MIPS" : mips,
        "TAP06": tap06,
        "SGD": sgd
           }
    create_excel_file(data)
