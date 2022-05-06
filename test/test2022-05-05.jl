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

function init_agent_dataframe(
    model::ABM{S,A},
    properties::Vector{<:Tuple},
) where {S,A<:AbstractAgent}
    nagents(model) < 1 && throw(ArgumentError(
        "Model must have at least one agent to " * "initialize data collection",
    ))
    headers = Vector{String}(undef, 1 + length(properties))
    types = Vector{Vector}(undef, 1 + length(properties))

    utypes = union_types(A)

    headers[1] = "step"
    types[1] = Int[]

    if length(utypes) > 1
        multi_agent_agg_types!(types, utypes, headers, model, properties)
    else
        single_agent_agg_types!(types, headers, model, properties)
    end
    DataFrame(types, headers)
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

dataname(x::Tuple) =
    join(vcat([dataname(x[2]), dataname(x[1])], [dataname(s) for s in x[3:end]]), "_")
dataname(x::Union{Symbol,String}) = string(x)
# This takes care to include fieldnames and values in the column name to make column names unique
# if the same function is used with different values of outer scope variables.
dataname(x::Function) = join(
    vcat([string(x)], ["$(prop)=$(getproperty(x, prop))" for prop in propertynames(x)]),
    "_",
)
