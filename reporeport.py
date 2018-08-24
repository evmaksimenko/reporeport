import logging
import sys
import util.common as common
import util.reporter as rep

log_format = '%(filename)s[LINE:%(lineno)3d]# %(levelname)-8s %(message)s'

logging.basicConfig(format=log_format, level=logging.ERROR)

if __name__ == "__main__":
    params = common.parse_input_parameters()

    work_dir = common.get_working_dir(params.dir)
    logging.info("Directory to clone: " + work_dir)

    if not rep.clone_remote_repo(params.url, work_dir):
        sys.exit(1)

    report_result = rep.create_report(work_dir, params.lang, params.report,
                                      params.topmost)
    logging.info("Report result: " + report_result)

    formatted_result = rep.format_result(report_result, params.format)
    logging.info("Formatted result: " + formatted_result)

    rep.report_output(params.out, formatted_result)
