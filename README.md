# SystemicRisk总体架构



# 实验框架图





![系统性风险实验程序流程图-模型结构图-通用模型.drawio](README.assets/系统性风险实验程序流程图-实验程序流程图.drawio.svg)



![系统性风险实验程序流程图-模型结构图-模型对应的过程.drawio](README.assets/系统性风险实验程序流程图-模型结构图-模型对应的过程.drawio.svg)



![系统性风险实验程序流程图-实验程序流程图.drawio]()

![系统性风险实验程序流程图-模型结构图-过程对应的阶段.drawio](README.assets/系统性风险实验程序流程图-模型结构图-过程对应的阶段.drawio.svg)











> 作者说明：
>
> 本仓库`SystemicRisk`核心主要内容于`2022-03-24`继承自原仓库`SystemicRisk_code`。
> 原仓库`SystemicRisk_code`已经于`2022-03-25`停止更新。
>
> 原仓库`SystemicRisk_code`[链接地址在这](https://gitee.com/EthanLingo/SystemicRisk_code.git)。
>
> 作者：`Ethan Lin`
>
> 日期：`2022-03-25`

This code base is using the Julia Language and [DrWatson](https://juliadynamics.github.io/DrWatson.jl/stable/)
to make a reproducible scientific project named
> SystemicRisk

It is authored by Ethan Lin.

To (locally) reproduce this project, do the following:

0. Download this code base. Notice that raw data are typically not included in the
   git-history and may need to be downloaded independently.
1. Open a Julia console and do:
   ```
   julia> using Pkg
   julia> Pkg.add("DrWatson") # install globally, for using `quickactivate`
   julia> Pkg.activate("path/to/this/project")
   julia> Pkg.instantiate()
   ```

This will install all necessary packages for you to be able to run the scripts and
everything should work out of the box, including correctly finding local paths.
