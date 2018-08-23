# Нужно доработать скрипт из первого задания. Вот что он должен уметь:
#
##     клонировать репозитории с Гитхаба;
##     выдавать статистику самых частых слов по глаголам или существительным (в зависимости от параметра отчёта);
##     выдавать статистику самых частых слов названия функций или локальных переменных внутри функций (в зависимости от параметра отчёта);
##     выводить результат в консоль, json-файл или csv-файл (в зависимости от параметра отчёта);
##     принимать все аргументы через консольный интерфейс.
#
# При доработке предусмотреть, что вскоре в программу понадобится добавлять:
#
##     получение кода из других места, не только с Гитхаба;
##     парсеры других ЯП, не только Python;
##     сохранение в кучу разных форматов;
##     более сложные типы отчётов (не только частота частей речи в различных местах кода).
#
import logging
import sys
import util.common as common
import util.reporter as rep

log_format = '%(filename)s[LINE:%(lineno)3d]# %(levelname)-8s %(message)s'

logging.basicConfig(format=log_format, level=logging.INFO)

if __name__ == "__main__":
    params = common.parse_input_parameters()
    logging.debug(params)

    work_dir = common.get_working_dir(params.dir)
    logging.debug(work_dir)

    if not rep.clone_remote_repo(params.url, work_dir):
        sys.exit(1)
    report_result = rep.create_report(work_dir, params.lang, params.report, params.topmost)
    formatted_result = rep.format_result(report_result, params.format)
    rep.report_output(params.out)


