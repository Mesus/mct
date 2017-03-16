import os,sys,xlrd
reload(sys)
sys.setdefaultencoding( "utf-8" )
def paser_xls(filename):
    # filename = sys.path[0]+'/'+filename
    data = xlrd.open_workbook(filename, 'rb')
    sheet_num =  len(data.sheets())
    # print sheet_num
    s = ''
    edge = []
    # col_num = 1
    sheet = data.sheet_by_index(0)
    for col in range(sheet.ncols):
        col_lable = ''
        if col == 0:
            col_lable = 'A'
        if col == 1:
            col_lable = 'B'
        if col == 2:
            col_lable = 'C'
        if col == 3:
            col_lable = 'D'
        if col == 4:
            col_lable = 'E'
        s += col_lable+':['
        for row in range(sheet.nrows):
            val = sheet.cell_value(row,col)
            if val != '':
                s += str(int(val))+','
        s = s[:len(s)-1]
        s += '];'

    return s

if __name__=='__main__':
    arg = sys.argv
    fn = arg[1]
    classname = arg[2]
    class_data = paser_xls(fn)
    sql = "INSERT INTO public.sm_classify(class_1) VALUES ('%s')"%(class_data)
    print sql