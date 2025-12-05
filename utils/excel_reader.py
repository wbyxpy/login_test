# -*- coding: utf-8 -*-
"""
Excel数据读取工具类
"""
import openpyxl
from typing import List, Dict


class ExcelReader:
    """Excel读取器类"""
    
    def __init__(self, excel_file: str, sheet_name: str = None):
        """
        初始化Excel读取器
        :param excel_file: Excel文件路径
        :param sheet_name: 工作表名称，默认读取第一个工作表
        """
        self.excel_file = excel_file
        self.workbook = openpyxl.load_workbook(excel_file)
        
        if sheet_name:
            self.sheet = self.workbook[sheet_name]
        else:
            self.sheet = self.workbook.active
    
    def read_data(self) -> List[Dict]:
        """
        读取Excel数据，返回字典列表
        :return: 测试数据列表
        """
        data = []
        
        # 获取表头（第一行）
        headers = []
        for cell in self.sheet[1]:
            headers.append(cell.value)
        
        # 读取数据行
        for row in self.sheet.iter_rows(min_row=2, values_only=True):
            row_data = {}
            for header, value in zip(headers, row):
                row_data[header] = value
            
            # 只读取run列为'yes'的用例
            if row_data.get('run', '').lower() == 'yes':
                data.append(row_data)
        
        return data
    
    def get_case_by_id(self, case_id: str) -> Dict:
        """
        根据用例ID获取单个测试用例
        :param case_id: 用例ID
        :return: 测试用例数据
        """
        all_data = self.read_data()
        for case in all_data:
            if case.get('case_id') == case_id:
                return case
        return None
    
    def close(self):
        """关闭工作簿"""
        self.workbook.close()


if __name__ == '__main__':
    # 测试代码
    from config.config import TEST_DATA_FILE
    
    reader = ExcelReader(TEST_DATA_FILE)
    test_data = reader.read_data()
    
    print(f"读取到 {len(test_data)} 条测试数据:")
    for case in test_data:
        print(f"  - {case['case_id']}: {case['case_name']}")
    
    reader.close()
