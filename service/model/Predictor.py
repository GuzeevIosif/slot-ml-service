import pandas as pd


class Predictor:
    def __init__(self):
        sql_keywords = [
            'ADD',  'FETCH', 'ALTER', 'AND', 'READ', 'ANY', 'FROM',  'BETWEEN',  'GRANT',  'CASE', 'INDEX', 'SELECT',
            'INNER', 'COLUMN', 'INSERT', 'COMMIT', 'INTERSECT', 'COMPUTE', 'INTO', 'SESSION_USER', 'CONSTRAINT',
            'CONTAINS', 'JOIN', 'CREATE', 'LIKE', 'TABLE', 'THEN', 'NOT', 'NULL', 'DELETE', 'UPDATE',  'DROP',
            'VIEW', 'WHEN', 'EXISTS', 'UNION'
        ]
        sql_keywords = [r'((^| |\/\*\*\/)' + keyword.lower() + r'($| |\/\*\*\/))' for keyword in sql_keywords]
        self.sql_pattern = '|'.join(sql_keywords)

        code_keywords = [
            'echo', 'eval', 'print', 'chr', 'break', 'case', 'char', 'continue',
            'enum', 'float', 'return', 'sizeof', 'while', "ls", "pwd", "mkdir"
        ]
        code_keywords = [r'(' + keyword.lower() + r')' for keyword in code_keywords]
        self.code_pattern = '|'.join(code_keywords)

    @staticmethod
    def get_label(summary_row: pd.Series):
        print(summary_row)
        if summary_row["sql_injection"]:
            return 2
        if summary_row["eval_injection"]:
            return 3
        return 1

    def predict(self, traffic):
        x = pd.DataFrame(traffic)
        summary = pd.DataFrame(index=x.index)
        summary["sql_injection"] = x["vector"].str.contains(self.sql_pattern, regex=True, case=False)
        summary["eval_injection"] = x["vector"].str.contains(self.code_pattern, regex=True, case=False)

        return summary.apply(Predictor.get_label, axis=1)
