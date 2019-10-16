import openpyxl
DOC_TYPE_LIST = ('+','-')
DOC_TYPE_CELL = 'B1'
SIZE_OF_HEAD = 3

def get_info_from_excel(file):
    work_book = openpyxl.load_workbook(file)
    sheet_list = work_book.sheetnames
    work_sheet = work_book.active #get active sheet 
    
    doc_type = work_sheet[DOC_TYPE_CELL].value
    rows = work_sheet.rows
    good_table = tuple(rows)[SIZE_OF_HEAD:]
    return  {
                'doc_type':doc_type,
                'good_table':good_table
            }


def is_valid_or_list_error(doc):
    def analyzer_doc_type(value):
        return  value in DOC_TYPE_LIST
    pull_erorrs = {
        f'doc_type_error (cell {DOC_TYPE_CELL}):':analyzer_doc_type(doc['doc_type']),
        'empty_file:':(doc is not None)
        }
    if False in pull_erorrs.values():
        return pull_erorrs
    else:
        return True

def print_table(table):
    for row in table:
        for cell in row:
            print (cell,end='')
        print ()

if __name__ == "__main__":   
    document = get_info_from_excel('C:\\Users\\Admin\\Desktop\\put_file.xlsx')
    analyzer_doc(document)


    
