"函数区：工具集"

## 函数区：工具集

##########################################
#状态/使用
##########################################

"宏：当测试时使用"
macro testprintln(content)
    if env[:isTest]
        return esc(
            quote
                write(f,$(content));write(f,"\n");println($(content))
            end
        )
        # return :(content)
        # return $(content)
        # return :($(content))
    end
end


