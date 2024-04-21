# -*- coding: utf-8 -*-
import time

import pandas

from SystemicRiskSimulator.external_packages import warnings, logging, platform, os, Path, time, sys, base64, pickle, multiprocessing, Pool
from SystemicRiskSimulator.core.operations.operator import Operator


def main():
    """
    实验组模拟程序。用于运行实验组。
    """

    # %% 预安装模型、数据，运行实验组

    # 从命令行参数获取配置字典
    sgv_base64 = sys.argv[1]
    sgv_pkl = base64.b64decode(sgv_base64)
    sgv = pickle.loads(sgv_pkl)

    # para_base64 = sys.argv[2]
    # para_pkl = base64.b64decode(para_base64)
    # paras_works = pickle.loads(para_pkl)

    # %% 预安装模型、数据，运行实验组

    if sgv['is_ignore_warning']:
        warnings.filterwarnings("ignore")  # 忽略警告

    ## 初始化、构建、安装模型
    if sgv['init_parameters_method'] == 'import data':
        sgv, parameters_works, models = Operator.operate_installing(sgv)
    elif sgv['init_parameters_method'] == 'set manually':
        sgv, parameters_works, models = Operator.operate_installing(sgv, parameters_works)  # #BUG 这里的 parameters_works 变量没有定义
        pass  # if

    ## 运行实验组
    logging.debug("\n\n\n实验组开始：\n\n")

    sgv['experiments_running_time'] = 0  # 初始化实验组运行总时长
    sgv['export_data_running_time'] = 0  # 初始化导出数据运行总时长

    sgv['simulator_start_time'] = time.time()  # 记录模拟器开始运行时刻

    # works = []
    # for i, d in parameters_works.iterrows():
    #     for w in range(sgv['vis']['num_time']):
    #         works.append((sgv, parameters_works))
    #         pass  # for
    #     pass  # for
    if sgv['is_enable_multiprocessing']:
        ## #TODO NOTE：多进程并行处理
        num_cores = int(multiprocessing.cpu_count() * sgv['percent_core_for_multiprocessing'])  # 用于计算的 CPU 核心数
        with Pool(num_cores) as p:
            p.map(fun_experiment_work, works)
            pass  # with

        pass
    else:
        ## #NOW #NOTE：串行处理
        for i, para in parameters_works.iterrows():
            para = para.to_dict()  # 将参数数据框转换为字典

            model = models[f"model_{para['model_name']}"]  # 获取当前实验对应的模型
            sgv['id_experiment'] = i + 1  # 设定当前实验编号

            ## 运行一次实验作业
            fun_experiment_work(sgv, para, model)
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
            pass  # if

        pass  # if

    pass  # main


