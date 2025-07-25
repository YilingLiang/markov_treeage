# -------------------------------
# 1. 参数容器
# -------------------------------
from parameter.define_tables import Table
from pydantic import BaseModel


class ParametersOld(dict):
    """支持 .key 直接访问"""
    def __init__(self, **kwargs):
        super().__init__()
        self.update(kwargs)

    def __getattr__(self, key):
        return self[key]


class Parameters(dict):
    """
    支持 .key 直接取值
    同时支持 .desc(key) 或 .desc.key 查看描述
    """
    def __init__(self, **kwargs):
        """
        kwargs 允许两种写法：
        age = (20, '起始年龄(岁)')
        age = 20           # 无描述时默认为空字符串
        """
        super().__init__()
        self._desc = {}
        for k, v in kwargs.items():
            if isinstance(v, tuple) and len(v) == 2:
                value, doc = v
            else:
                value, doc = v, ''
            self[k] = value
            self._desc[k] = doc

    # 让 desc 既能 .desc.key 也能 .desc('key')
    class DescView:
        def __init__(self, desc_dict):
            self._d = desc_dict

        def __getattr__(self, key):
            return self._d[key]

        def __call__(self, key):
            return self._d[key]

    @property
    def desc(self):
        return self.DescView(self._desc)

    # 保持原来的 .key 语法糖
    def __getattr__(self, key):
        return self[key]

    def get(self, key: str, index=None):
        # 用于时间依赖类参数
        if isinstance(self[key], Table):
            return self[key][index]
        return self[key]


if __name__ == '__main__':
    def fun(cycle: int):
        return cycle ** 2

    p = Parameters(a="b", c=fun)
    print(p)
    print(p.a)
    print(p.c(5))
    # ===========================
    p = Parameters(
        age_base=(20, '进入模型时的年龄(岁)'),
        sex_indiv='MLE',  # 没写描述→描述是空串
        dr=(0.05, '年贴现率')
    )
    print(p.age_base)  # 20
    print(p.desc.age_base)  # 进入模型时的年龄(岁)
    print(p.dr, p.desc('dr'))  # 年贴现率
