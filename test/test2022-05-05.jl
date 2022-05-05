using DrWatson
@quickactivate "SystemicRisk" # 快速激活本项目
using DataFrames

struct S
    tau::Int
    s1::String
    s2::String
end

s=S(1,"s1","s2")

fieldstuples=struct2ntuple(s)

df=DataFrames(fieldstuples)

tau=0
while tau<=10
    tau+=1
    dd=DataFrames(fieldstuples)
    dd[!,:]=
    append!(df,dd)
end



function collect_agent_data!(df, model, properties::Vector, step::Int=0; kwargs...)
    alla = sort!(collect(values(model.agents)), by=a -> a.id)
    dd = DataFrame()
    dd[!, :step] = fill(step, length(alla))
    dd[!, :id] = map(a -> a.id, alla)
    if :agent_type ∈ propertynames(df)
        dd[!, :agent_type] = map(a -> Symbol(typeof(a)), alla)
    end

    for fn in properties
        _add_col_data!(dd, eltype(df[!, dataname(fn)]), fn, alla; kwargs...)
    end
    append!(df, dd)
    return df
end

function _add_col_data!(
    dd::DataFrame,
    col::Type{T},
    property,
    agent_iter;
    obtainer=identity
) where {T}
    dd[!, dataname(property)] = collect(get_data(a, property, obtainer) for a in agent_iter)
end