def fun_experiment_work(sgv: dict, para: pandas.Series, model: dict):
    """
    实验组模拟程序。用于运行实验组。

    Args:
        sgv (dict): 模拟器全局变量
        para (pandas.Series): 参数作业数据框
        model (dict): 模型集字典

    Returns:

    """

    if (sgv['list_idsExperiment_to_run'] is None) or (sgv['id_experiment'] in sgv['list_idsExperiment_to_run']):  # 如果没有设置要运行的实验编号列表，或者当前实验编号在要运行的实验编号列表中，那么继续。
        ## 进行实验
        if sgv['is_use_PettingZoo_environments'] is False and sgv['is_use_RLlib_frameworks'] is False:
            ## NOTE 如果只使用模拟器自带的模型，不使用使用强化学习环境工具包自定义的模型 #DEBUG 还没测试过

            logging.debug("\nexperiments_program.py : 只使用模拟器自带的模型，不使用使用强化学习环境工具包自定义的模型。\n")  # DEBUG专用

            ## 运行实验
            Operator.operate_run_experiment(sgv, para, model)

        elif sgv['is_use_PettingZoo_environments'] is True and sgv['is_use_RLlib_frameworks'] is False:
            ## #NOTE 如果使用 PettingZoo 环境框架结合自定义的环境模型，但是没有用强化学习框架 RLlib 时
            logging.debug("\nexperiments_program.py : 使用 PettingZoo 环境框架结合自定义的环境模型，但是没有用强化学习框架 RLlib 进行训练。\n")  # DEBUG 专用

            ## 重置实验
            A, A_data, sgv, para = Operator.operate_reset_experiment(sgv, para)
            ## 步进式运行实验
            A, A_data, sgv, para = Operator.operate_step_experiment(A, A_data, sgv, para, model)
            # A, A_data, sgv, para, model = Operator.operate_step_experiment(sgv, para, model)
            ## 收尾实验
            Operator.operate_end_experiment(A_data, sgv)

        elif sgv['is_use_PettingZoo_environments'] is True and sgv['is_use_RLlib_frameworks'] is True and sgv['RL_state'] == 'using':
            ## #NOW #NOTE 如果使用 PettingZoo 环境框架结合自定义的环境模型，并且使用强化学习框架 RLlib ，并且强化学习状态是做应用时
            logging.debug("\nexperiments_program.py : 使用 PettingZoo 环境框架结合自定义的环境模型，并且使用强化学习框架 RLlib 已经训练过的模型做运用。\n")  # DEBUG 专用

            ## 重置实验
            A, A_data, sgv, para = Operator.operate_reset_experiment(sgv, para)
            ## 步进式运行实验
            A, A_data, sgv, para = Operator.operate_step_experiment(A, A_data, sgv, para, model)
            # A, A_data, sgv, para, model = Operator.operate_step_experiment(sgv, para, model)
            ## 收尾实验
            Operator.operate_end_experiment(A_data, sgv)

        elif sgv['is_use_PettingZoo_environments'] is True and sgv['is_use_RLlib_frameworks'] is True and sgv['RL_state'] == 'training':
            ## #NOTE 如果使用 PettingZoo 环境框架结合自定义的环境模型，并且使用强化学习框架 RLlib ，并且强化学习状态是做训练时

            logging.debug("\nexperiments_program.py : 使用 PettingZoo 环境框架结合自定义的环境模型，并且使用强化学习框架 RLlib 进行训练。\n")  # DEBUG专用

            # # 设置 RLlib 结果目录 #BUG 不起作用
            # if sgv['system_platform'] == 'Windows':
            #     os.environ["RLLIB_RESULTS_DIR"] = str(Path(sgv['folderpath_experiments_output_log']))  # 设置 RLlib 的结果目录
            # elif sgv['system_platform'] == 'Darwin':
            #     os.environ["RLLIB_RESULTS_DIR"] = str(Path(sgv['folderpath_experiments_output_log'], "ray_results"))  # 设置 RLlib 的结果目录
            # elif sgv['system_platform'] == 'Linux':
            #     os.environ["RLLIB_RESULTS_DIR"] = str(Path(sgv['folderpath_experiments_output_log']))  # 设置 RLlib 的结果目录
            #     pass  # if

            ## 导入包
            # from torch.optim import Adam
            import ray
            from ray import air, tune
            from ray.rllib.algorithms.callbacks import DefaultCallbacks
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

            ray.init()  # 初始化 Ray

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

            # class MyCallbacks(DefaultCallbacks):
            #     def on_train_result(self, trainer, result):
            #         print("trainer.train() result: {}".format(result))
            #         super().on_train_result(trainer, result)

            # 配置项
            config = (
                PPOConfig()
                .experimental(_enable_new_api_stack=False)
                .environment(
                    env=env_name,
                    clip_actions=sgv['clip_actions'],
                    clip_rewards=sgv['clip_rewards'],
                    disable_env_checking=sgv['disable_env_checking'],
                )
                # .optimizer(
                #     type="adam",
                #     adam_eps=1e-8,
                #     grad_clip=None,
                # )
                .resources(
                    num_gpus=int(os.environ.get("RLLIB_NUM_GPUS", "0")),
                )
                .rollouts(
                    num_rollout_workers=sgv['num_rollout_workers'],
                    num_envs_per_worker=sgv['num_envs_per_worker'],
                    rollout_fragment_length=sgv['rollout_fragment_length'],
                    batch_mode="complete_episodes",  # 可选值为 "complete_episodes" 或 "truncate_episodes"。这里建议用 "complete_episodes"。
                )
                .debugging(log_level="ERROR")
                .reporting(
                    metrics_num_episodes_for_smoothing=sgv['metrics_num_episodes_for_smoothing'],
                )
                .training(
                    train_batch_size=sgv['train_batch_size'],
                    lr=sgv['lr'],
                    gamma=sgv['gamma'],
                    lambda_=sgv['lambda_'],
                    use_gae=sgv['use_gae'],
                    clip_param=sgv['clip_param'],
                    grad_clip=sgv['grad_clip'],
                    entropy_coeff=sgv['entropy_coeff'],
                    vf_loss_coeff=sgv['vf_loss_coeff'],
                    sgd_minibatch_size=sgv['sgd_minibatch_size'],
                    num_sgd_iter=sgv['num_sgd_iter'],
                    # optimizer={Adam},
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

            # #TODO 调参
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

    pass  # function


if __name__ == '__main__':
    main()
