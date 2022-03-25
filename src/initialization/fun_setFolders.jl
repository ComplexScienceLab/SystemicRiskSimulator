"函数区：设置实验文件夹"

## 函数区：设置实验文件夹

##########################################
#状态/开发
##########################################

"函数：设置实验文件夹"
function setExperimentsFolders(env)
    if env.filenameTypeOfExperiments=="default"
        folderpath=projectdir()*"/data/sims/default"
    elseif env.filenameTypeOfExperiments=="datetime"
            # NOW
    elseif env.filenameTypeOfExperiments=="set manually"
        #TODO
    else   
        throw(DomainError(env.filenameTypeOfExperiments, "关键词取值错误！")) 
    end

    mkpath(folderpath)
    
return env
end # functioin
