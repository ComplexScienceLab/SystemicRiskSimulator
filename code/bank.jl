
## 构建商业银行主体结构

mutable struct bank_commercial # 商业银行结构体
    ID::Int32 # 银行编号
    abbr_name::String # 银行名称缩写
    name::String # 银行名称
    Assets::Float32 # 资产
    Liabilities::Float32 # 负债
    Equity::Float32 # 所有者权益
    Loan::Float32 # 贷款量
    Borrow::Float32 # 借款量
end






