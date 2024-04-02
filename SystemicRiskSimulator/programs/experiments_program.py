# -*- coding: utf-8 -*-
import time

from SystemicRiskSimulator.external_packages import warnings, logging, platform, os, Path
from SystemicRiskSimulator.core.operations.operator import Operator


def experiments_program(sgv: dict, para: dict):
    """
    实验组模拟程序。用于运行实验组。

    Args:
        sgv (dict): 模拟器全局变量
        para (dict): 参数字典

    Returns:

    """

    # %% 预安装模型、数据，运行实验组

    if sgv['is_ignore_warning']:
        warnings.filterwarnings("ignore")  # 忽略警告

    ## 初始化、构建、安装模型
    sgv, models = Operator.operate_installing(sgv, para)
    ## 运行实验组
    logging.debug("\n\n\n实验组开始：\n\n")

    sgv['experiments_running_time'] = 0  # 初始化实验组运行总时长
    sgv['export_data_running_time'] = 0  # 初始化导出数据运行总时长

    sgv['simulator_start_time'] = time.time()  # 记录模拟器开始运行时刻

    for (i, para) in enumerate(sgv['list_combination_of_para']):
        model = models[f"model_{para['model_name']}"]  # 获取当前实验对应的模型
        sgv['id_experiment'] = i + 1  # 设定当前实验编号

        if (sgv['list_idsExperiment_to_run'] is None) or (sgv['id_experiment'] in sgv['list_idsExperiment_to_run']):
            ## 进行实验
            if sgv['is_use_PettingZoo_environments'] is False and sgv['is_use_RLlib_frameworks'] is False:
                ## NOTE 如果只使用模拟器自带的模型，不使用使用强化学习环境工具包自定义的模型 #DEBUG 还没测试过
                ## 运行实验
                Operator.operate_run_experiment(sgv, para, model)
            elif sgv['is_use_PettingZoo_environments'] is True and sgv['is_use_RLlib_frameworks'] is False:
                ## #NOTE 如果使用 PettingZoo 环境框架结合自定义的环境模型，但是没有用强化学习框架 RLlib 时
                ## 重置实验
                A, A_data, sgv, para = Operator.operate_reset_experiment(sgv, para)
                ## 步进式运行实验
                A, A_data, sgv, para = Operator.operate_step_experiment(A, A_data, sgv, para, model)
                # A, A_data, sgv, para, model = Operator.operate_step_experiment(sgv, para, model)
                ## 收尾实验
                Operator.operate_end_experiment(A_data, sgv)
            elif sgv['is_use_PettingZoo_environments'] is True and sgv['is_use_RLlib_frameworks'] is True:
                ## #NOTE 如果使用 PettingZoo 环境框架结合自定义的环境模型，并且使用强化学习框架 RLlib 时

                ## 导入包
                import ray
                from ray import air, tune
                from ray.tune.registry import register_env
                from ray.rllib.policy.policy import PolicySpec
                # from ray.rllib.env.wrappers.pettingzoo_env import PettingZooEnv
                from ray.rllib.env.wrappers.pettingzoo_env import ParallelPettingZooEnv
                from ray.rllib.algorithms.algorithm_config import AlgorithmConfig
                from ray.rllib.algorithms.ppo import (
                    PPO,
                    PPOConfig,
                    PPOTorchPolicy,
                )

                ## 重置实验
                A, A_data, sgv, para = Operator.operate_reset_experiment(sgv, para)

                env_name = model.attribute.entity_name

                modelEntity = model.content  # 获取节点实体对应的模型实体

                process = modelEntity.process

                content_model = modelEntity.content['content_model']
                content_agents = modelEntity.content['content_agents']
                content_finance = modelEntity.content['content_finance']
                env_PettingZoo = modelEntity.environment(A, A_data, para, sgv, content_model)

                # observations, infos = env_PettingZoo.reset()

                # ray.init()

                def env_creator(args):
                    env = modelEntity.environment(A, A_data, para, sgv, content_model)
                    return env  # 返回环境实例

                # 注册自定义的 PettingZoo 环境
                register_env(env_name, lambda config: ParallelPettingZooEnv(env_creator(config)))

                # 停止条件
                stop = {
                    "training_iteration": sgv['stop_iters'],
                    "timesteps_total": sgv['stop_timesteps'],
                    "episode_reward_mean": sgv['stop_reward'],
                }

                # 配置项
                config = (
                    PPOConfig()
                    .environment(
                        env=env_name,
                        clip_actions=True,
                        clip_rewards=True,
                        disable_env_checking=False,
                    )
                    .resources(num_gpus=int(os.environ.get("RLLIB_NUM_GPUS", "0")))
                    .rollouts(
                        num_rollout_workers=0,
                        num_envs_per_worker=1,
                        rollout_fragment_length=32,
                    )
                    # .debugging(log_level="ERROR")
                    .reporting(metrics_num_episodes_for_smoothing=1)
                    .training(
                        num_sgd_iter=1,
                        sgd_minibatch_size=4,
                        train_batch_size=32,
                    )
                )

                ## 运行实验
                logging.debug("    开始执行模型内容：")
                sgv['process_name'] = modelEntity.attribute.entity_name  # 执行的过程之名称（英文名称）

                sgv['experiment_start_time'] = time.time()  # 记录此次实验开始时间

                algo = config.build()
                # algo = PPO(config=config, env=env_name)

                for i in range(1):
                    result = algo.train()
                    if i >= stop["training_iteration"] or result["timesteps_total"] >= stop["timesteps_total"] or result["episode_reward_mean"] >= stop["episode_reward_mean"]:
                        break
                    print(result)

                #
                # tune.Tuner(
                #     "PPO",
                #     run_config=air.RunConfig(
                #         stop=stop,
                #         checkpoint_config=air.CheckpointConfig(
                #             checkpoint_frequency=10,
                #         ),
                #     ),
                #     param_space=config,
                # ).fit()

                ## 收尾实验
                Operator.operate_end_experiment(A_data, sgv)

            else:
                pass  # if

            pass  # if

        pass  # for

    sgv['simulator_end_time'] = time.time()  # 记录模拟器结束运行时刻
    sgv['simulator_running_time'] = sgv['simulator_end_time'] - sgv['simulator_start_time']  # 记录模拟器运行时长

    logging.info(f"实验组结束。\n实验组运行总时长：{sgv['experiments_running_time']} 秒。\n导出数据运行总时长：{sgv['export_data_running_time']} 秒。\n模拟器运行总时长：{sgv['simulator_running_time']}秒。")

    # sgv['experiments_end_time'] = 0  # 记录实验组结束运行时刻
    # sgv['experiments_running_time'] = sgv['experiments_end_time'] - sgv['experiments_start_time']  # 记录实验组运行时长
    # logging.info(f"实验组运行总的时长：{sgv['experiments_running_time']}秒。")

    ## 默认程序打开输出文件查看
    if sgv['is_auto_open_outputlog']:
        system = platform.system()
        if system == 'Darwin':
            os.system(r"open " + str(Path(sgv['folderpath_experiments_output_log'], r"outputlog.txt")))
        elif system == 'Windows':
            os.startfile(str(Path(sgv['folderpath_experiments_output_log'], r"outputlog.txt")))
        elif system == 'Linux':
            os.system('xdg-open ' + str(Path(sgv['folderpath_experiments_output_log'], r"outputlog.txt")))  # #DEBUG 还没测试过
        else:
            print("Unsupported operating system")
            pass  # if
        pass  # if

    if sgv['is_ignore_warning']:
        warnings.filterwarnings("default")  # 恢复警告

    pass  # function
