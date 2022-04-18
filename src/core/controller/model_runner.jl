"模型运行器"

## 模型运行器

##########################################
#状态/开发
##########################################


function runModel!(model::ModelComponent)
    model.run(model.content)
end

