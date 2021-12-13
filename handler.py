from app.modules.operations import products_dept_style
from app.lib.timeutils import getDateStr

if __name__ == '__main__':
    print("strated")
    date = getDateStr()
    products_dept_style()
    print(f"Output is in products_dept_style_{date}.csv")
    print("end")