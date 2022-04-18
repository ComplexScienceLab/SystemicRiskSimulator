"过程运行器"

## 过程运行器

##########################################
#状态/开发
##########################################


function runProcess!(process::ProcessComponent)
    process.run(process.content)
end

