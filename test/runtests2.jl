## temp文件

##########################################
#用途/草稿；
##########################################

# using DrWatson
# @quickactivate "SystemicRisk"

function add(x, y)
    return x + y
end

macro run_process(content)
    return quote
        if x != y
            $(content)
        end
    end
end

function fun_runprocess(x, y)
    expr=@run_process :(z = add(x, y))

    return z
end

input1 = 3
input2 = 4
fun_runprocess(input1, input2)
println(z)
