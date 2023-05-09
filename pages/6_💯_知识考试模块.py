# coding=utf8
import base64
import copy
import time
import json
import os

import streamlit as st

from lib.JSCookieManager import JSCookieManager
from common.init_user import initUserConfig
from common.refresh import refreshPage
from common.hide_iframe import hideIframe
from conf.path import root_path, images_common_path
from conf.menu import menu_items
from core.timer import timer, destroyTimer
from core.exam.init_paper import initPaper
from core.exam.grade_paper import gradePaper, showGrades


# ---------- Start:每页基础配置 ---------- #
st.set_page_config(
    page_title="知识考试模块", page_icon="💯", layout="wide", menu_items=menu_items, initial_sidebar_state="expanded"
)
initUserConfig()
# ---------- End:每页基础配置 ---------- #


def createPaperPage():
    """显示试卷"""
    # 判断是否已完成
    finished = st.session_state.exam_config["finished"]
    # 选择题
    st.markdown(f"##### 一、不定向选择题")
    st.markdown("> 注：选对一个选项得1分，上限5分；或全选对得5分；有错选得0分。")
    with st.expander("展开"):
        for choices_question_index, choices_question_dict in enumerate(choices_questions):
            choices_question = choices_question_dict["question"]
            choices_options = choices_question_dict["options"]
            choices_key = f"choices-{choices_question_index}"
            choices_examinee = []
            if finished:
                choices_grade_answer = grade_answer["choices"][choices_key]
                choices_points = choices_grade_answer["points"]
                choices_examinee = [choices_options[i] for i in choices_grade_answer["examinee"]]
                choices_correct = choices_grade_answer["correct"]
            st.multiselect(
                f"【第{choices_question_index+1}题】{choices_question}",
                choices_options,
                default=choices_examinee,
                key=choices_key,
                disabled=finished
            )
            if finished:
                st.info("正确答案：{}".format("；".join([choices_options[i] for i in choices_correct])))
                if choices_points == 0:
                    st.error(f"得分：{choices_points}")
                elif choices_points == 5:
                    st.success(f"得分：{choices_points}")
                else:
                    st.warning(f"得分：{choices_points}")
    # 判断题
    st.markdown(f"##### 二、判断题")
    st.markdown("> 注：每题2分。")
    with st.expander("展开"):
        for judgement_question_index, judgement_question_dict in enumerate(judgement_questions):
            judgement_question = judgement_question_dict["question"]
            judgement_key = f"judgement-{judgement_question_index}"
            judgement_examinee = 0
            if finished:
                judgement_grade_answer = grade_answer["judgement"][judgement_key]
                judgement_points = judgement_grade_answer["points"]
                judgement_examinee = judgement_grade_answer["examinee"]
                judgement_correct = judgement_grade_answer["correct"]
            st.radio(
                f"【第{judgement_question_index+1}题】{judgement_question}",
                ["×", "√"],
                horizontal=False,
                index=judgement_examinee,
                key=judgement_key,
                disabled=finished
            )
            if finished:
                st.info("正确答案：{}".format(["×", "√"][judgement_correct]))
                if judgement_points == 0:
                    st.error(f"得分：{judgement_points}")
                else:
                    st.success(f"得分：{judgement_points}")
    # 填空题
    st.markdown(f"##### 三、填空题")
    st.markdown("> 注：每空2分。")
    with st.expander("展开"):
        for completions_question_index, completions_question_dict in enumerate(completions_questions):
            completions_question = completions_question_dict["question"]
            completions_blanks = completions_question_dict["blanks"]
            st.markdown(f"【第{completions_question_index+1}题】{completions_question}")
            for blank_index in range(completions_blanks):
                completions_key = f"completions-{completions_question_index}-{blank_index}"
                completions_examinee = ""
                if finished:
                    completions_grade_answer = grade_answer["completions"][completions_key]
                    completions_points = completions_grade_answer["points"]
                    completions_examinee = completions_grade_answer["examinee"]
                    completions_correct = completions_grade_answer["correct"]
                st.text_input(
                    f"第({blank_index+1})空：",
                    key=completions_key,
                    value=completions_examinee,
                    disabled=finished
                )
                if finished:
                    st.info("正确答案：{}".format(completions_correct))
                    if completions_points == 0:
                        st.error(f"得分：{completions_points}")
                    else:
                        st.success(f"得分：{completions_points}")
    # 计算填空题
    st.markdown(f"##### 四、计算填空题")
    st.markdown("> 注：每空10分。")
    # 企业 Q 值计算
    st.markdown(f"###### 四一、企业Q值计算")
    with st.expander("展开"):
        for Q_question_index, Q_question_dict in enumerate(Q_questions):
            Q_question = Q_question_dict["question"]
            st.markdown(f"【第{Q_question_index+1}题】{Q_question}")
            Q_key = f"Q-{Q_question_index}"
            Q_examinee = 0.00
            if finished:
                Q_grade_answer = grade_answer["Q"][Q_key]
                Q_points = Q_grade_answer["points"]
                Q_examinee = Q_grade_answer["examinee"]
                Q_correct = Q_grade_answer["correct"]
            st.number_input(
                "Q值：",
                step=0.01,
                key=Q_key,
                value=Q_examinee,
                disabled=finished
            )
            if finished:
                st.info("正确答案：{}".format(Q_correct))
                if Q_points == 0:
                    st.error(f"得分：{Q_points}")
                else:
                    st.success(f"得分：{Q_points}")
                st.markdown(Q_question_dict["explanation"])
    # 泄漏量计算
    st.markdown(f"###### 四二、泄漏量计算")
    with st.expander("展开"):
        for leakage_question_index, leakage_question_dict in enumerate(leakage_questions):
            leakage_question = leakage_question_dict["question"]
            st.markdown(f"【第{leakage_question_index+1}题】{leakage_question}")
            leakage_key = f"leakage-{leakage_question_index}"
            leakage_examinee = 0.00
            if finished:
                leakage_grade_answer = grade_answer["leakage"][leakage_key]
                leakage_points = leakage_grade_answer["points"]
                leakage_examinee = leakage_grade_answer["examinee"]
                leakage_correct = leakage_grade_answer["correct"]
            st.number_input(
                "泄漏流量：", 
                step=0.01, 
                key=leakage_key,
                value=leakage_examinee,
                disabled=finished
            )
            if finished:
                st.info("正确答案：{}".format(leakage_correct))
                if leakage_points == 0:
                    st.error(f"得分：{leakage_points}")
                else:
                    st.success(f"得分：{leakage_points}")
    # 事故应急池计算
    st.markdown(f"###### 四三、事故应急池计算")
    with st.expander("展开"):
        for pool_question_index, pool_question_dict in enumerate(pool_questions):
            pool_question = pool_question_dict["question"]
            st.markdown(f"【第{pool_question_index+1}题】{pool_question}")
            pool_key = f"pool-{pool_question_index}"
            pool_examinee = 0.00
            if finished:
                pool_grade_answer = grade_answer["pool"][pool_key]
                pool_points = pool_grade_answer["points"]
                pool_examinee = pool_grade_answer["examinee"]
                pool_correct = pool_grade_answer["correct"]
            st.number_input(
                "事故应急池最小容量：",
                step=0.01,
                key=pool_key,
                value=pool_examinee,
                disabled=finished
            )
            if finished:
                st.info("正确答案：{}".format(pool_correct))
                if pool_points == 0:
                    st.error(f"得分：{pool_points}")
                else:
                    st.success(f"得分：{pool_points}")
    # 消防废水计算
    st.markdown(f"###### 四四、消防废水相关计算")
    with st.expander("展开"):
        for waste_water_question_index, waste_water_question_dict in enumerate(waste_water_questions):
            waste_water_question = waste_water_question_dict["question"]
            no_outdoor = waste_water_question_dict["no_outdoor"]
            st.markdown(f"【第{waste_water_question_index+1}题】{waste_water_question}")
            waste_water_key_1 = f"waste_water-{waste_water_question_index}-1"
            waste_water_examinee1 = 0.00
            if finished:
                waste_water_grade_answer1 = grade_answer["waste_water"][waste_water_key_1]
                waste_water_points1 = waste_water_grade_answer1["points"]
                waste_water_examinee1 = waste_water_grade_answer1["examinee"]
                waste_water_correct1 = waste_water_grade_answer1["correct"]
            st.number_input(
                "消防水池最小有效容积：",
                step=0.01,
                key=waste_water_key_1,
                value=waste_water_examinee1,
                disabled=finished
            )
            if finished:
                st.info("正确答案：{}".format(waste_water_correct1))
                if waste_water_points1 == 0:
                    st.error(f"得分：{waste_water_points1}")
                else:
                    st.success(f"得分：{waste_water_points1}")
            if not no_outdoor:
                waste_water_key_2 = f"waste_water-{waste_water_question_index}-2"
                waste_water_examinee2 = 0.00
                if finished:
                    waste_water_grade_answer2 = grade_answer["waste_water"][waste_water_key_2]
                    waste_water_points2 = waste_water_grade_answer2["points"]
                    waste_water_examinee2 = waste_water_grade_answer2["examinee"]
                    waste_water_correct2 = waste_water_grade_answer2["correct"]
                st.number_input(
                    "消防水量：",
                    step=0.01,
                    key=waste_water_key_2,
                    value=waste_water_examinee2,
                    disabled=finished
                )
                if finished:
                    st.info("正确答案：{}".format(waste_water_correct2))
                    if waste_water_points2 == 0:
                        st.error(f"得分：{waste_water_points2}")
                    else:
                        st.success(f"得分：{waste_water_points2}")
            if finished:
                st.markdown(waste_water_question_dict["explanation"])
    # 落地浓度计算
    st.markdown(f"###### 四五、落地浓度计算")
    with st.expander("展开"):
        for potency_question_index, potency_question_dict in enumerate(potency_questions):
            potency_question = potency_question_dict["question"]
            st.markdown(f"【第{potency_question_index+1}题】{potency_question}")
            potency_key_1 = f"potency-{potency_question_index}-1"
            potency_examinee1 = 0.00
            if finished:
                potency_grade_answer1 = grade_answer["potency"][potency_key_1]
                potency_points1 = potency_grade_answer1["points"]
                potency_examinee1 = potency_grade_answer1["examinee"]
                potency_correct1 = potency_grade_answer1["correct"]
            st.number_input(
                "轴向浓度：", 
                step=0.01, 
                key=potency_key_1,
                value=potency_examinee1,
                disabled=finished
            )
            if finished:
                st.info("正确答案：{}".format(potency_correct1))
                if potency_points1 == 0:
                    st.error(f"得分：{potency_points1}")
                else:
                    st.success(f"得分：{potency_points1}")
            potency_key_2 = f"potency-{potency_question_index}-2"
            potency_examinee2 = 0.00
            if finished:
                potency_grade_answer2 = grade_answer["potency"][potency_key_2]
                potency_points2 = potency_grade_answer2["points"]
                potency_examinee2 = potency_grade_answer2["examinee"]
                potency_correct2 = potency_grade_answer2["correct"]
            st.number_input(
                "最大地面浓度：", 
                step=0.01, 
                key=potency_key_2,
                value=potency_examinee2,
                disabled=finished
            )
            if finished:
                st.info("正确答案：{}".format(potency_correct2))
                if potency_points2 == 0:
                    st.error(f"得分：{potency_points2}")
                else:
                    st.success(f"得分：{potency_points2}")
            potency_key_3 = f"potency-{potency_question_index}-3"
            potency_examinee3 = 0.00
            if finished:
                potency_grade_answer3 = grade_answer["potency"][potency_key_3]
                potency_points3 = potency_grade_answer3["points"]
                potency_examinee3 = potency_grade_answer3["examinee"]
                potency_correct3 = potency_grade_answer3["correct"]
            st.number_input(
                "最大地面浓度产生距离：", 
                step=0.01, 
                key=potency_key_3,
                value=potency_examinee3,
                disabled=finished
            )
            if finished:
                st.info("正确答案：{}".format(potency_correct3))
                if potency_points3 == 0:
                    st.error(f"得分：{potency_points3}")
                else:
                    st.success(f"得分：{potency_points3}")
                st.markdown(potency_question_dict["explanation"])


