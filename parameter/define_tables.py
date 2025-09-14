# -------------------------------
# 2. Table 容器
# -------------------------------
from typing import Union, Dict, List


class Table:
    def __init__(self, table: Union[Dict[int, float], List[float]], desc:str=""):
        if isinstance(table, Dict):
            self.table = table
        elif isinstance(table, List):
            # 列表时 index 从 0 - (len-1)
            self.table = {k: v for k, v in enumerate(table)}
        else:
            raise TypeError('必须是字典或列表')
        self.desc = desc # 数据表存储内容的描述

    def __getitem__(self, index: int) -> float:
        """支持 table[index] 的访问方式"""
        return self.table[index]

    def __setitem__(self, index: int, value: float):
        """支持 table[index] = value 的赋值方式"""
        self.table[index] = value

    def get(self, index: int) -> float:
        if index not in self.table:
            raise IndexError("Table 中没有该索引")
        return self.table[index]

    def __mul__(self, factor: float) -> 'Table':
        """支持 Table * 常数"""
        if not isinstance(factor, (int, float)):
            raise TypeError("只能乘以数字")
        new_table = {k: v * factor for k, v in self.table.items()}
        return Table(new_table, desc=f"{self.desc} * {factor}")

    def __rmul__(self, factor: float) -> 'Table':
        """支持 Table * 常数"""
        if not isinstance(factor, (int, float)):
            raise TypeError("只能乘以数字")
        new_table = {k: v * factor for k, v in self.table.items()}
        return Table(new_table, desc=f"{self.desc} * {factor}")

    def __repr__(self):
        return f"Table({self.table}, desc='{self.desc}')"


if __name__ == '__main__':
    table = Table({1: 0.3, 2: 0.6})
    print(1/23.4 * table * 23.4)
