"函数区：工具集"

## 函数区：工具集

##########################################
#状态/使用
##########################################

"宏：当测试时使用"
macro test(content)
    if env[:isTest]
        return esc(content)
        # return :(content)
        # return $(content)
        # return :($(content))
    end
end