def stopTimer():
    """停止计时"""
    destroyTimer()
    st.session_state.set_used_time = False
    JSCookieManager(key="exam_timer", value=json.dumps({
        "used_time": 0
    }))


def submit():
    """提交试卷"""
    # 选择题
    choices_questions_keys = list(examinee_answer["choices"].keys())
    for choices_question_key_index, choices_question_key in enumerate(choices_questions_keys):
        choices_question_option = paper["choices_questions"][choices_question_key_index]["options"]
        examinee_answer["choices"][choices_question_key] = [choices_question_option.index(i) for i in st.session_state.get(choices_question_key)]
    # 判断题
    judgement_questions_keys = list(examinee_answer["judgement"].keys())
    for judgement_question_key_index, judgement_question_key in enumerate(judgement_questions_keys):
        examinee_answer["judgement"][judgement_question_key] = 0 if st.session_state.get(judgement_question_key) == "×" else 1
    # 填空题
    for questions_type in list(examinee_answer.keys())[2:]:
        questions_type_keys = list(examinee_answer[questions_type].keys())
        for question_type_key_index, question_type_key in enumerate(questions_type_keys):
            examinee_answer[questions_type][question_type_key] = st.session_state.get(question_type_key)
    # 将答案压缩
    examinee_answer_list = [list(i.values()) for i in list(examinee_answer.values())]
    examinee_answer_compress = {
        "answer": examinee_answer_list,
        "seed": seed,
        "amount": questions_amount
    }
    # 保存至应用会话
    st.session_state.exam_config = {
        "seed": seed,
        "amount": questions_amount,
        "finished": True,
        "answer": examinee_answer_compress
    }


