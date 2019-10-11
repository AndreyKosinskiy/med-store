import openpyxl
DOC_TYPE_LIST = ('+','-')
DOC_TYPE_CELL = 'B1'
SIZE_OF_HEAD = 3

def open(path_to_file):
    work_book = openpyxl.load_workbook(path_to_file)
    sheet_list = work_book.sheetnames
    work_sheet = work_book.active #get active sheet 
    
    doc_type = work_sheet[DOC_TYPE_CELL].value
    rows = work_sheet.rows
    good_table = tuple(rows)[SIZE_OF_HEAD:]
    return  {
                'doc_type':doc_type,
                'good_table':good_table
            }


def analyzer_doc(doc):
    def analyzer_doc_type(value):
        return  value in DOC_TYPE_LIST
    pull_erorrs = {
        'doc_type_error:':analyzer_doc_type(doc['doc_type']),
        'empty_check:':(doc is not None)
        }
    if False in pull_erorrs.values():
        for key,value in pull_erorrs.items():
            if value == False:
                print(key,value)
    else:
        print("Save Document")

def print_table(table):
    for row in table:
        for cell in row:
            print (cell,end='')
        print ()

    
file = open('C:\\Users\\Admin\\Desktop\\put_file.xlsx')
analyzer_doc(file)


    
