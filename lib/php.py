#-*- coding:utf-8 -*-
from commands import getoutput
from termcolor import colored
from common import get_commit_errors as get_php_commit_errors
from common import get_receive_errors as get_php_receive_errors
from config import base_path, config

def get_commit_errors():
  return get_php_commit_errors("php", _get_commit_file_error)

def _get_commit_file_error(path):
  file_errors = _get_error(path, "emacs")
  if not file_errors:
    return None

  errors = []
  for error in file_errors:
    error_type = error.split(' ')[1]
    if error_type == 'error':
      errors.append(colored(error, "red"))
    else:
      errors.append(colored(error, "yellow"))

  return "\n".join(errors)

def get_receive_errors(rev_old, rev_new):
  return get_php_receive_errors(
    rev_old, rev_new, "php", _get_receive_file_error
  )

def _get_receive_file_error(path):
  file_errors = _get_error(path, "summary")
  if not file_errors:
    return None

  file_error = file_errors[-2].split(" ")
  error_count = int(file_error[3])
  warning_count = int(file_error[6])
  error = colored("%s error(s)" % error_count, "red")
  warning = colored("%s warning(s)" % warning_count, "yellow")

  if error_count > 0 and warning_count > 0:
    return "    %s  %s" % (error, warning)

  if error_count > 0 or warning_count > 0:
    return "    %s" % (error if error_count > 0 else warning)

  return None

def _get_error(path, report):
  errors = getoutput(
    "%s/bin/phpcs --report=%s %s" % (base_path, report, path)
  ).split("\n")

  return [error for error in errors if error]