def initExamConfig(**kwargs):
    """初始化试卷设置"""
    e_conf = st.session_state.get("exam_config")
    # 重做本卷
    if kwargs.get("seed") is not None:
        # 停止计时
        stopTimer()
        e_conf = {
            "seed": kwargs.get("seed"),
            "amount": kwargs.get("amount"),
            "finished": False,
            "answer": {}
        }
    # 重新组卷
    elif kwargs.get("amount") is not None:
        # 停止计时
        stopTimer()
        e_conf = {
            "seed": 0,
            "amount": kwargs.get("amount"),
            "finished": False,
            "answer": {}
        }
    # 初始化
    elif (e_conf is None) or kwargs.get("reload"):
        # 停止计时
        stopTimer()
        e_conf = {
            "seed": 0,
            "amount": 0,
            "finished": False,
            "answer": {}
        }
    st.session_state.exam_config = e_conf


# 初始化试卷设置
initExamConfig()
exam_config = st.session_state.exam_config

# 难度选择
difficulty_level = ["请选择", "一级（30题）", "二级（60题）", "三级（90题）", "查看历史"]
with st.sidebar:
    st.radio(
        "选择考试难度",
        difficulty_level,
        key="questions_amount",
        on_change=lambda: initExamConfig(reload=True)
    )
questions_amount = int(difficulty_level.index(st.session_state.questions_amount) * 30)

# 提示选择题量
if questions_amount == 0:
    stopTimer()
    st.warning("请选择考试难度以生成试卷！")
    with open(os.path.join(images_common_path, "motto.jpg"), "rb") as fp:
        st.image(fp.read())
# 查看历史考试
elif questions_amount == 120:
    # 必须连接云
    jgy = st.session_state.get("jgy")
    if jgy is None:
        st.warning("未连接坚果云，无法查看考试记录！")
    else:
        # 获取考试记录列表
        exams_history_response = jgy.listdir(exams=True)
        if exams_history_response and exams_history_response.get("code") == 200:
            # 整理为试卷编号列表
            exams_history = sorted([i["name"].split("/")[-1].replace(".b64", "") for i in exams_history_response["files"]], reverse=True)
            if len(exams_history) > 0:
                # 下拉选择
                st.selectbox(
                    "请选择要查看的历史考试：",
                    exams_history,
                    key="exams_history",
                    format_func=lambda x: f"编号：{x}"
                )
                # 获取选择的考试编号对应的考试详情
                get_exams_history = jgy.get(st.session_state.exams_history, exams=True)
                if get_exams_history and get_exams_history.get("code") == 200:
                    # 解 base64
                    exams_history_details = json.loads(base64.b64decode(get_exams_history["value"]).decode())
                    # 点击查看
                    if st.button("查看考试详情", key="exam_details"):
                        exam_config = {
                            "seed": exams_history_details["seed"],
                            "amount": exams_history_details["amount"],
                            "finished": True,
                            "answer": exams_history_details
                        }
                        st.session_state.exam_config = exam_config
                        st.session_state.history = True
                else:
                    st.warning("获取考试详情失败！")
            else:
                st.warning("暂无考试记录！")
        else:
            st.warning("坚果云连接失败，无法查看考试记录！")

# 选择了难度/查看历史
if (questions_amount not in [0, 120]) or st.session_state.get("history"):
    if questions_amount == 120:
        questions_amount = exam_config["amount"]
    else:
        st.session_state.history = False
    # 生成试卷
    with st.spinner("正在生成试卷"):
        # 新生成
        if exam_config["seed"] == 0:
            paper, examinee_answer = initPaper(amount=questions_amount)
        # 恢复
        else:
            paper, examinee_answer = initPaper(amount=questions_amount, seed=exam_config["seed"])
        seed = paper["seed"]
        exam_config["seed"] = seed
        exam_config["amount"] = questions_amount
        st.session_state.exam_config = exam_config
        choices_questions = paper["choices_questions"]
        judgement_questions = paper["judgement_questions"]
        completions_questions = paper["completions_questions"]
        Q_questions = paper["Q_questions"]
        leakage_questions = paper["leakage_questions"]
        pool_questions = paper["pool_questions"]
        waste_water_questions = paper["waste_water_questions"]
        potency_questions = paper["potency_questions"]
    # 获取所有题目编号
    question_keys = [list(i.keys()) for i in list(examinee_answer.values())]
    # 显示试卷
    if not exam_config["finished"]:
        if not st.session_state.history:
            st.button("重新组卷", key="reload", on_click=lambda: initExamConfig(amount=questions_amount))
        with st.form("exam"):
            # 试卷头
            st.info(f"本试卷编号{seed}，共{questions_amount}题，考试时间{int(40 * questions_amount / 30)}分钟。")
            # 试卷主体
            createPaperPage()
            # 提交按钮
            st.form_submit_button("提交试卷", on_click=submit, use_container_width=True)
            # 计时器
            if not st.session_state.get("set_used_time"):
                st.session_state.set_used_time = True
                JSCookieManager(key="exam_timer", value=json.dumps({
                    "used_time": 0
                }))
            timer()
    else:
        # 保存用时
        if st.session_state.exam_timer["used_time"] != 0:
            st.session_state.exam_config["answer"]["used_time"] = st.session_state.exam_timer["used_time"]
            st.session_state.exam_config["answer"]["timestamp"] = st.session_state.exam_timer["timestamp"]
        # 停止计时
        stopTimer()
        st.button("重做本卷", key="redo", on_click=lambda: initExamConfig(amount=questions_amount, seed=seed))
        # 试卷编号
        st.markdown(f"##### 试卷编号：{seed}")
        # 用时
        used_time = st.session_state.exam_config["answer"].get("used_time")
        if used_time is not None:
            used_time = time.strftime("%H:%M:%S", time.gmtime(used_time))
            st.markdown(f"##### 用时：{used_time}")
        # 开始评分
        grades, grade_answer = gradePaper(examinee_answer_compress=st.session_state.exam_config["answer"])
        st.session_state.exam_config["answer"]["hundred"] = grades["hundred"]
        # 提供成绩上传
        jgy = st.session_state.get("jgy")
        if jgy is not None:
            if st.button("保存成绩", key="upload_grades"):
                with st.spinner("正在上传成绩..."):
                    upload_res = jgy.set(param=f"{seed}", value=json.dumps(st.session_state.exam_config["answer"]), exams=True)
                    if upload_res.get("code") == 200:
                        st.success("已上传！")
                    else:
                        st.error(f"上传失败: {upload_res['msg']}")
        st.markdown(f"##### 得分：{grades['examinee']}")
        st.markdown(f"##### 百分制得分：{grades['hundred']}")
        # 得分图
        if st.checkbox("展开得分图", key="check_photo"):
            showGrades(grades=grades)
        # 具体评分
        if st.checkbox("查看试卷详情", key="check_details"):
            createPaperPage()


# ---------- Start:每页基础配置 ---------- #
# 隐藏自定义的 JS 组件, 并显示 streamlit 原生组件
hideIframe()
# ---------- End:每页基础配置 ---------- #